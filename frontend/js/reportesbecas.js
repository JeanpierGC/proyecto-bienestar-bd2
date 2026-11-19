// Reportes de becas: cada bloque consume una vista o procedimiento de la base de datos.
const anioRanking = document.getElementById("anio");
anioRanking.value = new Date().getFullYear();

function mensajeVacio(texto) {
  return `<div class="empty-state"><div class="empty-icon"><i class="bi bi-inbox"></i></div><p>${texto}</p></div>`;
}

async function cargarCupos() {
  const contenedor = document.getElementById("tablacupos");
  try {
    const filas = await api.get("/reportes/becas/cuposconv");
    if (filas.length === 0) return (contenedor.innerHTML = mensajeVacio("Aún no hay convocatorias."));
    charts.table(
      contenedor,
      ["Convocatoria", "Cupos", "Postulaciones", "Aprobadas"],
      filas.map((f) => [f.convocatoria, f.cupos, f.cantpostulaciones, f.cantaprobadas])
    );
  } catch (error) {
    contenedor.innerHTML = mensajeVacio(ui.escape(error.message));
  }
}

async function cargarOtorgadas() {
  const contenedor = document.getElementById("tablaotorgadas");
  try {
    const filas = await api.get("/reportes/becas/otorgadas");
    if (filas.length === 0) return (contenedor.innerHTML = mensajeVacio("Aún no se han otorgado becas."));
    charts.table(contenedor, ["Convocatoria", "Beca", "Becas otorgadas"], filas.map((f) => [f.convocatoria, f.beca, f.cantotorgadas]));
  } catch (error) {
    contenedor.innerHTML = mensajeVacio(ui.escape(error.message));
  }
}

async function cargarPorEstudiante() {
  const contenedor = document.getElementById("tablaporestudiante");
  try {
    const filas = await api.get("/reportes/postulaciones/porestudiante");
    if (filas.length === 0) return (contenedor.innerHTML = mensajeVacio("Aún no hay postulaciones."));
    charts.table(contenedor, ["Estudiante", "Año", "Postulaciones"], filas.map((f) => [f.estudiante, f.anio, f.cantpostulaciones]));
  } catch (error) {
    contenedor.innerHTML = mensajeVacio(ui.escape(error.message));
  }
}

async function cargarPromedios() {
  const contenedor = document.getElementById("tablapromedios");
  try {
    const filas = await api.get("/reportes/postulaciones/promediosbeca");
    if (filas.length === 0) return (contenedor.innerHTML = mensajeVacio("Aún no hay seguimientos."));
    charts.table(contenedor, ["Beca", "Promedio", "Seguimientos"], filas.map((f) => [f.beca, f.promedio, f.cantseguimientos]));
  } catch (error) {
    contenedor.innerHTML = mensajeVacio(ui.escape(error.message));
  }
}

async function cargarRanking() {
  const contenedor = document.getElementById("graficoranking");
  const anio = anioRanking.value;
  try {
    const filas = await api.get(`/reportes/becas/ranking?anio=${anio}`);
    if (filas.length === 0) return (contenedor.innerHTML = mensajeVacio(`No hay postulaciones en ${ui.escape(anio)}.`));
    charts.barList(
      contenedor,
      filas.map((f) => ({
        label: f.beca,
        sublabel: `Año ${f.anio}`,
        value: f.cantpostulaciones,
        tooltip: `<strong>${ui.escape(f.beca)}</strong><br>${ui.plural(f.cantpostulaciones, "postulación", "postulaciones")}`,
      }))
    );
  } catch (error) {
    contenedor.innerHTML = mensajeVacio(ui.escape(error.message));
  }
}

document.getElementById("formranking").addEventListener("submit", (event) => {
  event.preventDefault();
  cargarRanking();
});

cargarCupos();
cargarOtorgadas();
cargarPorEstudiante();
cargarPromedios();
cargarRanking();
