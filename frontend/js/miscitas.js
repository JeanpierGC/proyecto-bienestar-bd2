// Citas del estudiante: solicitar una nueva (procedimiento p04) y cancelar las programadas.
const selector = document.getElementById("estudiante");
const lista = document.getElementById("lista");
const contador = document.getElementById("contador");
const modal = new bootstrap.Modal(document.getElementById("modalcita"));
const formulario = document.getElementById("formcita");
const servicioElegido = document.getElementById("servicio");
const profesional = document.getElementById("codper");
let personal = [];

function pintarProfesionales() {
  const delServicio = personal.filter((p) => String(p.codserv) === servicioElegido.value);
  ui.fillSelect(profesional, delServicio, "codper", (p) => `${p.nomper} ${p.apeper} · ${p.cargoper}`, "Selecciona al profesional");
}

function tarjeta(c) {
  const cancelar = c.estcita === "PROGRAMADA"
    ? `<button class="btn btn-ghost btn-sm" data-cancelar="${c.codcita}"><i class="bi bi-x-circle"></i> Cancelar</button>` : "";
  return `
    <div class="list-row">
      <div class="text-center" style="min-width: 70px"><strong class="d-block">${ui.fecha(c.fechcita).slice(0, 5)}</strong><small class="text-muted">${c.horacita.slice(0, 5)} h</small></div>
      <div class="flex-grow-1">
        <strong>${ui.escape(`${c.personal.nomper} ${c.personal.apeper}`)}</strong>
        <small class="d-block text-muted">${ui.escape(c.personal.cargoper)} · ${c.modcita === "VIRTUAL" ? "Virtual" : "Presencial"}${c.motcita ? ` · ${ui.escape(c.motcita)}` : ""}</small>
      </div>
      ${ui.chip(c.estcita)}${cancelar}
    </div>`;
}

async function cargar(codest) {
  document.getElementById("nuevacita").disabled = !codest;
  if (!codest) {
    contador.textContent = "";
    lista.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi bi-person"></i></div><h3>Elige tu perfil</h3><p>Selecciona al estudiante para ver sus citas.</p></div>`;
    return;
  }
  try {
    const citas = await api.get(`/citas?codest=${codest}`);
    contador.textContent = ui.plural(citas.length, "cita");
    lista.innerHTML = citas.length
      ? `<div class="card-app"><div class="card-app-body py-2">${citas.map(tarjeta).join("")}</div></div>`
      : `<div class="empty-state"><div class="empty-icon"><i class="bi bi-calendar-event"></i></div><h3>Aún no tienes citas</h3><p>Solicita tu primera cita con el botón de arriba.</p></div>`;
  } catch (error) {
    lista.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi bi-wifi-off"></i></div><h3>No se pudieron cargar</h3><p>${ui.escape(error.message)}</p></div>`;
  }
}

function abrirNueva(codserv) {
  formulario.reset();
  formulario.classList.remove("was-validated");
  ui.clearAlert("alertascita");
  if (codserv) servicioElegido.value = codserv;
  pintarProfesionales();
  modal.show();
}

async function solicitar(event) {
  event.preventDefault();
  if (!formulario.checkValidity()) return formulario.classList.add("was-validated");
  try {
    const datos = ui.formData(formulario);
    delete datos.servicio;
    await api.post("/citas", { ...datos, codest: Number(selector.value) });
    modal.hide();
    ui.toast("Cita solicitada");
    cargar(Number(selector.value));
  } catch (error) {
    ui.alert(error.message, "danger", "alertascita");
  }
}

lista.addEventListener("click", async (event) => {
  const cancelar = event.target.closest("[data-cancelar]");
  if (!cancelar) return;
  const confirmado = await ui.confirm({ title: "¿Cancelar la cita?", message: "La cita quedará cancelada y el horario se libera.", confirmText: "Cancelar cita" });
  if (!confirmado) return;
  try {
    await api.put(`/citas/${cancelar.dataset.cancelar}/estado`, { estcita: "CANCELADA" });
    ui.toast("Cita cancelada");
    cargar(Number(selector.value));
  } catch (error) {
    ui.toast(error.message, "danger");
  }
});

servicioElegido.addEventListener("change", pintarProfesionales);
formulario.addEventListener("submit", solicitar);
document.getElementById("nuevacita").addEventListener("click", () => abrirNueva());
document.getElementById("fechcita").min = new Date().toISOString().slice(0, 10);

async function iniciar() {
  try {
    const [servicios, listaPersonal] = await Promise.all([api.get("/servicios"), api.get("/personal")]);
    personal = listaPersonal;
    ui.fillSelect(servicioElegido, servicios, "codserv", (s) => s.nomserv, "Selecciona un servicio");
    await sesion.cargarselector(selector, cargar);
    const params = new URLSearchParams(location.search);
    if (params.has("nuevo") && selector.value) abrirNueva(params.get("serv"));
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

iniciar();
