const serviciosPage = new CrudPage({
  endpoint: "/servicios",
  idField: "codserv",
  entityName: "servicio",
  columnCount: 3,
  displayName: (s) => s.nomserv,
  searchText: (s) => `${s.nomserv} ${s.descserv ?? ""}`,
  renderRow: (s) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-square"><i class="bi bi-heart-pulse"></i></span>
        <strong>${ui.escape(s.nomserv)}</strong>
      </div>
    </td>
    <td class="text-muted">${ui.escape(s.descserv ?? "Sin descripción")}</td>
    <td><span class="code-tag">#${s.codserv}</span></td>`,
});

serviciosPage.load();
serviciosPage.openFromUrl();
