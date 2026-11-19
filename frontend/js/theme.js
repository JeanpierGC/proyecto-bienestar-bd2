// Tema claro/oscuro. Se carga en <head> para aplicar el tema antes de pintar la página.
// Sin preferencia guardada, sigue el tema del sistema operativo.
(function initTheme() {
  const CLAVETEMA = "udh-tema";

  function leerGuardado() {
    try {
      return localStorage.getItem(CLAVETEMA);
    } catch {
      return null;
    }
  }

  function guardar(valor) {
    try {
      localStorage.setItem(CLAVETEMA, valor);
    } catch {
      // Sin almacenamiento disponible: el tema solo dura la visita actual.
    }
  }

  function aplicar(valor) {
    const root = document.documentElement;
    root.dataset.theme = valor;
    root.dataset.bsTheme = valor; // componentes de Bootstrap (modales, selects, botón cerrar)
  }

  const prefiereOscuro = window.matchMedia("(prefers-color-scheme: dark)").matches;
  aplicar(leerGuardado() || (prefiereOscuro ? "dark" : "light"));

  window.tema = {
    actual: () => document.documentElement.dataset.theme,
    alternar() {
      const siguiente = this.actual() === "dark" ? "light" : "dark";
      aplicar(siguiente);
      guardar(siguiente);
      return siguiente;
    },
  };
})();
