const requisitosPage = new CrudPage({
  endpoint: "/requisitos",
  idField: "codreq",
  entityName: "requisito",
  columnCount: 3,
  displayName: (r) => r.nomreq,
  searchText: (r) => `${r.nomreq} ${r.descreq ?? ""}`,
  renderRow: (r) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-square"><i class="bi bi-card-checklist"></i></span>
        <strong>${ui.escape(r.nomreq)}</strong>
      </div>
    </td>
    <td class="text-muted">${ui.escape(r.descreq ?? "Sin descripción")}</td>
    <td><span class="code-tag">#${r.codreq}</span></td>`,
});

requisitosPage.load();
requisitosPage.openFromUrl();
