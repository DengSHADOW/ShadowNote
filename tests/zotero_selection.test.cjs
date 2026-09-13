// Mocked Zotero runtime contract tests, not a live application test.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
async function fixture() {
    const paper = {id: 1, key: 'PAPER123', libraryID: 1, itemType: 'journalArticle',
        isRegularItem: () => true, isAttachment: () => false,
        getField: () => 'Fixture paper', getAttachments: () => [2]};
    const pdf = {id: 2, key: 'ATTACH12', libraryID: 1, itemType: 'attachment', parentItemID: 1,
        attachmentContentType: 'application/pdf', attachmentLinkMode: 0,
        isRegularItem: () => false, isAttachment: () => true,
        getField: () => 'Fixture PDF', getFilePathAsync: async () => '/fixture.pdf'};
    const main = {Zotero_Tabs: {selectedID: 'zotero-pane'}, ZoteroPane: {getSelectedItems: () => [paper]}};
    const state = {recent: main, main, reader: {itemID: 2}};
    const items = new Map([[1, paper], [2, pdf]]);
    const Zotero = {getMainWindow: () => state.main,
        Items: {get: id => items.get(id), getAsync: async id => items.get(id)},
        Libraries: {userLibraryID: 1, get: () => ({libraryType: 'group', groupID: 1234})},
        Reader: {getByTabID: () => state.reader},
        Attachments: {LINK_MODE_LINKED_FILE: 2},
        Server: {LocalAPI: {Root: class {}}, Endpoints: {}}};
    const context = vm.createContext({Zotero, Services: {wm: {getMostRecentWindow: () => state.recent}}});
    vm.runInContext(fs.readFileSync('zotero-plugin/selection/bootstrap.js', 'utf8'), context);
    await context.startup();
    const endpoint = new Zotero.Server.Endpoints['/api/paper-wiki/selection']();
    async function request(view = 'auto', header = '1') {
        return endpoint.run({headers: new Headers({'X-Paper-Wiki': header}), searchParams: new URLSearchParams({view})});
    }
    async function snapshot(view) { const response = await request(view); assert.equal(response[0], 200); return JSON.parse(response[2]); }
    return {paper, pdf, main, state, Zotero, context, endpoint, request, snapshot};
}
test('library selection works without opening PDF and reports local availability', async () => {
    const f = await fixture();
    const s = await f.snapshot();
    assert.equal(s.selection_kind, 'library');
    assert.equal(s.items[0].item_key, 'PAPER123');
    assert.equal(s.items[0].pdf_attachments[0].available_locally, true);
    f.pdf.getFilePathAsync = async () => false;
    assert.equal((await f.snapshot()).items[0].pdf_attachments[0].available_locally, false);
});
test('active reader wins, explicit library override works, unloaded reader never falls back', async () => {
    const f = await fixture(); f.main.Zotero_Tabs.selectedID = 'reader-tab';
    assert.equal((await f.snapshot()).items[0].attachment_key, 'ATTACH12');
    assert.equal((await f.snapshot('library')).items[0].attachment_key, null);
    f.state.reader = null;
    const s = await f.snapshot(); assert.equal(s.items.length, 0); assert.match(s.problem, /not a loaded/);
});
test('independent reader and unknown window are distinguished', async () => {
    const f = await fixture(); f.state.recent = {reader: {itemID: 2}};
    assert.equal((await f.snapshot()).selection_kind, 'reader-window');
    f.state.recent = {};
    assert.match((await f.snapshot()).problem, /Activate/);
    assert.equal((await f.snapshot('library')).selection_kind, 'library');
});
test('none and multiple selections remain explicit', async () => {
    const f = await fixture(); f.main.ZoteroPane.getSelectedItems = () => [];
    assert.equal((await f.snapshot()).items.length, 0);
    f.main.ZoteroPane.getSelectedItems = () => [f.paper, f.pdf];
    assert.equal((await f.snapshot()).items.length, 2);
    f.main.ZoteroPane.getSelectedItems = () => Array(21).fill(f.paper);
    assert.equal((await f.request())[0], 400);
});
test('group, standalone PDF, and trash are identified', async () => {
    const f = await fixture(); f.paper.libraryID = 2;
    assert.equal((await f.snapshot()).items[0].library, 'groups/1234');
    f.main.ZoteroPane.getSelectedItems = () => [f.pdf]; f.pdf.parentItemID = null;
    assert.match((await f.snapshot()).items[0].problem, /Standalone/);
    f.pdf.deleted = true;
    assert.match((await f.snapshot()).items[0].problem, /trash/);
});
test('GET endpoint checks client header and view; shutdown unregisters it', async () => {
    const f = await fixture(); assert.equal(f.endpoint.supportedMethods.join(','), 'GET');
    assert.equal((await f.request('auto', ''))[0], 403);
    assert.equal((await f.request('invalid'))[0], 400);
    assert.match((await f.snapshot('reader')).problem, /No attachment reader/);
    f.context.shutdown(); assert.equal(f.Zotero.Server.Endpoints['/api/paper-wiki/selection'], undefined);
});
