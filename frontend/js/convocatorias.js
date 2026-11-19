const convocatoriasPage = new CrudPage({
  endpoint: "/convocatorias",
  idField: "codconv",
  entityName: "convocatoria",
  columnCount: 5,
  displayName: (c) => c.nomconv,
  searchText: (c) => `${c.nomconv} ${c.perioconv} ${c.beca.nombeca}`,
  renderRow: (c) => `
    <td>
      <div class="cell-main">
        <span class="avatar avatar-square"><i class="bi bi-megaphone"></i></span>
        <div>
          <strong>${ui.escape(c.nomconv)}</strong>
          <div class="text-muted small">Periodo ${ui.escape(c.perioconv)}</div>
        </div>
      </div>
    </td>
    <td><span class="soft-badge neutral"><i class="bi bi-award"></i> ${ui.escape(c.beca.nombeca)}</span></td>
    <td class="text-nowrap">${ui.fecha(c.fechinconv)} <i class="bi bi-arrow-right text-muted"></i> ${ui.fecha(c.fechfinconv)}</td>
    <td title="Cupos disponibles de ${c.cupconv}"><strong>${c.cuposdisponibles ?? "—"}</strong> <span class="text-muted">/ ${c.cupconv}</span></td>
    <td>${ui.chip(c.estconv)}</td>`,
});

const filtroBeca = document.getElementById("filtro-beca");

async function cargarBecas() {
  try {
    const becas = await api.get("/becas");
    const nombre = (b) => b.nombeca;
    ui.fillSelect(filtroBeca, becas, "codbeca", nombre, "Todas las becas");
    ui.fillSelect(document.getElementById("codbeca"), becas, "codbeca", nombre, "Selecciona una beca");
  } catch (error) {
    ui.toast(error.message, "danger");
  }
}

filtroBeca.addEventListener("change", () => convocatoriasPage.setFilter({ codbeca: filtroBeca.value }));

cargarBecas();
convocatoriasPage.load();
convocatoriasPage.openFromUrl();
