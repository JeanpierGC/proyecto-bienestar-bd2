// Postulaciones del estudiante: avance, documentos que debe presentar y retiro de la postulación.
const selector = document.getElementById("estudiante");
const lista = document.getElementById("lista");
const contador = document.getElementById("contador");
let postulaciones = [];

function filaDocumento(codpost, requisito) {
  const estado = requisito.estdoc
    ? ui.chip(requisito.estdoc)
    : `<button class="btn btn-soft btn-sm" data-presentar="${requisito.codreq}" data-codpost="${codpost}">Presentar</button>`;
  const observacion = requisito.obsdoc ? `<small class="text-muted d-block">${ui.escape(requisito.obsdoc)}</small>` : "";
  return `<div class="list-row"><div class="flex-grow-1"><span>${ui.escape(requisito.nomreq)}</span>${observacion}</div>${estado}</div>`;
}

async function tarjeta(p) {
  let documentos = "";
  try {
    const requisitos = await api.get(`/postulaciones/${p.codpost}/requisitos`);
    documentos = requisitos.map((r) => filaDocumento(p.codpost, r)).join("") || `<p class="text-muted mb-0">Esta beca no pide documentos.</p>`;
  } catch (error) {
    documentos = `<p class="text-danger mb-0">${ui.escape(error.message)}</p>`;
  }
  const retirar = p.estpost === "REGISTRADA"
    ? `<button class="btn btn-ghost btn-sm" data-retirar="${p.codpost}"><i class="bi bi-x-circle"></i> Retirar postulación</button>` : "";
  const beca = p.otorgada
    ? `<a class="btn btn-primary btn-sm" href="misbecas.html"><i class="bi bi-patch-check"></i> Ver mi beca</a>` : "";
  return `
    <article class="card-app">
      <div class="card-app-header">
        <div><h2>${ui.escape(p.convocatoria.nomconv)}</h2><p>${ui.escape(p.convocatoria.beca.nombeca)} · postulaste el ${ui.fecha(p.fechpost)}</p></div>
        ${ui.chip(p.estpost)}
      </div>
      <div class="card-app-body">
        ${flujo.html(p)}
        <p class="mt-3 mb-1"><strong>${ui.escape(p.otorgada ? "¡Tu beca fue otorgada!" : p.mensajeestado ?? "")}</strong></p>
        <p class="small text-muted">Promedio ${p.prompost} · Ingreso familiar S/ ${p.ingfampost}${p.puntpost != null ? ` · Puntaje ${p.puntpost}` : ""}</p>
        <h3 class="form-section-title">Documentos</h3>
        ${documentos}
        <div class="d-flex gap-2 mt-3">${beca}${retirar}</div>
      </div>
    </article>`;
}

async function cargar(codest) {
  if (!codest) {
    contador.textContent = "";
    lista.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi bi-person"></i></div><h3>Elige tu perfil</h3><p>Selecciona al estudiante para ver sus postulaciones.</p></div>`;
    return;
  }
  lista.innerHTML = `<div class="text-center py-5"><div class="spinner-border text-primary"></div></div>`;
  try {
    const [datos, conteo] = await Promise.all([api.get(`/postulaciones?codest=${codest}`), api.get(`/postulaciones/conteo/${codest}`)]);
    postulaciones = datos;
    contador.textContent = ui.plural(conteo.cantidad, "postulación", "postulaciones");
    lista.innerHTML = postulaciones.length
      ? (await Promise.all(postulaciones.map(tarjeta))).join("")
      : `<div class="empty-state"><div class="empty-icon"><i class="bi bi-inbox"></i></div><h3>Aún no postulaste</h3><p>Revisa las becas disponibles y postula a una convocatoria abierta.</p><a class="btn btn-primary" href="catalogo.html">Ver becas</a></div>`;
  } catch (error) {
    lista.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi bi-wifi-off"></i></div><h3>No se pudieron cargar</h3><p>${ui.escape(error.message)}</p></div>`;
  }
}

lista.addEventListener("click", async (event) => {
  const presentar = event.target.closest("[data-presentar]");
  const retirar = event.target.closest("[data-retirar]");
  try {
    if (presentar) {
      await api.put(`/postulaciones/${presentar.dataset.codpost}/requisitos/${presentar.dataset.presentar}`, { estdoc: "PENDIENTE" });
      ui.toast("Documento presentado, queda pendiente de revisión");
    } else if (retirar) {
      const confirmado = await ui.confirm({ title: "¿Retirar la postulación?", message: "Se eliminará tu postulación y los documentos presentados.", confirmText: "Retirar" });
      if (!confirmado) return;
      await api.delete(`/postulaciones/${retirar.dataset.retirar}`);
      ui.toast("Postulación retirada");
    } else {
      return;
    }
    cargar(Number(selector.value));
  } catch (error) {
    ui.toast(error.message, "danger");
  }
});

sesion.cargarselector(selector, cargar).catch((error) => ui.toast(error.message, "danger"));
