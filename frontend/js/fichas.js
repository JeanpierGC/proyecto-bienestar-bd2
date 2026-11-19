const fichasPage = new CrudPage({
  endpoint: "/fichas",
  idField: "codfic",
  entityName: "ficha psicológica",
  columnCount: 5,
  displayName: (f) => `la ficha de ${f.estudiante.apeest}`,
  searchText: (f) => `${f.estudiante.apeest} ${f.estudiante.nomest} ${f.estudiante.dniest} ${f.motfic}`,
  renderRow: (f) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-sm">${ui.initials(f.estudiante.nomest, f.estudiante.apeest)}</span>
        <div><strong>${ui.escape(sesion.nombre(f.estudiante))}</strong><small>DNI ${ui.escape(f.estudiante.dniest)}</small></div>
      </div>
    </td>
    <td>${ui.escape(f.motfic.length > 70 ? `${f.motfic.slice(0, 70)}…` : f.motfic)}
      <div class="text-muted small">${f.diagfic ? "Con diagnóstico" : "Diagnóstico pendiente"} · ${f.planfic ? "con plan" : "plan pendiente"}</div></td>
    <td>${ui.escape(`${f.responsable.nomper} ${f.responsable.apeper}`)}</td>
    <td class="text-nowrap">${ui.fecha(f.fechaper)}</td>
    <td>${ui.chip(f.estfic)}</td>`,
});

async function cargarListas() {
  try {
    const [estudiantes, personal] = await Promise.all([api.get("/estudiantes"), api.get("/personal")]);
    ui.fillSelect(document.getElementById("codest"), estudiantes, "codest", (e) => sesion.nombre(e), "Selecciona un estudiante");
    ui.fillSelect(document.getElementById("codperresp"), personal, "codper", (p) => `${p.apeper}, ${p.nomper} · ${p.cargoper}`, "Selecciona al responsable");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

cargarListas();
fichasPage.load();
fichasPage.openFromUrl();
