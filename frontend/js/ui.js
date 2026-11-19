// Utilidades de interfaz reutilizadas por todas las pantallas.
// Color del chip según el estado (ver docs/disenoui.md) y su texto en español.
const COLORESESTADO = {
  ACTIVA: "c-ok", INACTIVA: "c-mute",
  ABIERTA: "c-ok", CERRADA: "c-mute", EN_EVALUACION: "c-warn",
  REGISTRADA: "c-info", APROBADA: "c-ok", RECHAZADA: "c-bad",
  VIGENTE: "c-ok", FINALIZADA: "c-mute", REVOCADA: "c-bad", SUSPENDIDA: "c-warn",
  PROGRAMADA: "c-info", ATENDIDA: "c-ok", CANCELADA: "c-bad", NO_ASISTIO: "c-warn",
  ABIERTO: "c-info", EN_PROCESO: "c-warn", CERRADO: "c-mute",
  PENDIENTE: "c-warn", APROBADO: "c-ok", OBSERVADO: "c-warn", RECHAZADO: "c-bad",
  BAJO: "c-ok", MEDIO: "c-info", ALTO: "c-warn", CRITICO: "c-bad",
};
const TEXTOESTADO = { EN_EVALUACION: "En evaluación", EN_PROCESO: "En proceso", NO_ASISTIO: "No asistió", CRITICO: "Crítico" };

const ui = {
  // Aviso dentro de un contenedor (se usa para errores dentro de los modales).
  alert(message, type = "danger", containerId = "modal-alertas") {
    document.getElementById(containerId).innerHTML = `
      <div class="alert alert-${type} d-flex gap-2 align-items-start py-2" role="alert">
        <i class="bi bi-exclamation-circle mt-1"></i><div>${ui.escape(message)}</div>
      </div>`;
  },

  clearAlert(containerId = "modal-alertas") {
    document.getElementById(containerId).innerHTML = "";
  },

  // Aviso flotante en la esquina inferior derecha.
  toast(message, type = "success") {
    const icon = type === "success" ? "bi-check-circle" : "bi-exclamation-triangle";
    const container = ui.toastContainer();
    container.insertAdjacentHTML(
      "beforeend",
      `<div class="toast" role="status" aria-live="polite">
        <div class="d-flex align-items-center gap-2 px-3 py-2">
          <i class="bi ${icon}"></i>
          <div class="flex-grow-1">${ui.escape(message)}</div>
        </div>
      </div>`
    );
    const element = container.lastElementChild;
    element.addEventListener("hidden.bs.toast", () => element.remove());
    new bootstrap.Toast(element, { delay: 3500 }).show();
  },

  toastContainer() {
    let container = document.getElementById("toasts");
    if (!container) {
      document.body.insertAdjacentHTML(
        "beforeend",
        '<div id="toasts" class="toast-container position-fixed bottom-0 end-0 p-3"></div>'
      );
      container = document.getElementById("toasts");
    }
    return container;
  },

  // Modal de confirmación. Devuelve una promesa que se resuelve en true o false.
  confirm({ title, message, confirmText = "Eliminar" }) {
    const element = ui.confirmModal();
    element.querySelector("[data-confirm-title]").textContent = title;
    element.querySelector("[data-confirm-message]").innerHTML = message;
    element.querySelector("[data-confirm-ok]").textContent = confirmText;
    const modal = bootstrap.Modal.getOrCreateInstance(element);

    return new Promise((resolve) => {
      let accepted = false;
      const ok = element.querySelector("[data-confirm-ok]");
      const onOk = () => {
        accepted = true;
        modal.hide();
      };
      ok.addEventListener("click", onOk, { once: true });
      element.addEventListener(
        "hidden.bs.modal",
        () => {
          ok.removeEventListener("click", onOk);
          resolve(accepted);
        },
        { once: true }
      );
      modal.show();
    });
  },

  confirmModal() {
    let element = document.getElementById("confirm-modal");
    if (!element) {
      document.body.insertAdjacentHTML(
        "beforeend",
        `<div class="modal fade" id="confirm-modal" tabindex="-1">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-body d-flex pt-4">
                <span class="modal-icon danger"><i class="bi bi-trash3"></i></span>
                <div>
                  <h2 class="h5 mb-1" data-confirm-title></h2>
                  <p class="text-muted mb-0" data-confirm-message></p>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-ghost" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-danger" data-confirm-ok></button>
              </div>
            </div>
          </div>
        </div>`
      );
      element = document.getElementById("confirm-modal");
    }
    return element;
  },

  escape(text) {
    const div = document.createElement("div");
    div.textContent = text ?? "";
    return div.innerHTML;
  },

  initials(...words) {
    return words
      .map((word) => (word ?? "").trim().charAt(0))
      .join("")
      .toUpperCase();
  },

  // Texto en minúsculas y sin tildes, para búsquedas.
  normalize(text) {
    return String(text ?? "")
      .normalize("NFD")
      .replace(/\p{Diacritic}/gu, "")
      .toLowerCase();
  },

  plural(count, singular, pluralForm = `${singular}s`) {
    return `${count} ${count === 1 ? singular : pluralForm}`;
  },

  stateRow(colspan, { icon, title, text = "" }) {
    return `
      <tr><td colspan="${colspan}">
        <div class="empty-state">
          <div class="empty-icon"><i class="bi ${icon}"></i></div>
          <h3>${title}</h3>
          <p>${text}</p>
        </div>
      </td></tr>`;
  },

  loadingRow(colspan) {
    return `
      <tr><td colspan="${colspan}" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <div class="text-muted small mt-2">Cargando...</div>
      </td></tr>`;
  },

  // Chip de color para un estado de la base de datos (ej. "EN_EVALUACION").
  chip(state) {
    const text = TEXTOESTADO[state] || state.charAt(0) + state.slice(1).toLowerCase();
    return `<span class="chip ${COLORESESTADO[state] || "c-mute"}">${ui.escape(text)}</span>`;
  },

  // "2026-03-15" -> "15/03/2026" (sin pasar por Date para evitar desfases de zona horaria).
  fecha(iso) {
    if (!iso) return "—";
    const [year, month, day] = iso.split("-");
    return `${day}/${month}/${year}`;
  },

  fillSelect(select, items, valueKey, textFn, placeholder) {
    const options = items.map(
      (item) => `<option value="${item[valueKey]}">${ui.escape(textFn(item))}</option>`
    );
    select.innerHTML = `<option value="">${placeholder}</option>${options.join("")}`;
  },

  // Convierte el formulario en un objeto: "" -> null y campos data-type="number" -> Number.
  formData(form) {
    const data = {};
    for (const field of form.querySelectorAll("[name]")) {
      const value = field.value.trim();
      if (value === "") data[field.name] = null;
      else data[field.name] = field.dataset.type === "number" ? Number(value) : value;
    }
    return data;
  },

  fillForm(form, item) {
    for (const field of form.querySelectorAll("[name]")) {
      field.value = item[field.name] ?? "";
    }
  },
};
