// Citas (administración): programar con el procedimiento p04, registrar la atención (p05), cancelar.
const boton = (accion, icono, titulo, clase = "") =>
  (id) => `<button class="btn-action ${clase}" data-action="${accion}" data-id="${id}" title="${titulo}"><i class="bi ${icono}"></i></button>`;

const botones = {
  atender: boton("attend", "bi-clipboard2-pulse", "Registrar atención"),
  cancelar: boton("cancel", "bi-x-circle", "Cancelar cita"),
  noasistio: boton("noshow", "bi-person-x", "Marcar como no asistió"),
  eliminar: boton("delete", "bi-trash3", "Eliminar", "danger"),
};

class CitasPage extends CrudPage {
  actionButtons(cita) {
    const id = cita.codcita;
    const programada = cita.estcita === "PROGRAMADA";
    const acciones = programada ? botones.atender(id) + botones.cancelar(id) + botones.noasistio(id) : "";
    const eliminar = cita.atencion ? "" : botones.eliminar(id);
    return `<td class="text-end text-nowrap">${acciones}${eliminar}</td>`;
  }

  onTableClick(event) {
    const clic = event.target.closest("button[data-action]");
    if (!clic) return;
    const cita = this.findItem(Number(clic.dataset.id));
    const acciones = {
      attend: () => atencion.abrir(cita),
      cancel: () => this.cambiarEstado(cita, "CANCELADA", "Cita cancelada"),
      noshow: () => this.cambiarEstado(cita, "NO_ASISTIO", "Marcada como no asistió"),
      delete: () => this.remove(cita.codcita),
    };
    acciones[clic.dataset.action]?.();
  }

  async cambiarEstado(cita, estcita, mensaje) {
    try {
      await api.put(`/citas/${cita.codcita}/estado`, { estcita });
      ui.toast(mensaje);
      await this.load();
    } catch (error) {
      ui.toast(error.message, "danger");
    }
  }
}

const citasPage = new CitasPage({
  endpoint: "/citas",
  idField: "codcita",
  entityName: "cita",
  columnCount: 5,
  displayName: (c) => `la cita de ${c.estudiante.apeest} del ${ui.fecha(c.fechcita)}`,
  searchText: (c) => `${c.estudiante.apeest} ${c.estudiante.nomest} ${c.estudiante.dniest} ${c.personal.apeper} ${c.personal.nomper}`,
  renderRow: (c) => `
    <td class="text-nowrap"><strong>${ui.fecha(c.fechcita)}</strong><div class="text-muted small">${c.horacita.slice(0, 5)} h</div></td>
    <td>
      <div class="cell-main">
        <span class="avatar avatar-sm">${ui.initials(c.estudiante.nomest, c.estudiante.apeest)}</span>
        <div><strong>${ui.escape(sesion.nombre(c.estudiante))}</strong><small>DNI ${ui.escape(c.estudiante.dniest)}</small></div>
      </div>
    </td>
    <td>${ui.escape(`${c.personal.nomper} ${c.personal.apeper}`)}<div class="text-muted small">${ui.escape(c.personal.cargoper)}</div></td>
    <td><span class="soft-badge neutral"><i class="bi ${c.modcita === "VIRTUAL" ? "bi-camera-video" : "bi-geo-alt"}"></i> ${c.modcita === "VIRTUAL" ? "Virtual" : "Presencial"}</span>
      <div class="text-muted small">${ui.escape(c.motcita ?? "Sin motivo")}</div></td>
    <td>${ui.chip(c.estcita)}${c.atencion ? `<div class="mt-1">${ui.chip(c.atencion.nivelaten)}</div>` : ""}</td>`,
});

// Registro de la atención de una cita: procedimiento p05.
const atencion = {
  modal: new bootstrap.Modal(document.getElementById("modalatencion")),
  formulario: document.getElementById("formatencion"),
  codcita: null,

  abrir(cita) {
    this.codcita = cita.codcita;
    this.formulario.reset();
    this.formulario.classList.remove("was-validated");
    ui.clearAlert("alertasatencion");
    document.getElementById("resumenatencion").textContent =
      `${sesion.nombre(cita.estudiante)} · ${ui.fecha(cita.fechcita)} ${cita.horacita.slice(0, 5)}`;
    this.modal.show();
  },

  async guardar(event) {
    event.preventDefault();
    if (!this.formulario.checkValidity()) return this.formulario.classList.add("was-validated");
    const datos = ui.formData(this.formulario);
    datos.reqseg = datos.reqseg === "1";
    try {
      await api.post("/atenciones", { ...datos, codcita: this.codcita });
      this.modal.hide();
      ui.toast("Atención registrada");
      citasPage.load();
    } catch (error) {
      ui.alert(error.message, "danger", "alertasatencion");
    }
  },
};

atencion.formulario.addEventListener("submit", (e) => atencion.guardar(e));

const filtroEstado = document.getElementById("filtro-estado");
filtroEstado.addEventListener("change", () => citasPage.setFilter({ estcita: filtroEstado.value }));

async function cargarListas() {
  try {
    const [estudiantes, personal] = await Promise.all([api.get("/estudiantes"), api.get("/personal")]);
    ui.fillSelect(document.getElementById("codest"), estudiantes, "codest", (e) => sesion.nombre(e), "Selecciona un estudiante");
    ui.fillSelect(document.getElementById("codper"), personal, "codper", (p) => `${p.apeper}, ${p.nomper} · ${p.servicio.nomserv}`, "Selecciona al profesional");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

document.getElementById("fechcita").min = new Date().toISOString().slice(0, 10);
cargarListas();
citasPage.load();
citasPage.openFromUrl();
