// Catálogo de becas para el estudiante: tarjetas con la convocatoria más relevante de cada beca.
const tarjetas = document.getElementById("tarjetas");
const buscador = document.getElementById("buscador");
const filtroEstado = document.getElementById("filtro-estado");
const detalleModal = new bootstrap.Modal(document.getElementById("modaldetalle"));
let becas = [];
let convocatorias = [];

// Prefiere la convocatoria abierta; si no hay, la que termina más tarde.
function convocatoriaDe(codbeca) {
  const propias = convocatorias.filter((c) => c.codbeca === codbeca);
  return (
    propias.find((c) => c.estconv === "ABIERTA") ||
    [...propias].sort((a, b) => b.fechfinconv.localeCompare(a.fechfinconv))[0] ||
    null
  );
}

function visibles() {
  const texto = ui.normalize(buscador.value.trim());
  return becas.filter((b) => {
    const conv = convocatoriaDe(b.codbeca);
    const coincideTexto = ui.normalize(`${b.nombeca} ${b.tipobeca}`).includes(texto);
    const coincideEstado = !filtroEstado.value || conv?.estconv === filtroEstado.value;
    return coincideTexto && coincideEstado;
  });
}

function tarjeta(beca) {
  const conv = convocatoriaDe(beca.codbeca);
  const estado = conv ? ui.chip(conv.estconv) : `<span class="chip c-mute">Sin convocatoria</span>`;
  const datosConv = conv
    ? `<div class="small"><i class="bi bi-megaphone"></i> ${ui.escape(conv.nomconv)}</div>
       <div class="small text-muted"><i class="bi bi-calendar-event"></i> ${ui.fecha(conv.fechinconv)} al ${ui.fecha(conv.fechfinconv)}</div>
       <div class="small text-muted"><i class="bi bi-people"></i> ${conv.cuposdisponibles ?? "—"} cupos disponibles de ${conv.cupconv}</div>`
    : `<div class="small text-muted">Aún no hay convocatorias para esta beca.</div>`;
  return `
    <div class="col-md-6 col-xl-4">
      <article class="card-app h-100">
        <div class="card-app-body d-flex flex-column gap-2 h-100">
          <div class="d-flex justify-content-between align-items-start gap-2">
            <span class="soft-badge neutral">${ui.escape(beca.tipobeca)}</span>${estado}
          </div>
          <h3 class="h5 mb-0">${ui.escape(beca.nombeca)}</h3>
          <div class="fs-2 fw-bold" style="color: var(--brand)">${beca.porcbeca}%</div>
          ${datosConv}
          <button class="btn btn-primary mt-auto" data-codbeca="${beca.codbeca}">Ver detalles</button>
        </div>
      </article>
    </div>`;
}

function pintar() {
  const lista = visibles();
  document.getElementById("contador").textContent = ui.plural(lista.length, "beca");
  tarjetas.innerHTML = lista.length
    ? lista.map(tarjeta).join("")
    : `<div class="col-12"><div class="empty-state"><div class="empty-icon"><i class="bi bi-search"></i></div>
         <h3>No hay becas para mostrar</h3><p>Prueba con otro filtro.</p></div></div>`;
}

function listaDe(items, vacio, texto) {
  if (items.length === 0) return `<p class="text-muted mb-0">${vacio}</p>`;
  return items.map((i) => `<div class="list-row d-flex align-items-center gap-2">${texto(i)}</div>`).join("");
}

function abrirDetalle(codbeca) {
  const beca = becas.find((b) => b.codbeca === codbeca);
  const conv = convocatoriaDe(codbeca);
  document.getElementById("detalletitulo").textContent = beca.nombeca;
  document.getElementById("detalledescripcion").textContent = beca.descbeca ?? "Sin descripción.";
  document.getElementById("detallerequisitos").innerHTML = listaDe(
    beca.requisitos, "Sin requisitos registrados.", (r) => `<i class="bi bi-check2-circle me-2"></i>${ui.escape(r.nomreq)}`
  );
  document.getElementById("detallereglas").innerHTML = listaDe(
    beca.reglas, "Sin reglas registradas.",
    (r) => `<span>${ui.escape(r.nomreg)}</span><span class="code-tag ms-auto">${ui.escape(r.opreg)} ${r.valreg}</span>`
  );

  const boton = document.getElementById("botonpostular");
  const puedePostular = conv?.estconv === "ABIERTA" && (conv.cuposdisponibles ?? 0) > 0;
  boton.classList.toggle("disabled", !puedePostular);
  boton.setAttribute("aria-disabled", String(!puedePostular));
  boton.href = puedePostular ? `postular.html?conv=${conv.codconv}` : "#";
  boton.textContent = puedePostular ? "Postular" : "Convocatoria no disponible";
  detalleModal.show();
}

tarjetas.addEventListener("click", (event) => {
  const boton = event.target.closest("[data-codbeca]");
  if (boton) abrirDetalle(Number(boton.dataset.codbeca));
});
buscador.addEventListener("input", pintar);
filtroEstado.addEventListener("change", pintar);

async function iniciar() {
  try {
    [becas, convocatorias] = await Promise.all([api.get("/becas"), api.get("/convocatorias")]);
    becas = becas.filter((b) => b.estbeca === "ACTIVA");
    pintar();
  } catch (error) {
    tarjetas.innerHTML = `<div class="col-12"><div class="empty-state"><div class="empty-icon"><i class="bi bi-wifi-off"></i></div>
      <h3>No se pudo cargar el catálogo</h3><p>${ui.escape(error.message)}</p></div></div>`;
  }
}

iniciar();
