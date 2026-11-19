const escuelasPage = new CrudPage({
  endpoint: "/escuelas",
  idField: "codesc",
  entityName: "escuela",
  columnCount: 3,
  displayName: (e) => e.nomesc,
  searchText: (e) => `${e.nomesc} ${e.facultad.nomfac}`,
  renderRow: (e) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-square"><i class="bi bi-mortarboard"></i></span>
        <strong>${ui.escape(e.nomesc)}</strong>
      </div>
    </td>
    <td><span class="soft-badge neutral"><i class="bi bi-building"></i> ${ui.escape(e.facultad.nomfac)}</span></td>
    <td><span class="code-tag">#${e.codesc}</span></td>`,
});

const filtroFacultad = document.getElementById("filtro-facultad");

async function cargarFacultades() {
  try {
    const facultades = await api.get("/facultades");
    const nombre = (f) => f.nomfac;
    ui.fillSelect(filtroFacultad, facultades, "codfac", nombre, "Todas las facultades");
    ui.fillSelect(document.getElementById("codfac"), facultades, "codfac", nombre, "Selecciona una facultad");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

filtroFacultad.addEventListener("change", () =>
  escuelasPage.setFilter({ codfac: filtroFacultad.value })
);

cargarFacultades();
escuelasPage.load();
escuelasPage.openFromUrl();
