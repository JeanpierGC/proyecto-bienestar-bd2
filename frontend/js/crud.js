// Comportamiento común de una pantalla CRUD: tabla con buscador + modal con formulario.
// Cada pantalla solo define qué columnas mostrar y qué endpoint usar.
class CrudPage {
  constructor({ endpoint, idField, entityName, columnCount, renderRow, displayName, searchText }) {
    this.endpoint = endpoint;
    this.idField = idField;
    this.entityName = entityName;
    this.colspan = columnCount + 1;
    this.renderRow = renderRow;
    this.displayName = displayName;
    this.searchText = searchText;
    this.items = [];
    this.searchTerm = "";
    this.filterQuery = "";
    this.editingId = null;

    this.tableBody = document.querySelector("#tabla tbody");
    this.counter = document.getElementById("contador");
    this.form = document.getElementById("formulario");
    this.modal = new bootstrap.Modal(document.getElementById("modal"));
    this.modalTitle = document.getElementById("modal-titulo");
    this.bindEvents();
  }

  bindEvents() {
    document.getElementById("btn-nuevo").addEventListener("click", () => this.openNew());
    this.form.addEventListener("submit", (event) => this.save(event));
    this.tableBody.addEventListener("click", (event) => this.onTableClick(event));
    document.getElementById("buscador").addEventListener("input", (event) => {
      this.searchTerm = ui.normalize(event.target.value.trim());
      this.render();
    });
  }

  // Abre el formulario directamente si la URL trae ?nuevo (atajo desde el panel principal).
  openFromUrl() {
    if (new URLSearchParams(location.search).has("nuevo")) this.openNew();
  }

  setFilter(params) {
    const query = new URLSearchParams(
      Object.entries(params).filter(([, value]) => value !== "" && value != null)
    ).toString();
    this.filterQuery = query ? `?${query}` : "";
    return this.load();
  }

  async load() {
    this.tableBody.innerHTML = ui.loadingRow(this.colspan);
    try {
      this.items = await api.get(this.endpoint + this.filterQuery);
      this.render();
    } catch (error) {
      this.tableBody.innerHTML = ui.stateRow(this.colspan, {
        icon: "bi-wifi-off",
        title: "No se pudieron cargar los datos",
        text: ui.escape(error.message),
      });
    }
  }

  visibleItems() {
    if (!this.searchTerm) return this.items;
    return this.items.filter((item) => ui.normalize(this.searchText(item)).includes(this.searchTerm));
  }

  render() {
    const visible = this.visibleItems();
    this.counter.textContent = ui.plural(visible.length, "registro");

    if (this.items.length === 0) {
      this.tableBody.innerHTML = ui.stateRow(this.colspan, {
        icon: "bi-inbox",
        title: "Todavía no hay registros",
        text: "Usa el botón <strong>Nuevo</strong> para agregar el primero.",
      });
      return;
    }
    if (visible.length === 0) {
      this.tableBody.innerHTML = ui.stateRow(this.colspan, {
        icon: "bi-search",
        title: "Sin resultados",
        text: "Prueba con otro término de búsqueda.",
      });
      return;
    }
    this.tableBody.innerHTML = visible
      .map((item) => `<tr>${this.renderRow(item)}${this.actionButtons(item)}</tr>`)
      .join("");
  }

  actionButtons(item) {
    const id = item[this.idField];
    return `
      <td class="text-end text-nowrap">
        <button class="btn-action" data-action="edit" data-id="${id}" title="Editar">
          <i class="bi bi-pencil-square"></i></button>
        <button class="btn-action danger" data-action="delete" data-id="${id}" title="Eliminar">
          <i class="bi bi-trash3"></i></button>
      </td>`;
  }

  onTableClick(event) {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    const id = Number(button.dataset.id);
    if (button.dataset.action === "edit") this.openEdit(id);
    else this.remove(id);
  }

  findItem(id) {
    return this.items.find((item) => item[this.idField] === id);
  }

  openNew() {
    this.editingId = null;
    this.form.reset();
    this.openModal(`Registrar ${this.entityName}`);
  }

  openEdit(id) {
    this.editingId = id;
    ui.fillForm(this.form, this.findItem(id));
    this.openModal(`Editar ${this.entityName}`);
  }

  openModal(title) {
    this.modalTitle.textContent = title;
    this.form.classList.remove("was-validated");
    ui.clearAlert();
    this.modal.show();
  }

  async save(event) {
    event.preventDefault();
    if (!this.form.checkValidity()) {
      this.form.classList.add("was-validated");
      return;
    }
    const submit = this.form.querySelector("[type=submit]");
    submit.disabled = true;
    try {
      const creating = this.editingId === null;
      await this.persist(ui.formData(this.form));
      this.modal.hide();
      ui.toast(creating ? "Registro creado correctamente" : "Cambios guardados correctamente");
      await this.load();
    } catch (error) {
      ui.alert(error.message);
    } finally {
      submit.disabled = false;
    }
  }

  persist(payload) {
    if (this.editingId === null) return api.post(this.endpoint, payload);
    return api.put(`${this.endpoint}/${this.editingId}`, payload);
  }

  async remove(id) {
    const confirmed = await ui.confirm({
      title: `¿Eliminar ${this.entityName}?`,
      message: `Se eliminará <strong>${ui.escape(this.displayName(this.findItem(id)))}</strong>. Esta acción no se puede deshacer.`,
    });
    if (!confirmed) return;
    try {
      await api.delete(`${this.endpoint}/${id}`);
      ui.toast("Registro eliminado correctamente");
      await this.load();
    } catch (error) {
      ui.toast(error.message, "danger");
    }
  }
}
