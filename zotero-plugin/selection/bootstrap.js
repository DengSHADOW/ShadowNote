/* Read-only Zotero 10 bridge. Source is distributed with the project. */
var endpointPath = "/api/paper-wiki/selection";
var selectionEndpoint = null;

function install() {}
function uninstall() {}

function currentItems(view) {
    const main = Zotero.getMainWindow();
    const recent = Services.wm.getMostRecentWindow(null);
    if (view !== "library" && recent?.reader) {
        const item = Zotero.Items.get(recent.reader.itemID);
        return {kind: "reader-window", items: item ? [item] : []};
    }
    if (!main) return {kind: "none", items: [], problem: "No Zotero library window is open."};
    if (view !== "library" && recent && recent !== main) {
        return {kind: "none", items: [], problem: "Activate the Zotero library or PDF reader once, then retry."};
    }
    if (view !== "library" && main.Zotero_Tabs?.selectedID !== "zotero-pane") {
        const reader = Zotero.Reader.getByTabID(main.Zotero_Tabs?.selectedID);
        const item = reader?.itemID && Zotero.Items.get(reader.itemID);
        return {kind: "reader-tab", items: item ? [item] : [],
            problem: item ? null : "The active tab is not a loaded attachment reader. No library selection was substituted."};
    }
    if (view === "reader") return {kind: "none", items: [], problem: "No attachment reader is active."};
    return {kind: "library", items: main.ZoteroPane?.getSelectedItems() || []};
}

async function describeItem(selected) {
    const library = Zotero.Libraries.get(selected.libraryID);
    let libraryPath = null;
    if (selected.libraryID === Zotero.Libraries.userLibraryID) libraryPath = "users/0";
    else if (library?.libraryType === "group") libraryPath = "groups/" + library.groupID;
    let paper = selected.isRegularItem() ? selected : null;
    let attachment = null;
    let problem = null;
    if (selected.isAttachment() && selected.attachmentContentType === "application/pdf") {
        attachment = selected;
        paper = selected.parentItemID ? await Zotero.Items.getAsync(selected.parentItemID) : null;
        if (!paper) problem = "Standalone PDF: use import-pdf, or attach it to a parent paper in Zotero.";
    }
    if (!paper && !problem) problem = "Select a paper item or a PDF attachment, not a note/annotation.";
    if (selected.deleted || paper?.deleted) problem = "The selected item is in the trash.";
    if (!libraryPath) problem = "This library type is not supported.";
    const ids = attachment ? [attachment.id] : (paper ? paper.getAttachments() : []);
    const pdfs = [];
    for (const id of ids.slice(0, 100)) {
        const item = await Zotero.Items.getAsync(id);
        if (item?.isAttachment() && !item.deleted && item.attachmentContentType === "application/pdf") {
            pdfs.push({key: item.key, title: item.getField("title"),
                available_locally: Boolean(await item.getFilePathAsync()),
                linked_file: item.attachmentLinkMode === Zotero.Attachments.LINK_MODE_LINKED_FILE});
        }
    }
    if (ids.length > 100) problem = "Too many attachments; select the intended PDF attachment explicitly.";
    return {selected_key: selected.key, item_type: selected.itemType,
        library: libraryPath, item_key: paper?.key || null,
        attachment_key: attachment?.key || null,
        title: paper?.getField("title") || selected.getField("title") || "",
        pdf_attachments: pdfs, problem};
}

async function startup() {
    // Add-ons can be installed while Zotero is still starting. Registering a
    // Local API endpoint before the server exists makes Add-on Manager report
    // a generic, misleading compatibility failure.
    await Zotero.initializationPromise;
    if (!Zotero.Server?.LocalAPI?.Root) throw new Error("Paper Wiki Selection requires Zotero 10 Local API.");
    if (Zotero.Server.Endpoints[endpointPath]) throw new Error("Paper Wiki endpoint already registered.");
    selectionEndpoint = class extends Zotero.Server.LocalAPI.Root {
        supportedMethods = ["GET"];
        async run(request) {
            if (request.headers.get("X-Paper-Wiki") !== "1") {
                return [403, "text/plain", "Use the Paper Wiki local client."];
            }
            const view = request.searchParams.get("view") || "auto";
            if (!["auto", "library", "reader"].includes(view)) return [400, "text/plain", "Invalid view."];
            const snapshot = currentItems(view);
            if (snapshot.items.length > 20) return [400, "text/plain", "Select at most 20 items."];
            const items = [];
            for (const item of snapshot.items) items.push(await describeItem(item));
            return [200, {"Content-Type": "application/json", "Cache-Control": "no-store"},
                JSON.stringify({schema_version: 1, bridge_version: "0.1.0",
                    selection_kind: snapshot.kind, problem: snapshot.problem || null, items})];
        }
    };
    Zotero.Server.Endpoints[endpointPath] = selectionEndpoint;
}

function shutdown() {
    if (Zotero.Server.Endpoints[endpointPath] === selectionEndpoint) delete Zotero.Server.Endpoints[endpointPath];
    selectionEndpoint = null;
}
