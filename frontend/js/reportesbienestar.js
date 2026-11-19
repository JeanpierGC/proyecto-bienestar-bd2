// Reportes de bienestar: cada bloque consume una vista de la base de datos.
function mensajeVacio(texto) {
  return `<div class="empty-state"><div class="empty-icon"><i class="bi bi-inbox"></i></div><p>${texto}</p></div>`;
}

async function cargarCitas() {
  const contenedor = document.getElementById("graficocitas");
  try {
    const filas = await api.get("/reportes/bienestar/citasprofesional");
    if (filas.length === 0) return (contenedor.innerHTML = mensajeVacio("Aún no hay citas."));
    charts.barList(
      contenedor,
      filas.map((f) => ({
        label: f.profesional,
        sublabel: f.servicio,
        value: f.cantcitas,
        tooltip: `<strong>${ui.escape(f.profesional)}</strong><br>${ui.plural(f.cantcitas, "cita")}`,
      }))
    );
  } catch (error) {
    contenedor.innerHTML = mensajeVacio(ui.escape(error.message));
  }
}

async function cargarCasos() {
  const contenedor = document.getElementById("tablacasos");
  try {
    const filas = await api.get("/reportes/bienestar/casosriesgo");
    if (filas.length === 0) return (contenedor.innerHTML = mensajeVacio("No hay casos de riesgo con seguimiento pendiente."));
    charts.table(
      contenedor,
      ["Estudiante", "Cita", "Nivel", "Seguimiento", "Próxima sesión"],
      filas.map((f) => [f.estudiante, ui.fecha(f.fechacita), f.nivel, f.estadoseguimiento.replace("_", " ").toLowerCase(), ui.fecha(f.proximafecha)])
    );
  } catch (error) {
    contenedor.innerHTML = mensajeVacio(ui.escape(error.message));
  }
}

cargarCitas();
cargarCasos();
