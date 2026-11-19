// El estudiante de las pantallas es quien inició sesión: ya no se elige de una lista.
const sesion = {
  codest() {
    return window.acceso.leer()?.codest ?? null;
  },

  // Con un estudiante, devuelve su nombre ("Apellidos, Nombres"); sin argumento, el de quien inició sesión.
  nombre(estudiante) {
    if (estudiante) return `${estudiante.apeest}, ${estudiante.nomest}`;
    return window.acceso.leer()?.nombre ?? "";
  },

  // Deja fija en la lista al estudiante de la sesión y avisa una vez para que la pantalla cargue sus datos.
  async cargarselector(select, alcambiar) {
    const codest = this.codest();
    select.innerHTML = `<option value="${codest}">${this.nombre()}</option>`;
    select.value = codest;
    select.disabled = true;
    alcambiar(codest);
  },
};
