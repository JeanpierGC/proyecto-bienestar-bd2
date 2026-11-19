// Línea de tiempo del seguimiento de un caso, de lo más antiguo a lo más reciente.
const linea = {
  clases: { ABIERTO: "abierto", EN_PROCESO: "proceso", CERRADO: "cerrado" },

  html(seguimientos, acciones = false) {
    if (seguimientos.length === 0) return `<p class="text-muted mb-0">Aún no hay seguimientos.</p>`;
    const items = [...seguimientos].reverse().map((s) => {
      const proxima = s.fechprox ? `<small class="text-muted"><i class="bi bi-calendar-event"></i> Próxima sesión: ${ui.fecha(s.fechprox)}</small>` : "";
      const botones = acciones
        ? `<div class="ms-auto text-nowrap">
             <button class="btn-action" data-editarseg="${s.codseg}" title="Editar"><i class="bi bi-pencil-square"></i></button>
             <button class="btn-action danger" data-quitarseg="${s.codseg}" title="Eliminar"><i class="bi bi-trash3"></i></button>
           </div>` : "";
      return `
        <li class="${this.clases[s.estseg] ?? ""}">
          <span class="marca"></span>
          <div class="d-flex gap-2 align-items-start">
            <div><strong>${ui.fecha(s.fechseg)}</strong> ${ui.chip(s.estseg)}
              <p>${ui.escape(s.descseg)}</p>${proxima}</div>${botones}
          </div>
        </li>`;
    });
    return `<ol class="linea">${items.join("")}</ol>`;
  },
};
