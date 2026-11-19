// Becas del estudiante: vigencia, estado y seguimiento académico.
const selector = document.getElementById("estudiante");
const lista = document.getElementById("lista");
const contador = document.getElementById("contador");

async function tarjeta(o) {
  let seguimientos = "";
  try {
    const filas = await api.get(`/becasotorgadas/${o.codotor}/seguimientos`);
    seguimientos = filas.map((s) => `
      <div class="list-row">
        <div class="flex-grow-1"><strong>${ui.fecha(s.fechsegb)}</strong> · promedio ${s.promsegb}
          <small class="text-muted d-block">${ui.escape(s.obssegb ?? "")}</small></div>
        ${s.cumsegb ? '<span class="chip c-ok">Cumple</span>' : '<span class="chip c-bad">No cumple</span>'}
      </div>`).join("") || `<p class="text-muted mb-0">Aún no hay seguimientos registrados.</p>`;
  } catch (error) {
    seguimientos = `<p class="text-danger mb-0">${ui.escape(error.message)}</p>`;
  }
  const { beca, nomconv } = { beca: o.postulacion.convocatoria.beca, nomconv: o.postulacion.convocatoria.nomconv };
  return `
    <article class="card-app">
      <div class="card-app-header">
        <div><h2>${ui.escape(beca.nombeca)}</h2><p>${ui.escape(nomconv)} · ${beca.porcbeca}% de cobertura</p></div>
        ${ui.chip(o.estotor)}
      </div>
      <div class="card-app-body">
        <p class="mb-1"><i class="bi bi-calendar-range"></i> Vigente del <strong>${ui.fecha(o.fechiniotor)}</strong> al <strong>${ui.fecha(o.fechfinotor)}</strong></p>
        <p class="small text-muted">${o.promedioseguimiento != null ? `Promedio de seguimiento: <strong>${o.promedioseguimiento}</strong>` : "Sin promedio de seguimiento todavía"}</p>
        <h3 class="form-section-title">Seguimiento</h3>
        ${seguimientos}
      </div>
    </article>`;
}

async function cargar(codest) {
  if (!codest) {
    contador.textContent = "";
    lista.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi bi-person"></i></div><h3>Elige tu perfil</h3><p>Selecciona al estudiante para ver sus becas.</p></div>`;
    return;
  }
  lista.innerHTML = `<div class="text-center py-5"><div class="spinner-border text-primary"></div></div>`;
  try {
    const propias = await api.get(`/becasotorgadas?codest=${codest}`);
    contador.textContent = ui.plural(propias.length, "beca");
    lista.innerHTML = propias.length
      ? (await Promise.all(propias.map(tarjeta))).join("")
      : `<div class="empty-state"><div class="empty-icon"><i class="bi bi-inbox"></i></div><h3>Todavía no tienes becas</h3><p>Cuando una postulación aprobada se otorgue, aparecerá aquí.</p><a class="btn btn-primary" href="mispostulaciones.html">Ver mis postulaciones</a></div>`;
  } catch (error) {
    lista.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi bi-wifi-off"></i></div><h3>No se pudieron cargar</h3><p>${ui.escape(error.message)}</p></div>`;
  }
}

sesion.cargarselector(selector, cargar).catch((error) => ui.toast(error.message, "danger"));
