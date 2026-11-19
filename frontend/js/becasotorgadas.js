// Becas otorgadas (administración): otorgar, seguimiento, cambio de estado y baja.
class BecasOtorgadasPage extends CrudPage {
  actionButtons(o) {
    return `
      <td class="text-end text-nowrap">
        <button class="btn-action" data-action="seg" data-id="${o.codotor}" title="Seguimiento y estado"><i class="bi bi-activity"></i></button>
        <button class="btn-action danger" data-action="delete" data-id="${o.codotor}" title="Eliminar"><i class="bi bi-trash3"></i></button>
      </td>`;
  }

  onTableClick(event) {
    const clic = event.target.closest("button[data-action]");
    if (!clic) return;
    const id = Number(clic.dataset.id);
    if (clic.dataset.action === "seg") seguimientos.abrir(this.findItem(id));
    else this.remove(id);
  }
}

const becasOtorgadasPage = new BecasOtorgadasPage({
  endpoint: "/becasotorgadas",
  idField: "codotor",
  entityName: "beca otorgada",
  columnCount: 4,
  displayName: (o) => `la beca otorgada a ${o.postulacion.estudiante.apeest}`,
  searchText: (o) => `${o.postulacion.estudiante.apeest} ${o.postulacion.estudiante.nomest} ${o.postulacion.convocatoria.beca.nombeca}`,
  renderRow: (o) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-sm">${ui.initials(o.postulacion.estudiante.nomest, o.postulacion.estudiante.apeest)}</span>
        <div><strong>${ui.escape(sesion.nombre(o.postulacion.estudiante))}</strong><small>DNI ${ui.escape(o.postulacion.estudiante.dniest)}</small></div>
      </div>
    </td>
    <td><strong>${ui.escape(o.postulacion.convocatoria.beca.nombeca)}</strong><div class="text-muted small">${ui.escape(o.postulacion.convocatoria.nomconv)}</div></td>
    <td class="text-nowrap">${ui.fecha(o.fechiniotor)} <i class="bi bi-arrow-right text-muted"></i> ${ui.fecha(o.fechfinotor)}</td>
    <td>${ui.chip(o.estotor)}
      <div class="text-muted small">${ui.plural(o.cantseguimientos, "seguimiento")}${o.promedioseguimiento != null ? ` · promedio ${o.promedioseguimiento}` : ""}</div></td>`,
});

// Seguimiento de una beca otorgada y cambio de su estado.
const seguimientos = {
  modal: new bootstrap.Modal(document.getElementById("modalseg")),
  formulario: document.getElementById("formseg"),
  lista: document.getElementById("listaseg"),
  otorgada: null,

  async abrir(otorgada) {
    this.otorgada = otorgada;
    this.formulario.reset();
    this.formulario.classList.remove("was-validated");
    this.formulario.fechsegb.value = new Date().toISOString().slice(0, 10);
    ui.clearAlert("alertasseg");
    document.getElementById("resumenseg").textContent =
      `${sesion.nombre(otorgada.postulacion.estudiante)} · ${otorgada.postulacion.convocatoria.beca.nombeca}`;
    document.getElementById("estadootor").value = otorgada.estotor;
    await this.pintar();
    this.modal.show();
  },

  async pintar() {
    try {
      const filas = await api.get(`/becasotorgadas/${this.otorgada.codotor}/seguimientos`);
      this.lista.innerHTML = filas.length
        ? filas.map((s) => this.tarjeta(s)).join("")
        : `<p class="text-muted mb-0">Todavía no hay seguimientos.</p>`;
    } catch (error) {
      ui.alert(error.message, "danger", "alertasseg");
    }
  },

  tarjeta(s) {
    const cumple = s.cumsegb ? '<span class="chip c-ok">Cumple</span>' : '<span class="chip c-bad">No cumple</span>';
    return `
      <div class="tarjeta-seguimiento mb-2 d-flex gap-3 align-items-start">
        <div class="flex-grow-1">
          <strong>${ui.fecha(s.fechsegb)}</strong> · promedio <strong>${s.promsegb}</strong> ${cumple}
          <div class="small text-muted">${ui.escape(s.obssegb ?? "Sin observaciones")} · ${ui.escape(`${s.responsable.nomper} ${s.responsable.apeper}`)}</div>
        </div>
        <button class="btn-action danger" data-quitarseg="${s.codsegb}" title="Eliminar seguimiento"><i class="bi bi-trash3"></i></button>
      </div>`;
  },

  async ejecutar(accion, mensaje) {
    ui.clearAlert("alertasseg");
    try {
      await accion();
      ui.toast(mensaje);
      await becasOtorgadasPage.load();
      this.otorgada = becasOtorgadasPage.findItem(this.otorgada.codotor) ?? this.otorgada;
      await this.pintar();
      return true;
    } catch (error) {
      ui.alert(error.message, "danger", "alertasseg");
      return false;
    }
  },

  async registrar(event) {
    event.preventDefault();
    if (!this.formulario.checkValidity()) return this.formulario.classList.add("was-validated");
    const datos = ui.formData(this.formulario);
    datos.cumsegb = datos.cumsegb === "1";
    const guardado = await this.ejecutar(() => api.post(`/becasotorgadas/${this.otorgada.codotor}/seguimientos`, datos), "Seguimiento registrado");
    if (guardado) {
      this.formulario.reset();
      this.formulario.classList.remove("was-validated");
      this.formulario.fechsegb.value = new Date().toISOString().slice(0, 10);
    }
  },

  cambiarestado() {
    const estotor = document.getElementById("estadootor").value;
    return this.ejecutar(() => api.put(`/becasotorgadas/${this.otorgada.codotor}/estado`, { estotor }), "Estado actualizado");
  },
};

seguimientos.formulario.addEventListener("submit", (e) => seguimientos.registrar(e));
document.getElementById("guardarestado").addEventListener("click", () => seguimientos.cambiarestado());
seguimientos.lista.addEventListener("click", (event) => {
  const quitar = event.target.closest("[data-quitarseg]");
  if (quitar) seguimientos.ejecutar(() => api.delete(`/becasotorgadas/${seguimientos.otorgada.codotor}/seguimientos/${quitar.dataset.quitarseg}`), "Seguimiento eliminado");
});

// Otorgar desde esta pantalla: solo postulaciones aprobadas que aún no tienen beca.
async function cargarAprobadas() {
  try {
    const aprobadas = (await api.get("/postulaciones?estpost=APROBADA")).filter((p) => !p.otorgada);
    ui.fillSelect(document.getElementById("codpost"), aprobadas, "codpost",
      (p) => `${sesion.nombre(p.estudiante)} · ${p.convocatoria.beca.nombeca}`, "Selecciona una postulación aprobada");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

async function cargarPersonal() {
  try {
    const personal = await api.get("/personal");
    ui.fillSelect(document.getElementById("codperresp"), personal, "codper", (p) => `${p.apeper}, ${p.nomper}`, "Responsable");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

document.getElementById("btn-nuevo").addEventListener("click", cargarAprobadas);
cargarPersonal();
cargarAprobadas();
becasOtorgadasPage.load();
becasOtorgadasPage.openFromUrl();
