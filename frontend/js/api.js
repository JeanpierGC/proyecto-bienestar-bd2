// Cliente HTTP de la API REST del backend.
const APIURL = "http://localhost:8000/api";

async function request(method, path, body) {
  const options = { method, headers: { "Content-Type": "application/json" } };
  const token = window.acceso?.token();
  if (token) options.headers.Authorization = `Bearer ${token}`;
  if (body !== undefined) options.body = JSON.stringify(body);

  let response;
  try {
    response = await fetch(`${APIURL}${path}`, options);
  } catch {
    throw new Error("No se pudo conectar con el servidor. ¿Está corriendo el backend?");
  }

  // Sesión vencida o inválida: se vuelve al login (salvo en el propio login, donde el 401 es "clave incorrecta").
  if (response.status === 401 && token) return window.acceso.salir();
  if (response.status === 204) return null;
  const data = await response.json().catch(() => null);
  if (!response.ok) throw new Error(errorMessage(data, response.status));
  return data;
}

// Pydantic antepone "Value error, " a los mensajes propios y "body" al nombre del campo.
function mensajeValidacion(error) {
  const campo = error.loc.at(-1);
  const texto = error.msg.replace(/^Value error, /, "");
  return campo === "body" ? texto : `${campo}: ${texto}`;
}

function errorMessage(data, status) {
  const detail = data?.detail;
  if (Array.isArray(detail)) {
    return detail.map(mensajeValidacion).join(" | ");
  }
  return detail || `Error ${status}`;
}

const api = {
  get: (path) => request("GET", path),
  post: (path, body) => request("POST", path, body),
  put: (path, body) => request("PUT", path, body),
  delete: (path) => request("DELETE", path),
};
