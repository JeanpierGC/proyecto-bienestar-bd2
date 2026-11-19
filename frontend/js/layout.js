// Estructura común: barra lateral con el logo UDH + barra superior + título de página.
// Cada página declara <body data-page data-title data-section data-description> y un <main>.
// Si el <main> trae un .page-actions, se coloca a la derecha del título.
// Sesión guardada al iniciar sesión (login.js escribe la misma clave y la misma forma).
window.acceso = {
  clave: "udhsesion",

  leer() {
    try {
      const sesion = JSON.parse(localStorage.getItem(this.clave));
      return sesion && sesion.vence > Date.now() ? sesion : null;
    } catch {
      return null;
    }
  },

  token() {
    return this.leer()?.token ?? null;
  },

  salir() {
    try {
      localStorage.removeItem(this.clave);
    } catch {
      // Sin almacenamiento disponible: no hay nada que borrar.
    }
    location.replace(this.base + "login.html");
  },
};

(function renderLayout() {
  const base = location.pathname.includes("/pages/") ? "../" : "";
  const { page, title, section, description } = document.body.dataset;
  window.acceso.base = base;

  const sesion = window.acceso.leer();
  if (!sesion) return window.acceso.salir();

  // Páginas que solo tiene sentido abrir como estudiante (usan su propio código de estudiante).
  const PAGINASESTUDIANTE = ["inicioestudiante", "catalogo", "mispostulaciones", "misbecas", "bienestar", "miscitas", "miseguimiento"];
  const esadmin = sesion.rolusu === "ADMIN";
  const inicio = esadmin ? "index.html" : "pages/inicioestudiante.html";
  if (!esadmin && !PAGINASESTUDIANTE.includes(page) && page !== "perfil") return location.replace(base + inicio);
  if (esadmin && PAGINASESTUDIANTE.includes(page) && page !== "catalogo") return location.replace(base + inicio);

  // Las opciones sin href se habilitan cuando su módulo esté terminado.
  const NAV = [
    {
      section: "Estudiante",
      items: [
        { page: "inicioestudiante", text: "Inicio", icon: "bi-house-door", href: "pages/inicioestudiante.html" },
        { page: "catalogo", text: "Becas", icon: "bi-award", href: "pages/catalogo.html" },
        { page: "mispostulaciones", text: "Mis postulaciones", icon: "bi-file-earmark-text", href: "pages/mispostulaciones.html" },
        { page: "misbecas", text: "Mis becas", icon: "bi-patch-check", href: "pages/misbecas.html" },
        { page: "bienestar", text: "Bienestar universitario", icon: "bi-heart-pulse", href: "pages/bienestar.html" },
        { page: "miscitas", text: "Mis citas", icon: "bi-calendar-event", href: "pages/miscitas.html" },
        { page: "miseguimiento", text: "Seguimiento", icon: "bi-activity", href: "pages/miseguimiento.html" },
        { page: "perfil", text: "Mi perfil", icon: "bi-person-circle", href: "pages/perfil.html" },
      ],
    },
    {
      section: "Administración",
      items: [
        { page: "inicio", text: "Panel institucional", icon: "bi-bar-chart-line", href: "index.html" },
        { page: "facultades", text: "Facultades", icon: "bi-building", href: "pages/facultades.html" },
        { page: "escuelas", text: "Escuelas", icon: "bi-mortarboard", href: "pages/escuelas.html" },
        { page: "estudiantes", text: "Estudiantes", icon: "bi-people", href: "pages/estudiantes.html" },
        { page: "busquedas", text: "Buscar estudiantes", icon: "bi-search", href: "pages/busquedas.html" },
        { page: "becas", text: "Becas", icon: "bi-award", href: "pages/becas.html" },
        { page: "convocatorias", text: "Convocatorias", icon: "bi-megaphone", href: "pages/convocatorias.html" },
        { page: "postulaciones", text: "Postulaciones", icon: "bi-file-earmark-text", href: "pages/postulaciones.html" },
        { page: "becasotorgadas", text: "Becas otorgadas", icon: "bi-patch-check", href: "pages/becasotorgadas.html" },
        { page: "requisitos", text: "Requisitos", icon: "bi-card-checklist", href: "pages/requisitos.html" },
        { page: "reglas", text: "Reglas", icon: "bi-rulers", href: "pages/reglas.html" },
        { page: "reportesbecas", text: "Reportes de becas", icon: "bi-graph-up", href: "pages/reportesbecas.html" },
        { page: "auditoria", text: "Auditoría", icon: "bi-shield-check", href: "pages/auditoria.html" },
      ],
    },
    {
      section: "Gestión de bienestar",
      items: [
        { page: "citas", text: "Citas", icon: "bi-calendar-event", href: "pages/citas.html" },
        { page: "atenciones", text: "Atenciones", icon: "bi-clipboard2-pulse", href: "pages/atenciones.html" },
        { page: "fichas", text: "Fichas psicológicas", icon: "bi-journal-medical", href: "pages/fichas.html" },
        { page: "servicios", text: "Servicios", icon: "bi-heart-pulse", href: "pages/servicios.html" },
        { page: "personal", text: "Personal", icon: "bi-person-badge", href: "pages/personal.html" },
        { page: "reportesbienestar", text: "Reportes de bienestar", icon: "bi-graph-up", href: "pages/reportesbienestar.html" },
      ],
    },
  ];

  function navItem(item) {
    if (!item.href) {
      return `
        <span class="nav-item-link disabled" title="Disponible próximamente">
          <i class="bi ${item.icon}"></i><span>${item.text}</span>
          <i class="bi bi-clock badge-soon" aria-label="Próximamente"></i>
        </span>`;
    }
    const active = item.page === page;
    return `
      <a class="nav-item-link ${active ? "active" : ""}" href="${base}${item.href}" ${active ? 'aria-current="page"' : ""}>
        <i class="bi ${item.icon}"></i><span>${item.text}</span>
      </a>`;
  }

  const visibles = NAV.filter((grupo) => (grupo.section === "Estudiante") === !esadmin);
  const navHtml = visibles.map(
    (group) => `<div class="nav-section">${group.section}</div>${group.items.map(navItem).join("")}`
  ).join("");

  document.body.insertAdjacentHTML(
    "afterbegin",
    `
    <aside class="sidebar" aria-label="Navegación">
      <a class="brand" href="${base}${inicio}">
        <img src="${base}img/udhescudo.png" alt="Escudo de la Universidad de Huánuco">
        <div><b>UDH</b><small>Universidad de Huánuco</small></div>
      </a>
      <nav class="sidebar-nav">${navHtml}</nav>
    </aside>
    <div class="sidebar-backdrop"></div>`
  );

  const iniciales = esadmin
    ? "AD"
    : [sesion.nombre.split(/[ ,]+/)[0], sesion.nombre.split(/[ ,]+/).at(-1)].map((p) => p[0]).join("").toUpperCase();

  const appMain = document.createElement("div");
  appMain.className = "app-main";
  appMain.innerHTML = `
    <header class="topbar">
      <button class="icon-btn menu-btn" id="btn-menu" aria-label="Abrir menú"><i class="bi bi-list"></i></button>
      <div class="crumb">
        <a href="${base}${inicio}" aria-label="Inicio"><i class="bi bi-house-door"></i></a>
        ${section ? `<span>/</span><span>${section}</span>` : ""}
        <span>/</span><b>${title ?? ""}</b>
      </div>
      <div class="sp"></div>
      <button class="icon-btn" id="btn-tema"></button>
      ${esadmin ? "" : `<a class="icon-btn" href="${base}pages/inicioestudiante.html#avisos" aria-label="Avisos" title="Avisos"><i class="bi bi-bell"></i></a>`}
      <a class="user-pill text-reset text-decoration-none" href="${base}pages/perfil.html" title="Mi perfil">
        <span class="avatar-round">${iniciales}</span>
        <div><b>${sesion.nombre}</b><small>${esadmin ? "Bienestar Universitario" : "Estudiante"}</small></div>
      </a>
      <button class="icon-btn" id="btn-salir" aria-label="Cerrar sesión" title="Cerrar sesión">
        <i class="bi bi-box-arrow-right"></i>
      </button>
    </header>`;

  const main = document.querySelector("main");
  main.classList.add("app-content");
  main.insertAdjacentHTML(
    "afterbegin",
    `<div class="page-head">
      <div>
        <h1>${title ?? ""}</h1>
        ${description ? `<p>${description}</p>` : ""}
      </div>
    </div>`
  );
  const actions = main.querySelector(".page-actions");
  if (actions) main.querySelector(".page-head").appendChild(actions);

  document.querySelector(".sidebar-backdrop").after(appMain);
  appMain.appendChild(main);

  const btnTema = document.getElementById("btn-tema");
  const pintarBotonTema = () => {
    const oscuro = window.tema.actual() === "dark";
    btnTema.innerHTML = `<i class="bi ${oscuro ? "bi-sun" : "bi-moon"}"></i>`;
    btnTema.setAttribute("aria-label", oscuro ? "Cambiar a modo claro" : "Cambiar a modo oscuro");
    btnTema.title = btnTema.getAttribute("aria-label");
  };
  pintarBotonTema();
  btnTema.addEventListener("click", () => {
    window.tema.alternar();
    pintarBotonTema();
  });

  document.getElementById("btn-salir").addEventListener("click", () => window.acceso.salir());

  const toggleMenu = () => document.body.classList.toggle("sidebar-open");
  document.getElementById("btn-menu").addEventListener("click", toggleMenu);
  document.querySelector(".sidebar-backdrop").addEventListener("click", toggleMenu);
})();
