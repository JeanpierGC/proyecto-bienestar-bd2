// Formulario para postular a una convocatoria abierta. El registro lo valida el procedimiento p01.
const selectorEstudiante = document.getElementById("estudiante");
const selectorConvocatoria = document.getElementById("convocatoria");
const formulario = document.getElementById("formpostulacion");
const botonEnviar = document.getElementById("enviar");
let convocatorias = [];

const convocatoriaElegida = () => convocatorias.find((c) => c.codconv === Number(selectorConvocatoria.value));

function lista(items, vacio, texto) {
  if (items.length === 0) return `<p class="text-muted mb-0">${vacio}</p>`;
  return items.map((i) => `<div class="list-row">${texto(i)}</div>`).join("");
}

async function pintarBeca() {
  const contenedor = document.getElementById("infobeca");
  const convocatoria = convocatoriaElegida();
  botonEnviar.disabled = !convocatoria || convocatoria.estconv !== "ABIERTA";
  if (!convocatoria) {
    contenedor.innerHTML = `<p class="text-muted mb-0">Elige una convocatoria para ver sus requisitos y reglas.</p>`;
    return;
  }
  try {
    const beca = await api.get(`/becas/${convocatoria.codbeca}`);
    contenedor.innerHTML = `
      <div class="mb-3">${ui.chip(convocatoria.estconv)}
        <span class="soft-badge">${beca.porcbeca}% de cobertura</span></div>
      <p class="small text-muted"><i class="bi bi-calendar-event"></i> ${ui.fecha(convocatoria.fechinconv)} al ${ui.fecha(convocatoria.fechfinconv)}
        · <i class="bi bi-people"></i> ${convocatoria.cuposdisponibles ?? "—"} cupos disponibles</p>
      <h3 class="form-section-title">Reglas</h3>
      ${lista(beca.reglas, "Sin reglas.", (r) => `<span>${ui.escape(r.nomreg)}</span><span class="code-tag ms-auto">${ui.escape(r.opreg)} ${r.valreg}</span>`)}
      <h3 class="form-section-title mt-3">Documentos que deberás presentar</h3>
      ${lista(beca.requisitos, "Sin requisitos.", (r) => `<i class="bi bi-check2-circle"></i><span>${ui.escape(r.nomreq)}</span>`)}`;
  } catch (error) {
    contenedor.innerHTML = `<p class="text-danger mb-0">${ui.escape(error.message)}</p>`;
  }
}

async function enviar(event) {
  event.preventDefault();
  ui.clearAlert("alertas");
  if (!formulario.checkValidity()) {
    formulario.classList.add("was-validated");
    return;
  }
  botonEnviar.disabled = true;
  try {
    await api.post("/postulaciones", ui.formData(formulario));
    ui.toast("Postulación registrada");
    setTimeout(() => (location.href = "mispostulaciones.html"), 900);
  } catch (error) {
    ui.alert(error.message, "danger", "alertas");
    botonEnviar.disabled = false;
  }
}

async function iniciar() {
  try {
    await sesion.cargarselector(selectorEstudiante, () => {});
    convocatorias = await api.get("/convocatorias");
    const pedida = Number(new URLSearchParams(location.search).get("conv"));
    const opciones = convocatorias.filter((c) => c.estconv === "ABIERTA" || c.codconv === pedida);
    ui.fillSelect(selectorConvocatoria, opciones, "codconv", (c) => `${c.nomconv} (${c.perioconv})`, "Selecciona una convocatoria");
    if (opciones.some((c) => c.codconv === pedida)) selectorConvocatoria.value = pedida;
    await pintarBeca();
  } catch (error) {
    ui.alert(error.message, "danger", "alertas");
  }
}

selectorConvocatoria.addEventListener("change", pintarBeca);
formulario.addEventListener("submit", enviar);
iniciar();
