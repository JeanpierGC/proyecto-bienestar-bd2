// Gráficos simples en HTML/SVG: barras horizontales, columnas y dona, con tooltip al pasar el cursor.
// Los colores salen de variables CSS (--series-1, --cat-N), así siguen el tema claro/oscuro.
const charts = (() => {
  let tooltip;

  function getTooltip() {
    if (!tooltip) {
      tooltip = document.createElement("div");
      tooltip.className = "chart-tooltip";
      tooltip.setAttribute("role", "tooltip");
      document.body.appendChild(tooltip);
    }
    return tooltip;
  }

  function moveTooltip(x, y) {
    const tip = getTooltip();
    const left = Math.min(x + 14, window.innerWidth - tip.offsetWidth - 8);
    tip.style.left = `${left}px`;
    tip.style.top = `${y - tip.offsetHeight - 12}px`;
  }

  function showTooltip(html, x, y) {
    const tip = getTooltip();
    tip.innerHTML = html;
    tip.classList.add("visible");
    moveTooltip(x, y);
  }

  function hideTooltip() {
    getTooltip().classList.remove("visible");
  }

  // Cada elemento con data-i muestra el tooltip de su dato (con mouse o teclado).
  function bindTooltips(container, tooltipHtml) {
    container.querySelectorAll("[data-i]").forEach((element) => {
      const html = tooltipHtml(Number(element.dataset.i));
      element.addEventListener("mouseenter", (e) => showTooltip(html, e.clientX, e.clientY));
      element.addEventListener("mousemove", (e) => moveTooltip(e.clientX, e.clientY));
      element.addEventListener("mouseleave", hideTooltip);
      element.addEventListener("focus", () => {
        const rect = element.getBoundingClientRect();
        showTooltip(html, rect.left + rect.width / 2, rect.top);
      });
      element.addEventListener("blur", hideTooltip);
    });
  }

  function niceTicks(max) {
    const step = Math.max(1, Math.ceil(max / 4));
    const top = Math.max(step, Math.ceil(max / step) * step);
    const ticks = [];
    for (let value = 0; value <= top; value += step) ticks.push(value);
    return { top, ticks };
  }

  // data: [{ label, sublabel, value, tooltip }]
  function barList(container, data) {
    const max = Math.max(1, ...data.map((d) => d.value));
    container.innerHTML = data
      .map(
        (d, i) => `
        <div class="bar-row" tabindex="0" data-i="${i}">
          <div class="bar-label">
            <span>${ui.escape(d.label)}</span>
            <small>${ui.escape(d.sublabel)}</small>
          </div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${(d.value / max) * 85}%"></div>
            <span class="bar-value">${d.value}</span>
          </div>
        </div>`
      )
      .join("");
    bindTooltips(container, (i) => data[i].tooltip);
  }

  // data: [{ label, value, tooltip }]. Solo se rotulan las columnas con valor.
  function columns(container, data) {
    const { top, ticks } = niceTicks(Math.max(...data.map((d) => d.value)));
    const pct = (value) => (value / top) * 100;

    container.innerHTML = `
      <div class="col-chart">
        <div class="col-axis">
          ${ticks.map((t) => `<span style="bottom: ${pct(t)}%">${t}</span>`).join("")}
        </div>
        <div class="col-plot">
          ${ticks.slice(1).map((t) => `<div class="col-grid" style="bottom: ${pct(t)}%"></div>`).join("")}
          <div class="col-bars">
            ${data
              .map(
                (d, i) => `
                <div class="col-slot" tabindex="0" data-i="${i}">
                  ${d.value > 0 ? `<span class="col-value" style="bottom: calc(${pct(d.value)}% + 4px)">${d.value}</span>` : ""}
                  <div class="col-bar" style="height: ${pct(d.value)}%"></div>
                </div>`
              )
              .join("")}
          </div>
        </div>
        <div class="col-xlabels">${data.map((d) => `<span>${d.label}</span>`).join("")}</div>
      </div>`;
    bindTooltips(container, (i) => data[i].tooltip);
  }

  // data: [{ label, value, color }] con color = variable CSS (ej. "var(--cat-1)").
  function donut(container, data, { caption }) {
    const total = data.reduce((sum, d) => sum + d.value, 0);
    const radius = 52;
    const circumference = 2 * Math.PI * radius;
    const visibles = data.filter((d) => d.value > 0).length;
    const gap = visibles > 1 ? 2 : 0; // separación del color de la superficie entre segmentos
    const percent = (value) => (total ? Math.round((value / total) * 100) : 0);

    let offset = 0;
    const segments = data
      .map((d, i) => {
        if (d.value === 0) return "";
        const length = (d.value / total) * circumference;
        const segment = `
          <circle class="donut-seg" cx="70" cy="70" r="${radius}" tabindex="0" data-i="${i}"
                  style="stroke: ${d.color}"
                  stroke-dasharray="${Math.max(length - gap, 0)} ${circumference - length + gap}"
                  stroke-dashoffset="${-offset}" transform="rotate(-90 70 70)"></circle>`;
        offset += length;
        return segment;
      })
      .join("");

    container.innerHTML = `
      <div class="donut-wrap">
        <svg viewBox="0 0 140 140" role="img" aria-label="${ui.escape(caption)}: ${total}">
          <circle cx="70" cy="70" r="${radius}" fill="none" stroke-width="18" style="stroke: var(--line)"></circle>
          ${segments}
          <text class="donut-total" x="70" y="72" text-anchor="middle">${total}</text>
          <text class="donut-caption" x="70" y="90" text-anchor="middle">${ui.escape(caption)}</text>
        </svg>
        <ul class="legend">
          ${data
            .map(
              (d, i) => `
              <li tabindex="0" data-i="${i}">
                <i style="background: ${d.color}"></i>
                <span>${ui.escape(d.label)}</span>
                <b>${d.value}</b>
                <small>${percent(d.value)}%</small>
              </li>`
            )
            .join("")}
        </ul>
      </div>`;
    bindTooltips(
      container,
      (i) => `<strong>${ui.escape(data[i].label)}</strong>${data[i].value} (${percent(data[i].value)}%)`
    );
  }

  // Vista en tabla del mismo gráfico (accesibilidad).
  function table(container, headers, rows) {
    container.innerHTML = `
      <div class="tbl-wrap">
        <table class="table table-sm table-app" style="min-width: 0">
          <thead><tr>${headers.map((h) => `<th>${h}</th>`).join("")}</tr></thead>
          <tbody>
            ${rows.map((r) => `<tr>${r.map((c) => `<td>${ui.escape(String(c))}</td>`).join("")}</tr>`).join("")}
          </tbody>
        </table>
      </div>`;
  }

  return { barList, columns, donut, table };
})();
