"""Read-only Zotero Local API v3; no cloud fallback and no database access."""
import ipaddress
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from .core import WikiError, import_pdf, local_path


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Zotero:
    def __init__(self, project):
        self.project = project
        cfg = project.config.get("zotero", {})
        self.base = cfg.get("base_url", "http://localhost:23119/api/").rstrip("/") + "/"
        parsed = urlsplit(self.base)
        host = parsed.hostname or ""
        try:
            local = host == "localhost" or ipaddress.ip_address(host).is_loopback or ipaddress.ip_address(host).is_private
        except ValueError:
            local = host == "localhost"
        if not local or parsed.scheme not in ("http", "https") or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise WikiError("Zotero base_url must be a local/private HTTP(S) address without credentials or query parameters.")
        self.library = cfg.get("library", "users/0")
        if not re.fullmatch(r"(?:users|groups)/\d+", self.library):
            raise WikiError("Zotero library must be users/<number> or groups/<number>.")
        self.timeout = max(1, min(30, float(cfg.get("timeout", 5))))
        self.server_id = None
        self.api_version = None
        self.opener = build_opener(ProxyHandler({}), NoRedirect())

    def request(self, endpoint="", params=None):
        url = self.base + endpoint
        if params:
            url += "?" + urlencode(params)
        headers = {"Zotero-API-Version": "3"}
        if self.server_id:
            headers["Zotero-Server-ID"] = self.server_id
        try:
            with self.opener.open(Request(url, headers=headers, method="GET"), timeout=self.timeout) as response:
                self.api_version = response.headers.get("Zotero-API-Version", self.api_version)
                self.server_id = response.headers.get("Zotero-Server-ID", self.server_id)
                if self.api_version and self.api_version != "3":
                    raise WikiError("Zotero API version is not 3; this client does not support it.")
                return response.read(), response.headers
        except HTTPError as exc:
            if exc.code in (301, 302, 303, 307, 308):
                location = exc.headers.get("Location", "")
                if location.startswith("file:"):
                    return location.encode(), exc.headers
                raise WikiError("Zotero returned an unexpected redirect; no remote resource was fetched.") from exc
            hints = {403: "Enable Settings > Advanced > Allow other applications on this computer to communicate with Zotero.",
                     404: "Check library/item/attachment key and Zotero Local API support.",
                     412: "Zotero server identity changed. Re-run the command and check the selected library."}
            raise WikiError(f"Zotero HTTP {exc.code}. {hints.get(exc.code, 'Check Zotero and the selected library.')} Manual import-pdf remains available.") from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise WikiError("Zotero Local API unreachable. Start Zotero and enable its Local API; check config.local.toml. For WSL use an explicitly reachable local address or Windows execution; do not expose the port. Manual import-pdf remains available.") from exc

    def get(self, endpoint, params=None):
        data, _ = self.request(endpoint, params)
        try:
            return json.loads(data)
        except (ValueError, UnicodeError) as exc:
            raise WikiError("Zotero returned invalid JSON.") from exc

    def probe(self):
        self.request()
        return {"reachable": True, "api_version": self.api_version, "server_id_available": bool(self.server_id)}

    @staticmethod
    def key(value):
        if not re.fullmatch(r"[A-Z0-9]{8}", value):
            raise WikiError("Zotero item/collection key must be 8 uppercase letters or digits.")
        return value

    def listing(self, collections=False, collection=None, items=None, limit=20, start=0):
        if not 1 <= limit <= 100 or start < 0:
            raise WikiError("Use limit 1..100 and start >= 0; listing is explicitly bounded.")
        self.probe()
        params = {"limit": limit, "start": start, "format": "json"}
        if collections:
            endpoint = f"{self.library}/collections"
        elif collection:
            endpoint = f"{self.library}/collections/{self.key(collection)}/items/top"
        elif items:
            keys = [self.key(k.strip()) for k in items.split(",")]
            if len(keys) > 100:
                raise WikiError("Select at most 100 item keys.")
            endpoint = f"{self.library}/items"
            params["itemKey"] = ",".join(keys)
        else:
            raise WikiError("Select --collections, --collection KEY, or --items KEY1,KEY2; no whole-library import.")
        values = self.get(endpoint, params)
        if not isinstance(values, list):
            raise WikiError("Expected a Zotero result list.")
        return {"items": [{"key": x.get("key"), "title": x.get("data", {}).get("title") or x.get("data", {}).get("name"),
                           "item_type": x.get("data", {}).get("itemType")} for x in values],
                "start": start, "limit": limit, "next_start_if_more": start + limit if len(values) == limit else None}

    def import_item(self, key, attachment=None, version=None, revision_of=None):
        key = self.key(key)
        self.probe()
        item = self.get(f"{self.library}/items/{key}")
        if item.get("data", {}).get("itemType") == "attachment":
            raise WikiError("Select the parent paper item, not its attachment key.")
        if attachment:
            selected = self.get(f"{self.library}/items/{self.key(attachment)}")
            if selected.get("data", {}).get("parentItem") != key:
                raise WikiError("The selected attachment does not belong to the selected paper.")
        else:
            children = self.get(f"{self.library}/items/{key}/children", {"limit": 100, "format": "json"})
            attachments = [x for x in children if x.get("data", {}).get("itemType") == "attachment"
                           and x.get("data", {}).get("contentType") == "application/pdf"]
            if len(children) >= 100 or len(attachments) != 1:
                keys = ", ".join(x["key"] for x in attachments) or "none"
                raise WikiError(f"Select one PDF with --attachment KEY. PDF candidates: {keys}. If none are local, use import-pdf.")
            selected = attachments[0]
        if selected.get("data", {}).get("contentType") != "application/pdf":
            raise WikiError("The selected attachment is not a PDF.")
        attachment_key = self.key(selected["key"])
        try:
            raw, _ = self.request(f"{self.library}/items/{attachment_key}/file/view/url")
        except WikiError as exc:
            if "HTTP 404" not in str(exc):
                raise
            raw, _ = self.request(f"{self.library}/items/{attachment_key}/file")
        try:
            path = local_path(raw.decode("utf-8"), self.project.config)
        except UnicodeError as exc:
            raise WikiError("Expected a local attachment URL, not binary download data.") from exc
        if not path.is_file():
            raise WikiError("Zotero PDF is not available at its local path. Download it in Zotero, map the Windows drive in WSL, or use import-pdf.")
        data = item["data"]
        authors = [(c.get("name") or " ".join(filter(None, (c.get("firstName"), c.get("lastName")))))
                   for c in data.get("creators", []) if c.get("creatorType") == "author"]
        date = re.search(r"\b(\d{4})\b", data.get("date", ""))
        alias = {"library": self.library, "item_key": key, "attachment_key": attachment_key,
                 "server_id": self.server_id, "item_version": item.get("version")}
        return import_pdf(self.project, path, title=data.get("title"), authors=authors,
                          year=int(date[1]) if date else None, doi=data.get("DOI"), source_url=data.get("url"),
                          version=version, revision_of=revision_of, zotero=alias)
