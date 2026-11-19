// Inicio del estudiante: resumen y avisos armados solo con sus propios datos.
const codest = sesion.codest();

function hoy() {
  const d = new Date();
  const dos = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${dos(d.getMonth() + 1)}-${dos(d.getDate())}`;
}

function dato(clave, valor) {
  document.querySelector(`[data-stat="${clave}"]`).textContent = valor;
}

function aviso({ icono, color, titulo, detalle, enlace, extra = "" }) {
  return `
    <a class="list-row text-reset text-decoration-none" href="${enlace}">
      <span class="stat-icon ${color}"><i class="bi ${icono}"></i></span>
      <div class="list-text">
        <strong>${ui.escape(titulo)}</strong>
        <small class="d-block">${ui.escape(detalle)}</small>
      </div>
      ${extra}
    </a>`;
}

function avisosPostulaciones(postulaciones) {
  return postulaciones.map((p) => ({
    orden: p.fechpost,
    html: aviso({
      icono: "bi-file-earmark-text",
      color: "i-brand",
      titulo: `Postulación a ${p.convocatoria.beca.nombeca}`,
      detalle: p.mensajeestado || `Registrada el ${ui.fecha(p.fechpost)}`,
      enlace: "mispostulaciones.html",
      extra: ui.chip(p.estpost),
    }),
  }));
}

function avisosBecas(otorgadas) {
  return otorgadas
    .filter((o) => o.estotor === "VIGENTE")
    .map((o) => ({
      orden: o.fechotor,
      html: aviso({
        icono: "bi-patch-check",
        color: "i-ok",
        titulo: `Tu ${o.postulacion.convocatoria.beca.nombeca} está vigente`,
        detalle: `Del ${ui.fecha(o.fechiniotor)} al ${ui.fecha(o.fechfinotor)}`,
        enlace: "misbecas.html",
      }),
    }));
}

function avisosCitas(citas) {
  return citas
    .filter((c) => c.estcita === "PROGRAMADA" && c.fechcita >= hoy())
    .map((c) => ({
      orden: c.fechcita,
      html: aviso({
        icono: "bi-calendar-event",
        color: "i-info",
        titulo: `Cita el ${ui.fecha(c.fechcita)} a las ${c.horacita.slice(0, 5)}`,
        detalle: `Con ${c.personal.nomper} ${c.personal.apeper} · ${c.modcita === "VIRTUAL" ? "Virtual" : "Presencial"}`,
        enlace: "miscitas.html",
      }),
    }));
}

async function avisosSeguimiento(atenciones) {
  const conseguimiento = atenciones.filter((a) => a.reqseg);
  const listas = await Promise.all(conseguimiento.map((a) => api.get(`/seguimientoscaso?codaten=${a.codaten}`)));
  return listas
    .flat()
    .filter((s) => s.fechprox && s.fechprox >= hoy() && s.estseg !== "CERRADO")
    .map((s) => ({
      orden: s.fechprox,
      html: aviso({
        icono: "bi-activity",
        color: "i-gold",
        titulo: `Próxima sesión de seguimiento: ${ui.fecha(s.fechprox)}`,
        detalle: s.descseg,
        enlace: "miseguimiento.html",
      }),
    }));
}

async function cargar() {
  const nombre = (sesion.nombre().split(",")[1] || sesion.nombre()).trim();
  document.querySelector(".page-head h1").textContent = `Hola, ${nombre}`;
  const lista = document.getElementById("listaavisos");
  lista.innerHTML = `<div class="text-center py-4"><div class="spinner-border text-primary"></div></div>`;
  try {
    const [postulaciones, conteo, otorgadas, citas, atenciones, riesgo] = await Promise.all([
      api.get(`/postulaciones?codest=${codest}`),
      api.get(`/postulaciones/conteo/${codest}`),
      api.get(`/becasotorgadas?codest=${codest}`),
      api.get(`/citas?codest=${codest}`),
      api.get(`/atenciones?codest=${codest}`),
      api.get(`/atenciones/riesgo/${codest}`),
    ]);
    const proximas = citas.filter((c) => c.estcita === "PROGRAMADA" && c.fechcita >= hoy()).sort((a, b) => a.fechcita.localeCompare(b.fechcita));
    dato("postulaciones", conteo.cantidad);
    dato("becas", otorgadas.filter((o) => o.estotor === "VIGENTE").length);
    dato("cita", proximas.length ? ui.fecha(proximas[0].fechcita).slice(0, 5) : "—");
    dato("vigilancia", riesgo.nivel);

    const avisos = [
      ...avisosCitas(citas),
      ...(await avisosSeguimiento(atenciones)),
      ...avisosBecas(otorgadas),
      ...avisosPostulaciones(postulaciones),
    ];
    document.getElementById("contador").textContent = ui.plural(avisos.length, "aviso");
    lista.innerHTML = avisos.length
      ? avisos.map((a) => a.html).join("")
      : `<div class="empty-state"><div class="empty-icon"><i class="bi bi-bell"></i></div><h3>Sin avisos</h3><p>Cuando postules a una beca o pidas una cita, verás aquí su avance.</p></div>`;
  } catch (error) {
    lista.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi bi-wifi-off"></i></div><h3>No se pudo cargar</h3><p>${ui.escape(error.message)}</p></div>`;
  }
}

cargar();
