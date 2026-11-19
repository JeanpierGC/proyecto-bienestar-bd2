// Panel principal: indicadores de todos los módulos, gráficos y últimos registros.
const MODULOS = [
  { nombre: "Académico", detalle: "Facultades, escuelas y estudiantes", listo: true },
  { nombre: "Becas", detalle: "Becas, reglas, requisitos y convocatorias", listo: true },
  { nombre: "Postulaciones", detalle: "Postulación, evaluación, otorgamiento y seguimiento", listo: true },
  { nombre: "Bienestar", detalle: "Psicología, orientación, citas, atenciones y fichas", listo: true },
  { nombre: "Auditoría", detalle: "Triggers sobre postulaciones, becas otorgadas y citas", listo: true },
  { nombre: "Acceso", detalle: "Login con roles de administrador y estudiante", listo: true },
];

// Colores de la paleta categórica validada, en orden fijo. Más allá se agrupa en "Otras".
const COLORESCAT = ["var(--cat-1)", "var(--cat-2)", "var(--cat-3)", "var(--cat-4)", "var(--cat-5)"];

function renderIndicadores(resumen) {
  const promedio = resumen.ciclopromedio === null ? "—" : resumen.ciclopromedio.toFixed(1);
  const valores = {
    facultades: resumen.totalfacultades,
    escuelas: resumen.totalescuelas,
    estudiantes: resumen.totalestudiantes,
    promedio,
  };
  for (const [clave, valor] of Object.entries(valores)) {
    document.querySelector(`[data-stat="${clave}"]`).textContent = valor;
  }
}

function totalesPorFacultad(porEscuela) {
  const totales = new Map();
  for (const escuela of porEscuela) {
    totales.set(escuela.nomfac, (totales.get(escuela.nomfac) ?? 0) + escuela.total);
  }
  return [...totales].map(([label, value]) => ({ label, value })).sort((a, b) => b.value - a.value);
}

function renderPorFacultad(resumen) {
  const contenedor = document.getElementById("grafico-facultades");
  const facultades = totalesPorFacultad(resumen.estudiantesporescuela);
  if (facultades.length === 0) {
    contenedor.innerHTML = '<p class="text-muted small mb-0">Aún no hay facultades con escuelas.</p>';
    return;
  }
  const principales = facultades.slice(0, COLORESCAT.length);
  const resto = facultades.slice(COLORESCAT.length);
  const datos = principales.map((f, i) => ({ ...f, color: COLORESCAT[i] }));
  if (resto.length) {
    datos.push({ label: "Otras", value: resto.reduce((s, f) => s + f.value, 0), color: "var(--cat-otros)" });
  }
  charts.donut(contenedor, datos, { caption: "estudiantes" });
}

function renderPorEscuela(resumen) {
  const contenedor = document.getElementById("grafico-escuelas");
  const datos = resumen.estudiantesporescuela;
  if (datos.length === 0) {
    contenedor.innerHTML = '<p class="text-muted small mb-0">Aún no hay escuelas registradas.</p>';
    return;
  }
  charts.barList(
    contenedor,
    datos.map((e) => ({
      label: e.nomesc,
      sublabel: e.nomfac,
      value: e.total,
      tooltip: `<strong>${ui.escape(e.nomesc)}</strong>${ui.plural(e.total, "estudiante")}`,
    }))
  );
}

function renderPorCiclo(resumen) {
  const datos = resumen.estudiantesporciclo;
  const grafico = document.getElementById("grafico-ciclos");
  const tabla = document.getElementById("tabla-ciclos");

  charts.columns(
    grafico,
    datos.map((c) => ({
      label: c.ciclo,
      value: c.total,
      tooltip: `<strong>Ciclo ${c.ciclo}</strong>${ui.plural(c.total, "estudiante")}`,
    }))
  );
  charts.table(tabla, ["Ciclo", "Estudiantes"], datos.map((c) => [c.ciclo, c.total]));

  document.querySelectorAll("[data-vista]").forEach((boton) =>
    boton.addEventListener("click", () => {
      const verTabla = boton.dataset.vista === "tabla";
      grafico.classList.toggle("d-none", verTabla);
      tabla.classList.toggle("d-none", !verTabla);
      document.querySelectorAll("[data-vista]").forEach((b) => b.setAttribute("aria-pressed", b === boton));
    })
  );
}

function renderUltimos(resumen) {
  const contenedor = document.getElementById("ultimos-estudiantes");
  if (resumen.ultimosestudiantes.length === 0) {
    contenedor.innerHTML = '<p class="text-muted small mb-0">Aún no hay estudiantes registrados.</p>';
    return;
  }
  contenedor.innerHTML = resumen.ultimosestudiantes
    .map(
      (e) => `
      <div class="list-row">
        <span class="avatar avatar-sm">${ui.initials(e.nomest, e.apeest)}</span>
        <div class="list-text">
          <strong class="text-truncate">${ui.escape(`${e.nomest} ${e.apeest}`)}</strong>
          <small class="d-block text-truncate">${ui.escape(e.escuela.nomesc)}</small>
        </div>
        <span class="soft-badge neutral">Ciclo ${e.cicest}</span>
      </div>`
    )
    .join("");
}

function renderModulos() {
  document.getElementById("modulos").innerHTML = MODULOS.map(
    (m, i) => `
    <div class="list-row">
      <span class="avatar avatar-sm ${m.listo ? "i-ok" : "c-mute"}">${m.listo ? '<i class="bi bi-check-lg"></i>' : i + 1}</span>
      <div class="list-text">
        <strong>${m.nombre}</strong>
        <small class="d-block">${m.detalle}</small>
      </div>
      ${
        m.listo
          ? '<span class="chip c-ok">Completado</span>'
          : '<span class="chip c-mute">Pendiente</span>'
      }
    </div>`
  ).join("");
}

// Indicadores de becas y bienestar: salen de la API (funciones y vistas de la base de datos).
async function cargarGestion() {
  const [postulaciones, otorgadas, citas, casos] = await Promise.all([
    api.get("/postulaciones"),
    api.get("/becasotorgadas"),
    api.get("/citas?estcita=PROGRAMADA"),
    api.get("/reportes/bienestar/casosriesgo"),
  ]);
  const valores = {
    postulaciones: postulaciones.length,
    otorgadas: otorgadas.filter((o) => o.estotor === "VIGENTE").length,
    citas: citas.length,
    riesgo: casos.length,
  };
  for (const [clave, valor] of Object.entries(valores)) {
    document.querySelector(`[data-stat="${clave}"]`).textContent = valor;
  }
}

async function cargarPanel() {
  renderModulos();
  cargarGestion().catch((error) => ui.toast(error.message, "danger"));
  try {
    const resumen = await api.get("/resumen/academico");
    renderIndicadores(resumen);
    renderPorCiclo(resumen);
    renderPorFacultad(resumen);
    renderPorEscuela(resumen);
    renderUltimos(resumen);
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

cargarPanel();
