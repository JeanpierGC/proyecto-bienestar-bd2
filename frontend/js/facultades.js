const facultadesPage = new CrudPage({
  endpoint: "/facultades",
  idField: "codfac",
  entityName: "facultad",
  columnCount: 2,
  displayName: (f) => f.nomfac,
  searchText: (f) => f.nomfac,
  renderRow: (f) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-square"><i class="bi bi-building"></i></span>
        <strong>${ui.escape(f.nomfac)}</strong>
      </div>
    </td>
    <td><span class="code-tag">#${f.codfac}</span></td>`,
});

facultadesPage.load();
facultadesPage.openFromUrl();
