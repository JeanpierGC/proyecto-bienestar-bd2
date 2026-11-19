const personalPage = new CrudPage({
  endpoint: "/personal",
  idField: "codper",
  entityName: "personal",
  columnCount: 4,
  displayName: (p) => `${p.nomper} ${p.apeper}`,
  searchText: (p) => `${p.nomper} ${p.apeper} ${p.dniper} ${p.cargoper} ${p.servicio.nomserv}`,
  renderRow: (p) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-sm">${ui.initials(p.nomper, p.apeper)}</span>
        <div><strong>${ui.escape(`${p.apeper}, ${p.nomper}`)}</strong><small>${ui.escape(p.corrper)}</small></div>
      </div>
    </td>
    <td>${ui.escape(p.cargoper)}</td>
    <td><span class="soft-badge neutral"><i class="bi bi-heart-pulse"></i> ${ui.escape(p.servicio.nomserv)}</span></td>
    <td><span class="code-tag">DNI ${ui.escape(p.dniper)}</span></td>`,
});

async function cargarServicios() {
  try {
    const servicios = await api.get("/servicios");
    ui.fillSelect(document.getElementById("codserv"), servicios, "codserv", (s) => s.nomserv, "Selecciona un servicio");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

cargarServicios();
personalPage.load();
personalPage.openFromUrl();
