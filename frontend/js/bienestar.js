// Servicios de bienestar universitario y el personal que los atiende.
const contenedor = document.getElementById("servicios");

function tarjeta(servicio, personal) {
  const equipo = personal.length
    ? personal.map((p) => `<div class="list-row"><span class="avatar avatar-sm">${ui.initials(p.nomper, p.apeper)}</span>
        <div><strong>${ui.escape(`${p.nomper} ${p.apeper}`)}</strong><small class="d-block text-muted">${ui.escape(p.cargoper)}</small></div></div>`).join("")
    : `<p class="text-muted mb-0">Aún no hay personal asignado.</p>`;
  return `
    <div class="col-md-6 col-xl-4">
      <article class="card-app h-100">
        <div class="card-app-body d-flex flex-column gap-2 h-100">
          <span class="avatar avatar-square"><i class="bi bi-heart-pulse"></i></span>
          <h3 class="h5 mb-0">${ui.escape(servicio.nomserv)}</h3>
          <p class="text-muted small mb-1">${ui.escape(servicio.descserv ?? "")}</p>
          ${equipo}
          <a class="btn btn-primary mt-auto" href="miscitas.html?nuevo&serv=${servicio.codserv}">Solicitar cita</a>
        </div>
      </article>
    </div>`;
}

async function iniciar() {
  try {
    const [servicios, personal] = await Promise.all([api.get("/servicios"), api.get("/personal")]);
    contenedor.innerHTML = servicios.map((s) => tarjeta(s, personal.filter((p) => p.codserv === s.codserv))).join("");
  } catch (error) {
    contenedor.innerHTML = `<div class="col-12"><div class="empty-state"><div class="empty-icon"><i class="bi bi-wifi-off"></i></div>
      <h3>No se pudieron cargar los servicios</h3><p>${ui.escape(error.message)}</p></div></div>`;
  }
}

iniciar();
