// Búsqueda por apellido: procedimiento p06 y función f3 de la base de datos.
const campo = document.getElementById("apellido");
const resultados = document.getElementById("resultados");
let temporizador;
let pedido = 0;

function vacio(icono, titulo, texto) {
  resultados.innerHTML = `<div class="empty-state"><div class="empty-icon"><i class="bi ${icono}"></i></div><h3>${titulo}</h3><p>${texto}</p></div>`;
}

async function buscar() {
  const texto = campo.value.trim();
  const numero = ++pedido;
  if (!texto) {
    document.getElementById("contador").textContent = "";
    return vacio("bi-search", "Busca un estudiante", "Escribe las primeras letras del apellido.");
  }
  try {
    const filas = await api.get(`/busquedas/estudiantes?apellido=${encodeURIComponent(texto)}`);
    if (numero !== pedido) return;
    document.getElementById("contador").textContent = ui.plural(filas.length, "resultado");
    if (filas.length === 0) return vacio("bi-emoji-neutral", "Sin resultados", `Ningún apellido empieza con "${ui.escape(texto)}".`);
    charts.table(
      resultados,
      ["Estudiante", "DNI", "Ciclo", "Edad"],
      filas.map((f) => [`${f.apeest}, ${f.nomest}`, f.dniest, f.cicest, `${f.edad} años`])
    );
  } catch (error) {
    vacio("bi-wifi-off", "No se pudo buscar", ui.escape(error.message));
  }
}

campo.addEventListener("input", () => {
  clearTimeout(temporizador);
  temporizador = setTimeout(buscar, 300);
});
buscar();
