// Atenciones (administración): registrar con p05 y llevar el seguimiento de los casos que lo requieren.
class AtencionesPage extends CrudPage {
  actionButtons(a) {
    if (!a.reqseg) return `<td class="text-end text-muted small">Sin seguimiento</td>`;
    return `<td class="text-end text-nowrap">
      <button class="btn-action" data-action="seg" data-id="${a.codaten}" title="Seguimiento del caso"><i class="bi bi-activity"></i></button></td>`;
  }

  onTableClick(event) {
    const clic = event.target.closest('button[data-action="seg"]');
    if (clic) seguimiento.abrir(this.findItem(Number(clic.dataset.id)));
  }

  persist(payload) {
    return super.persist({ ...payload, reqseg: payload.reqseg === "1" });
  }

  // Cada fila muestra el nivel de vigilancia del estudiante, que calcula la función f5.
  async render() {
    super.render();
    for (const a of this.visibleItems()) {
      const celda = document.querySelector(`[data-riesgo="${a.codaten}"]`);
      if (!celda) continue;
      try {
        celda.textContent = (await api.get(`/atenciones/riesgo/${a.cita.estudiante.codest}`)).nivel;
      } catch {
        celda.textContent = "";
      }
    }
  }
}

const atencionesPage = new AtencionesPage({
  endpoint: "/atenciones",
  idField: "codaten",
  entityName: "atención",
  columnCount: 5,
  displayName: (a) => `la atención de ${a.cita.estudiante.apeest}`,
  searchText: (a) => `${a.cita.estudiante.apeest} ${a.cita.estudiante.nomest} ${a.cita.estudiante.dniest} ${a.nivelaten} ${a.resumaten}`,
  renderRow: (a) => `
    <td class="text-nowrap"><strong>${ui.fecha(a.cita.fechcita)}</strong><div class="text-muted small">${a.cita.horacita.slice(0, 5)} h</div></td>
    <td>
      <div class="cell-main">
        <span class="avatar avatar-sm">${ui.initials(a.cita.estudiante.nomest, a.cita.estudiante.apeest)}</span>
        <div><strong>${ui.escape(sesion.nombre(a.cita.estudiante))}</strong>
          <small data-riesgo="${a.codaten}"></small></div>
      </div>
    </td>
    <td>${ui.escape(`${a.cita.personal.nomper} ${a.cita.personal.apeper}`)}</td>
    <td>${ui.chip(a.nivelaten)}<div class="text-muted small">${ui.escape(a.resumaten.length > 60 ? `${a.resumaten.slice(0, 60)}…` : a.resumaten)}</div></td>
    <td>${a.reqseg ? `<span class="soft-badge"><i class="bi bi-activity"></i> ${ui.plural(a.cantseguimientos, "seguimiento")}</span>` : '<span class="text-muted small">No requiere</span>'}</td>`,
});

// Seguimiento de un caso: línea de tiempo y formulario para agregar o editar sesiones.
const seguimiento = {
  modal: new bootstrap.Modal(document.getElementById("modalseg")),
  formulario: document.getElementById("formseg"),
  lista: document.getElementById("listaseg"),
  atencion: null,
  items: [],
  editando: null,

  async abrir(atencion) {
    this.atencion = atencion;
    ui.clearAlert("alertasseg");
    document.getElementById("resumenseg").textContent =
      `${sesion.nombre(atencion.cita.estudiante)} · nivel ${atencion.nivelaten.toLowerCase()} · ${ui.fecha(atencion.cita.fechcita)}`;
    this.limpiar();
    await this.pintar();
    this.modal.show();
  },

  limpiar() {
    this.editando = null;
    this.formulario.reset();
    this.formulario.classList.remove("was-validated");
    this.formulario.fechseg.value = new Date().toISOString().slice(0, 10);
    document.getElementById("tituloformseg").textContent = "Registrar seguimiento";
  },

  async pintar() {
    try {
      this.items = await api.get(`/seguimientoscaso?codaten=${this.atencion.codaten}`);
      this.lista.innerHTML = linea.html(this.items, true);
    } catch (error) {
      ui.alert(error.message, "danger", "alertasseg");
    }
  },

  editar(codseg) {
    const item = this.items.find((s) => s.codseg === codseg);
    this.editando = codseg;
    ui.fillForm(this.formulario, item);
    document.getElementById("tituloformseg").textContent = "Editar seguimiento";
  },

  async ejecutar(accion, mensaje) {
    ui.clearAlert("alertasseg");
    try {
      await accion();
      ui.toast(mensaje);
      await atencionesPage.load();
      this.atencion = atencionesPage.findItem(this.atencion.codaten) ?? this.atencion;
      await this.pintar();
      return true;
    } catch (error) {
      ui.alert(error.message, "danger", "alertasseg");
      return false;
    }
  },

  async guardar(event) {
    event.preventDefault();
    if (!this.formulario.checkValidity()) return this.formulario.classList.add("was-validated");
    const datos = ui.formData(this.formulario);
    const accion = this.editando === null
      ? () => api.post("/seguimientoscaso", { ...datos, codaten: this.atencion.codaten })
      : () => api.put(`/seguimientoscaso/${this.editando}`, datos);
    const guardado = await this.ejecutar(accion, this.editando === null ? "Seguimiento registrado" : "Seguimiento actualizado");
    if (guardado) this.limpiar();
  },
};

seguimiento.formulario.addEventListener("submit", (e) => seguimiento.guardar(e));
document.getElementById("cancelaredicion").addEventListener("click", () => seguimiento.limpiar());
seguimiento.lista.addEventListener("click", (event) => {
  const editar = event.target.closest("[data-editarseg]");
  const quitar = event.target.closest("[data-quitarseg]");
  if (editar) seguimiento.editar(Number(editar.dataset.editarseg));
  if (quitar) seguimiento.ejecutar(() => api.delete(`/seguimientoscaso/${quitar.dataset.quitarseg}`), "Seguimiento eliminado");
});

// Nueva atención: solo citas programadas.
async function cargarCitas() {
  try {
    const citas = await api.get("/citas?estcita=PROGRAMADA");
    ui.fillSelect(document.getElementById("codcita"), citas, "codcita",
      (c) => `${ui.fecha(c.fechcita)} ${c.horacita.slice(0, 5)} · ${sesion.nombre(c.estudiante)}`, "Selecciona una cita programada");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

document.getElementById("btn-nuevo").addEventListener("click", cargarCitas);
cargarCitas();
atencionesPage.load();
atencionesPage.openFromUrl();
