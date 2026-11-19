// Seguimiento de los casos del estudiante: nivel de vigilancia (función f5) y línea de tiempo.
const selector = document.getElementById("estudiante");
const lista = document.getElementById("lista");
const contador = document.getElementById("contador");

async function tarjeta(a) {
  let seguimientos = [];
  try {
    seguimientos = await api.get(`/seguimientoscaso?codaten=${a.codaten}`);
  } catch (error) {
    ui.toast(error.message, "danger");
  }
  return `
    <article class="card-app">
      <div class="card-app-header">
        <div><h2>Atención del ${ui.fecha(a.cita.fechcita)}</h2>
          <p>${ui.escape(`${a.cita.personal.nomper} ${a.cita.personal.apeper}`)}</p></div>
        ${ui.chip(a.nivelaten)}
      </div>
      <div class="card-app-body">
        ${a.recomaten ? `<p class="mb-3"><strong>Recomendación:</strong> ${ui.escape(a.recomaten)}</p>` : ""}
        <h3 class="form-section-title">Seguimiento</h3>
        ${linea.html(seguimientos)}
      </div>
    </article>`;
}

async function cargar(codest) {
  if (!codest) {
    contador.textContent = "";
    lista.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi bi-person"></i></div><h3>Elige tu perfil</h3><p>Selecciona al estudiante para ver el seguimiento de sus casos.</p></div>`;
    return;
  }
  lista.innerHTML = `<div class="text-center py-5"><div class="spinner-border text-primary"></div></div>`;
  try {
    const [atenciones, riesgo] = await Promise.all([api.get(`/atenciones?codest=${codest}`), api.get(`/atenciones/riesgo/${codest}`)]);
    const propias = atenciones.filter((a) => a.cita.estudiante.codest === codest && a.reqseg);
    contador.textContent = riesgo.nivel;
    lista.innerHTML = propias.length
      ? (await Promise.all(propias.map(tarjeta))).join("")
      : `<div class="empty-state"><div class="empty-icon"><i class="bi bi-activity"></i></div><h3>Sin casos en seguimiento</h3><p>Cuando una atención requiera seguimiento, su avance aparecerá aquí.</p></div>`;
  } catch (error) {
    lista.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi bi-wifi-off"></i></div><h3>No se pudieron cargar</h3><p>${ui.escape(error.message)}</p></div>`;
  }
}

sesion.cargarselector(selector, cargar).catch((error) => ui.toast(error.message, "danger"));
