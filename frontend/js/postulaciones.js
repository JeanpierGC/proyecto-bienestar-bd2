// Postulaciones (administración): registrar, evaluar, revisar documentos y otorgar la beca.
const boton = (accion, icono, titulo, clase = "") =>
  (id) => `<button class="btn-action ${clase}" data-action="${accion}" data-id="${id}" title="${titulo}"><i class="bi ${icono}"></i></button>`;

const botones = {
  evaluar: boton("eval", "bi-clipboard-check", "Evaluar"),
  documentos: boton("docs", "bi-folder2-open", "Documentos"),
  otorgar: boton("grant", "bi-award", "Otorgar beca"),
  eliminar: boton("delete", "bi-trash3", "Eliminar", "danger"),
};

class PostulacionesPage extends CrudPage {
  actionButtons(p) {
    const id = p.codpost;
    const otorgar = p.estpost === "APROBADA" && !p.otorgada ? botones.otorgar(id) : "";
    const eliminar = p.estpost === "REGISTRADA" ? botones.eliminar(id) : "";
    return `<td class="text-end text-nowrap">${botones.evaluar(id)}${botones.documentos(id)}${otorgar}${eliminar}</td>`;
  }

  onTableClick(event) {
    const clic = event.target.closest("button[data-action]");
    if (!clic) return;
    const postulacion = this.findItem(Number(clic.dataset.id));
    const acciones = {
      eval: () => evaluacion.abrir(postulacion),
      docs: () => documentos.abrir(postulacion),
      grant: () => otorgamiento.abrir(postulacion),
      delete: () => this.remove(postulacion.codpost),
    };
    acciones[clic.dataset.action]?.();
  }
}

const postulacionesPage = new PostulacionesPage({
  endpoint: "/postulaciones",
  idField: "codpost",
  entityName: "postulación",
  columnCount: 5,
  displayName: (p) => `la postulación de ${p.estudiante.apeest}`,
  searchText: (p) => `${p.estudiante.apeest} ${p.estudiante.nomest} ${p.estudiante.dniest} ${p.convocatoria.nomconv} ${p.convocatoria.beca.nombeca}`,
  renderRow: (p) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-sm">${ui.initials(p.estudiante.nomest, p.estudiante.apeest)}</span>
        <div><strong>${ui.escape(sesion.nombre(p.estudiante))}</strong><small>DNI ${ui.escape(p.estudiante.dniest)}</small></div>
      </div>
    </td>
    <td><strong>${ui.escape(p.convocatoria.nomconv)}</strong><div class="text-muted small">${ui.escape(p.convocatoria.beca.nombeca)}</div></td>
    <td>Promedio <strong>${p.prompost}</strong><div class="text-muted small">Ingreso S/ ${p.ingfampost}</div></td>
    <td>${ui.chip(p.estpost)}
      ${p.otorgada ? '<span class="soft-badge"><i class="bi bi-patch-check"></i> Beca otorgada</span>' : ""}
      <div class="text-muted small">${ui.escape(p.otorgada ? "Beca otorgada" : p.mensajeestado ?? "")}</div></td>
    <td>${p.puntpost != null ? `<strong>${p.puntpost} pts</strong>` : "—"}
      <div class="text-muted small">${p.evaluador ? ui.escape(`${p.evaluador.nomper} ${p.evaluador.apeper}`) : "Sin evaluar"}</div></td>`,
});

// Evaluación: procedimiento p02.
const evaluacion = {
  modal: new bootstrap.Modal(document.getElementById("modalevaluar")),
  formulario: document.getElementById("formevaluar"),
  codpost: null,

  abrir(p) {
    this.codpost = p.codpost;
    this.formulario.reset();
    this.formulario.classList.remove("was-validated");
    ui.clearAlert("alertasevaluar");
    document.getElementById("resumenevaluar").textContent = `${sesion.nombre(p.estudiante)} · ${p.convocatoria.nomconv}`;
    if (p.puntpost != null) this.formulario.puntpost.value = p.puntpost;
    if (p.evaluador) this.formulario.codpereval.value = p.evaluador.codper;
    this.modal.show();
  },

  async guardar(event) {
    event.preventDefault();
    if (!this.formulario.checkValidity()) return this.formulario.classList.add("was-validated");
    try {
      await api.put(`/postulaciones/${this.codpost}/evaluacion`, ui.formData(this.formulario));
      this.modal.hide();
      ui.toast("Evaluación guardada");
      postulacionesPage.load();
    } catch (error) {
      ui.alert(error.message, "danger", "alertasevaluar");
    }
  },
};

// Revisión de los documentos presentados por el estudiante.
const documentos = {
  modal: new bootstrap.Modal(document.getElementById("modaldocs")),
  contenedor: document.getElementById("listadocs"),
  codpost: null,

  async abrir(p) {
    this.codpost = p.codpost;
    ui.clearAlert("alertasdocs");
    document.getElementById("resumendocs").textContent = `${sesion.nombre(p.estudiante)} · ${p.convocatoria.beca.nombeca}`;
    await this.pintar();
    this.modal.show();
  },

  async pintar() {
    try {
      const requisitos = await api.get(`/postulaciones/${this.codpost}/requisitos`);
      this.contenedor.innerHTML = requisitos.map((r) => this.fila(r)).join("")
        || `<p class="text-muted mb-0">Esta beca no pide documentos.</p>`;
    } catch (error) {
      ui.alert(error.message, "danger", "alertasdocs");
    }
  },

  fila(r) {
    const opciones = ["PENDIENTE", "APROBADO", "OBSERVADO", "RECHAZADO"]
      .map((e) => `<option value="${e}" ${e === r.estdoc ? "selected" : ""}>${e.charAt(0) + e.slice(1).toLowerCase()}</option>`).join("");
    const presentado = r.estdoc ? `Presentado el ${ui.fecha(r.fechpres)}` : "No presentado";
    return `
      <div class="tarjeta-seguimiento mb-2" data-codreq="${r.codreq}">
        <div class="d-flex justify-content-between"><strong>${ui.escape(r.nomreq)}</strong><small class="text-muted">${presentado}</small></div>
        <div class="row g-2 mt-1">
          <div class="col-md-4"><select class="form-select form-select-sm" name="estdoc" aria-label="Estado del documento">${opciones}</select></div>
          <div class="col-md-5"><input class="form-control form-control-sm" name="obsdoc" maxlength="255" placeholder="Observación" value="${ui.escape(r.obsdoc ?? "")}"></div>
          <div class="col-md-3 d-flex gap-1">
            <button class="btn btn-primary btn-sm flex-grow-1" data-guardar>Guardar</button>
            ${r.estdoc ? '<button class="btn btn-ghost btn-sm" data-quitar title="Quitar documento"><i class="bi bi-trash3"></i></button>' : ""}
          </div>
        </div>
      </div>`;
  },

  async accion(event) {
    const fila = event.target.closest("[data-codreq]");
    const guardar = event.target.closest("[data-guardar]");
    const quitar = event.target.closest("[data-quitar]");
    if (!fila || !(guardar || quitar)) return;
    const ruta = `/postulaciones/${this.codpost}/requisitos/${fila.dataset.codreq}`;
    try {
      if (guardar) {
        await api.put(ruta, ui.formData(fila.querySelector(".row")) );
        ui.toast("Documento actualizado");
      } else {
        await api.delete(ruta);
        ui.toast("Documento quitado");
      }
      await this.pintar();
    } catch (error) {
      ui.alert(error.message, "danger", "alertasdocs");
    }
  },
};

// Otorgamiento de la beca: procedimiento p03.
const otorgamiento = {
  modal: new bootstrap.Modal(document.getElementById("modalotorgar")),
  formulario: document.getElementById("formotorgar"),
  codpost: null,

  abrir(p) {
    this.codpost = p.codpost;
    ui.clearAlert("alertasotorgar");
    this.formulario.classList.remove("was-validated");
    document.getElementById("resumenotorgar").textContent = `${sesion.nombre(p.estudiante)} · ${p.convocatoria.beca.nombeca}`;
    const inicio = new Date();
    const fin = new Date(inicio);
    fin.setMonth(fin.getMonth() + 6);
    this.formulario.fechiniotor.value = inicio.toISOString().slice(0, 10);
    this.formulario.fechfinotor.value = fin.toISOString().slice(0, 10);
    this.modal.show();
  },

  async guardar(event) {
    event.preventDefault();
    if (!this.formulario.checkValidity()) return this.formulario.classList.add("was-validated");
    try {
      await api.post("/becasotorgadas", { ...ui.formData(this.formulario), codpost: this.codpost });
      this.modal.hide();
      ui.toast("Beca otorgada");
      postulacionesPage.load();
    } catch (error) {
      ui.alert(error.message, "danger", "alertasotorgar");
    }
  },
};

evaluacion.formulario.addEventListener("submit", (e) => evaluacion.guardar(e));
otorgamiento.formulario.addEventListener("submit", (e) => otorgamiento.guardar(e));
documentos.contenedor.addEventListener("click", (e) => documentos.accion(e));

const filtroEstado = document.getElementById("filtro-estado");
const filtroConvocatoria = document.getElementById("filtro-convocatoria");
const aplicarFiltros = () => postulacionesPage.setFilter({ estpost: filtroEstado.value, codconv: filtroConvocatoria.value });
filtroEstado.addEventListener("change", aplicarFiltros);
filtroConvocatoria.addEventListener("change", aplicarFiltros);

async function cargarListas() {
  try {
    const [estudiantes, convocatorias, personal] = await Promise.all([api.get("/estudiantes"), api.get("/convocatorias"), api.get("/personal")]);
    ui.fillSelect(document.getElementById("codest"), estudiantes, "codest", (e) => sesion.nombre(e), "Selecciona un estudiante");
    ui.fillSelect(filtroConvocatoria, convocatorias, "codconv", (c) => c.nomconv, "Todas las convocatorias");
    const abiertas = convocatorias.filter((c) => c.estconv === "ABIERTA");
    ui.fillSelect(document.getElementById("codconv"), abiertas, "codconv", (c) => `${c.nomconv} (${c.perioconv})`, "Selecciona una convocatoria");
    ui.fillSelect(evaluacion.formulario.codpereval, personal, "codper", (p) => `${p.apeper}, ${p.nomper} · ${p.cargoper}`, "Selecciona al evaluador");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

cargarListas();
postulacionesPage.load();
postulacionesPage.openFromUrl();
