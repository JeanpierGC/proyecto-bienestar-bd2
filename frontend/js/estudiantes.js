const estudiantesPage = new CrudPage({
  endpoint: "/estudiantes",
  idField: "codest",
  entityName: "estudiante",
  columnCount: 4,
  displayName: (e) => `${e.nomest} ${e.apeest}`,
  searchText: (e) => `${e.nomest} ${e.apeest} ${e.dniest} ${e.correst} ${e.escuela.nomesc}`,
  renderRow: (e) => `
    <td>
      <div class="cell-main">
        <span class="avatar">${ui.initials(e.nomest, e.apeest)}</span>
        <div>
          <strong>${ui.escape(`${e.apeest}, ${e.nomest}`)}</strong>
          <small>${ui.escape(e.correst)}</small>
        </div>
      </div>
    </td>
    <td><span class="code-tag">${ui.escape(e.dniest)}</span></td>
    <td><span class="soft-badge">Ciclo ${e.cicest}</span></td>
    <td>
      <div>${ui.escape(e.escuela.nomesc)}</div>
      <small class="text-muted">${ui.escape(e.escuela.facultad.nomfac)}</small>
    </td>`,
});

const filtroEscuela = document.getElementById("filtro-escuela");

async function cargarEscuelas() {
  try {
    const escuelas = await api.get("/escuelas");
    const nombre = (e) => `${e.nomesc} (${e.facultad.nomfac})`;
    ui.fillSelect(filtroEscuela, escuelas, "codesc", (e) => e.nomesc, "Todas las escuelas");
    ui.fillSelect(document.getElementById("codesc"), escuelas, "codesc", nombre, "Selecciona una escuela");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

filtroEscuela.addEventListener("change", () =>
  estudiantesPage.setFilter({ codesc: filtroEscuela.value })
);

cargarEscuelas();
estudiantesPage.load();
estudiantesPage.openFromUrl();
