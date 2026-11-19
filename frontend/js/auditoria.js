// Auditoría: solo lectura de las tablas de control que llenan los triggers.
const TABLAS = ["postulaciones", "otorgamientos", "citas"];
const ETIQUETAS = { INSERCION: "Inserción", ACTUALIZACION: "Actualización", ELIMINACION: "Eliminación" };
const cache = {};
let actual = "postulaciones";

function fechaHora(texto) {
  const f = new Date(texto);
  return `${ui.fecha(texto.slice(0, 10))} ${f.toTimeString().slice(0, 5)}`;
}

function pintar() {
  const contenedor = document.getElementById("registros");
  const accion = document.getElementById("filtro-accion").value;
  const filas = (cache[actual] || []).filter((f) => !accion || f.accion === accion);
  document.getElementById("contador").textContent = ui.plural(filas.length, "registro");
  if (filas.length === 0) {
    contenedor.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi bi-shield-check"></i></div><h3>Sin registros</h3><p>Aún no hay movimientos en esta tabla.</p></div>`;
    return;
  }
  charts.table(
    contenedor,
    ["#", "Fecha", "Acción", "Código", "Detalle"],
    filas.map((f) => [f.idctrl, fechaHora(f.fecha), ETIQUETAS[f.accion] ?? f.accion, f.codigo, f.detalle])
  );
}

async function cargar(tabla) {
  actual = tabla;
  document.querySelectorAll("#pestanas .nav-link").forEach((b) => b.classList.toggle("active", b.dataset.tabla === tabla));
  try {
    cache[tabla] = await api.get(`/auditoria/${tabla}`);
    pintar();
  } catch (error) {
    document.getElementById("registros").innerHTML = `<div class="empty-state"><p>${ui.escape(error.message)}</p></div>`;
  }
}

document.getElementById("pestanas").addEventListener("click", (e) => {
  const boton = e.target.closest("[data-tabla]");
  if (boton) cargar(boton.dataset.tabla);
});
document.getElementById("filtro-accion").addEventListener("change", pintar);
cargar(actual);
