// Pantalla de acceso: pide el token a la API y guarda la sesión (la misma que lee layout.js).
const CLAVESESION = "udhsesion";
const formulario = document.getElementById("formulario");
const alertas = document.getElementById("alertas");
const botonEntrar = document.getElementById("entrar");

function destino(sesion) {
  return sesion.rolusu === "ADMIN" ? "index.html" : "pages/inicioestudiante.html";
}

function sesionguardada() {
  try {
    const sesion = JSON.parse(localStorage.getItem(CLAVESESION));
    return sesion && sesion.vence > Date.now() ? sesion : null;
  } catch {
    return null;
  }
}

function mostrarerror(mensaje) {
  alertas.innerHTML = `<div class="alert alert-danger py-2" role="alert">${mensaje.replace(/</g, "&lt;")}</div>`;
}

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  alertas.innerHTML = "";
  formulario.classList.add("was-validated");
  if (!formulario.checkValidity()) return;

  botonEntrar.disabled = true;
  try {
    const datos = await api.post("/auth/login", {
      nomusu: formulario.nomusu.value.trim(),
      clausu: formulario.clausu.value,
    });
    const sesion = { ...datos, vence: Date.now() + datos.horas * 3600 * 1000 };
    try {
      localStorage.setItem(CLAVESESION, JSON.stringify(sesion));
    } catch {
      return mostrarerror("Tu navegador no deja guardar la sesión. Activa el almacenamiento del sitio e inténtalo de nuevo.");
    }
    location.replace(destino(sesion));
  } catch (error) {
    mostrarerror(error.message);
    formulario.clausu.select();
  } finally {
    botonEntrar.disabled = false;
  }
});

document.getElementById("verclave").addEventListener("click", (evento) => {
  const visible = formulario.clausu.type === "text";
  formulario.clausu.type = visible ? "password" : "text";
  evento.currentTarget.innerHTML = `<i class="bi ${visible ? "bi-eye" : "bi-eye-slash"}"></i>`;
});

const existente = sesionguardada();
if (existente) location.replace(destino(existente));
