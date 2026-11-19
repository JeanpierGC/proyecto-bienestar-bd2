// Barra de avance de una postulación, a partir de su estado y de si ya tiene beca otorgada.
const flujo = {
  html(postulacion) {
    const rechazada = postulacion.estpost === "RECHAZADA";
    const hechos = this.pasoshechos(postulacion);
    const nombres = ["Registrada", "En evaluación", rechazada ? "Rechazada" : "Aprobada", "Beca otorgada"];
    const pasos = nombres.map((nombre, i) => {
      const clase = this.clase(i, hechos, rechazada);
      const icono = clase === "mal" ? "bi-x-lg" : clase === "hecho" ? "bi-check-lg" : null;
      return `<li class="${clase}"><span class="punto">${icono ? `<i class="bi ${icono}"></i>` : i + 1}</span>${nombre}</li>`;
    });
    return `<ol class="flujo" aria-label="Avance de la postulación">${pasos.join("")}</ol>`;
  },

  pasoshechos({ estpost, otorgada }) {
    if (otorgada) return 4;
    return { REGISTRADA: 1, EN_EVALUACION: 2, APROBADA: 3, RECHAZADA: 3 }[estpost] ?? 1;
  },

  clase(indice, hechos, rechazada) {
    if (rechazada && indice === 2) return "mal";
    if (indice < hechos) return "hecho";
    return indice === hechos && !rechazada ? "actual" : "";
  },
};
