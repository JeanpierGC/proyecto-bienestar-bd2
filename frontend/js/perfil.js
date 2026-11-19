// Mi perfil: datos del usuario (y del estudiante, si lo es) y cambio de contraseña.
const formulario = document.getElementById("formclave");

function fila(icono, etiqueta, valor) {
  return `
    <div class="list-row">
      <span class="stat-icon i-brand"><i class="bi ${icono}"></i></span>
      <div class="list-text"><small class="d-block">${etiqueta}</small><strong>${ui.escape(String(valor ?? "—"))}</strong></div>
    </div>`;
}

async function cargarDatos() {
  const contenedor = document.getElementById("datos");
  try {
    const perfil = await api.get("/auth/perfil");
    const filas = [
      fila("bi-person", "Nombre", perfil.nombre),
      fila("bi-at", "Usuario", perfil.nomusu),
      fila("bi-shield-lock", "Rol", perfil.rolusu === "ADMIN" ? "Administrador" : "Estudiante"),
    ];
    const e = perfil.estudiante;
    if (e) {
      filas.push(
        fila("bi-credit-card-2-front", "DNI", e.dniest),
        fila("bi-envelope", "Correo", e.correst),
        fila("bi-building", "Facultad", e.facultad),
        fila("bi-mortarboard", "Escuela", e.escuela),
        fila("bi-bar-chart-steps", "Ciclo", e.cicest),
        fila("bi-cake2", "Nacimiento", `${ui.fecha(e.fnacest)} (${e.edad} años)`),
        fila("bi-geo-alt", "Dirección", e.direst)
      );
    }
    contenedor.innerHTML = filas.join("");
  } catch (error) {
    contenedor.innerHTML = `<div class="empty-state"><p>${ui.escape(error.message)}</p></div>`;
  }
}

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  ui.clearAlert("alertasclave");
  const confirmar = document.getElementById("confirmar");
  confirmar.setCustomValidity(confirmar.value === formulario.nueva.value ? "" : "no coincide");
  formulario.classList.add("was-validated");
  if (!formulario.checkValidity()) {
    if (confirmar.validationMessage === "no coincide") ui.alert("Las contraseñas nuevas no coinciden.", "danger", "alertasclave");
    return;
  }
  try {
    await api.put("/auth/clave", { actual: formulario.actual.value, nueva: formulario.nueva.value });
    formulario.reset();
    formulario.classList.remove("was-validated");
    ui.toast("Contraseña actualizada");
  } catch (error) {
    ui.alert(error.message, "danger", "alertasclave");
  }
});

cargarDatos();
