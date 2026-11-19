// Becas: tabla CRUD + ventana de detalle para administrar sus reglas y requisitos.
class BecasPage extends CrudPage {
  actionButtons(beca) {
    return `
      <td class="text-end text-nowrap">
        <button class="btn-action" data-action="detail" data-id="${beca.codbeca}" title="Reglas y requisitos">
          <i class="bi bi-list-check"></i></button>
        <button class="btn-action" data-action="edit" data-id="${beca.codbeca}" title="Editar">
          <i class="bi bi-pencil-square"></i></button>
        <button class="btn-action danger" data-action="delete" data-id="${beca.codbeca}" title="Eliminar">
          <i class="bi bi-trash3"></i></button>
      </td>`;
  }

  onTableClick(event) {
    const button = event.target.closest('button[data-action="detail"]');
    if (button) detalle.abrir(Number(button.dataset.id));
    else super.onTableClick(event);
  }
}

const becasPage = new BecasPage({
  endpoint: "/becas",
  idField: "codbeca",
  entityName: "beca",
  columnCount: 5,
  displayName: (b) => b.nombeca,
  searchText: (b) => `${b.nombeca} ${b.tipobeca}`,
  renderRow: (b) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-square"><i class="bi bi-award"></i></span>
        <div>
          <strong>${ui.escape(b.nombeca)}</strong>
          <div class="text-muted small">${ui.escape(b.tipobeca)}</div>
        </div>
      </div>
    </td>
    <td><strong>${b.porcbeca}%</strong></td>
    <td>
      <span class="soft-badge neutral"><i class="bi bi-card-checklist"></i> ${ui.plural(b.requisitos.length, "requisito")}</span>
      <span class="soft-badge neutral"><i class="bi bi-rulers"></i> ${ui.plural(b.reglas.length, "regla")}</span>
    </td>
    <td>${ui.chip(b.estbeca)}</td>
    <td><span class="code-tag">#${b.codbeca}</span></td>`,
});

// Ventana de detalle de una beca: reglas (alta y baja) y requisitos (conjunto completo).
const detalle = {
  modal: new bootstrap.Modal(document.getElementById("modaldetalle")),
  codbeca: null,
  requisitos: [],

  beca() {
    return becasPage.findItem(this.codbeca);
  },

  async abrir(codbeca) {
    this.codbeca = codbeca;
    ui.clearAlert("alertasdetalle");
    try {
      this.requisitos = await api.get("/requisitos");
    } catch (error) {
      ui.toast(error.message, "danger");
      return;
    }
    this.pintar();
    this.modal.show();
  },

  pintar() {
    const beca = this.beca();
    document.getElementById("detalletitulo").textContent = beca.nombeca;
    document.getElementById("detalleinfo").innerHTML = `
      ${ui.chip(beca.estbeca)}
      <span class="soft-badge">${beca.porcbeca}% de cobertura</span>
      <span class="soft-badge neutral">${ui.escape(beca.tipobeca)}</span>
      <p class="text-muted mt-2 mb-0">${ui.escape(beca.descbeca ?? "Sin descripción")}</p>`;
    this.pintarRequisitos(beca);
    this.pintarReglas(beca);
  },

  pintarRequisitos(beca) {
    const contenedor = document.getElementById("detallerequisitos");
    if (this.requisitos.length === 0) {
      contenedor.innerHTML = `<p class="text-muted mb-0">Aún no hay requisitos. Créalos en <a href="requisitos.html">Requisitos</a>.</p>`;
      return;
    }
    const asignados = new Set(beca.requisitos.map((r) => r.codreq));
    contenedor.innerHTML = this.requisitos
      .map(
        (r) => `
        <label class="list-row d-flex align-items-center gap-2">
          <input class="form-check-input me-2" type="checkbox" name="codreq" value="${r.codreq}" ${asignados.has(r.codreq) ? "checked" : ""}>
          <span>${ui.escape(r.nomreq)}</span>
        </label>`
      )
      .join("");
  },

  pintarReglas(beca) {
    const contenedor = document.getElementById("detallereglas");
    if (beca.reglas.length === 0) {
      contenedor.innerHTML = `<p class="text-muted mb-0">Esta beca no tiene reglas todavía.</p>`;
      return;
    }
    contenedor.innerHTML = beca.reglas
      .map(
        (r) => `
        <div class="list-row d-flex align-items-center gap-2">
          <div class="flex-grow-1">
            <strong>${ui.escape(r.nomreg)}</strong>
            <span class="code-tag">${ui.escape(r.opreg)} ${r.valreg}</span>
          </div>
          <button class="btn-action danger" data-regla="${r.codreg}" title="Quitar regla"><i class="bi bi-trash3"></i></button>
        </div>`
      )
      .join("");
  },

  // Recarga la tabla y vuelve a pintar el detalle con los datos actualizados.
  async refrescar() {
    await becasPage.load();
    this.pintar();
  },

  async guardarRequisitos() {
    const marcados = [...document.querySelectorAll("#detallerequisitos input:checked")].map((i) => Number(i.value));
    await this.ejecutar(() => api.put(`/becas/${this.codbeca}/requisitos`, { codreq: marcados }), "Requisitos guardados");
  },

  async agregarRegla(event) {
    event.preventDefault();
    const formulario = event.currentTarget;
    if (!formulario.checkValidity()) {
      formulario.classList.add("was-validated");
      return;
    }
    const datos = { ...ui.formData(formulario), codbeca: this.codbeca };
    const guardado = await this.ejecutar(() => api.post("/reglas", datos), "Regla agregada");
    if (guardado) {
      formulario.reset();
      formulario.classList.remove("was-validated");
    }
  },

  async quitarRegla(codreg) {
    await this.ejecutar(() => api.delete(`/reglas/${codreg}`), "Regla eliminada");
  },

  async ejecutar(accion, mensaje) {
    ui.clearAlert("alertasdetalle");
    try {
      await accion();
      ui.toast(mensaje);
      await this.refrescar();
      return true;
    } catch (error) {
      ui.alert(error.message, "danger", "alertasdetalle");
      return false;
    }
  },
};

document.getElementById("guardarrequisitos").addEventListener("click", () => detalle.guardarRequisitos());
document.getElementById("formregla").addEventListener("submit", (event) => detalle.agregarRegla(event));
document.getElementById("detallereglas").addEventListener("click", (event) => {
  const boton = event.target.closest("[data-regla]");
  if (boton) detalle.quitarRegla(Number(boton.dataset.regla));
});

becasPage.load();
becasPage.openFromUrl();
