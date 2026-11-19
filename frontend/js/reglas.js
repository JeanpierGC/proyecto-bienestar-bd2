const reglasPage = new CrudPage({
  endpoint: "/reglas",
  idField: "codreg",
  entityName: "regla",
  columnCount: 4,
  displayName: (r) => r.nomreg,
  searchText: (r) => `${r.nomreg} ${nombreBeca(r.codbeca)}`,
  renderRow: (r) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-square"><i class="bi bi-rulers"></i></span>
        <div>
          <strong>${ui.escape(r.nomreg)}</strong>
          <div class="text-muted small">${ui.escape(r.descreg ?? "")}</div>
        </div>
      </div>
    </td>
    <td><span class="code-tag">${ui.escape(r.opreg)} ${r.valreg}</span></td>
    <td><span class="soft-badge neutral"><i class="bi bi-award"></i> ${ui.escape(nombreBeca(r.codbeca))}</span></td>
    <td><span class="code-tag">#${r.codreg}</span></td>`,
});

const becasPorId = new Map();
const filtroBeca = document.getElementById("filtro-beca");

function nombreBeca(codbeca) {
  return becasPorId.get(codbeca)?.nombeca ?? `Beca ${codbeca}`;
}

async function cargarBecas() {
  try {
    const becas = await api.get("/becas");
    becas.forEach((b) => becasPorId.set(b.codbeca, b));
    ui.fillSelect(filtroBeca, becas, "codbeca", (b) => b.nombeca, "Todas las becas");
    ui.fillSelect(document.getElementById("codbeca"), becas, "codbeca", (b) => b.nombeca, "Selecciona una beca");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

filtroBeca.addEventListener("change", () => reglasPage.setFilter({ codbeca: filtroBeca.value }));

cargarBecas().then(() => reglasPage.load());
reglasPage.openFromUrl();
