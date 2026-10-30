// Encabezado común: menú en celular, borde al hacer scroll y estado de la cuenta (Ingresar / Mi panel).
(() => {
  "use strict";
  const head = document.querySelector(".s-head");
  if (!head) return;
  const nav = head.querySelector(".s-nav"), burger = head.querySelector(".s-burger");
  if (burger && nav) {
    burger.addEventListener("click", () => {
      const open = burger.getAttribute("aria-expanded") !== "true";
      burger.setAttribute("aria-expanded", String(open)); nav.classList.toggle("open", open);
    });
    nav.addEventListener("click", (e) => { if (e.target.closest("a")) { burger.setAttribute("aria-expanded", "false"); nav.classList.remove("open"); } });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && nav.classList.contains("open")) { burger.click(); burger.focus(); } });
  }
  const onScroll = () => head.classList.toggle("scrolled", window.scrollY > 4);
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // Link activo
  const here = location.pathname.replace(/\.html$/, "").replace(/\/$/, "") || "/";
  head.querySelectorAll(".s-nav a").forEach((a) => {
    const p = new URL(a.href, location.href).pathname.replace(/\.html$/, "").replace(/\/$/, "") || "/";
    if (p !== "/" && here.startsWith(p)) a.setAttribute("aria-current", "page");
  });

  // Sesión: guardada unos minutos para no consultar en cada página
  const pintar = (yo) => {
    if (!yo || !yo.ingresado) return;
    head.querySelectorAll("[data-anon]").forEach((n) => { n.hidden = true; });
    const me = head.querySelector("[data-user]");
    if (!me) return;
    me.hidden = false;
    const nombre = (yo.nombre || yo.email || "").trim();
    const av = me.querySelector(".s-av");
    if (av) {
      if (yo.foto && /^https:\/\/[a-z0-9.-]+\.googleusercontent\.com\//.test(yo.foto)) {
        const img = document.createElement("img"); img.src = yo.foto; img.alt = ""; img.referrerPolicy = "no-referrer";
        img.onerror = () => { av.textContent = nombre.charAt(0).toUpperCase(); };
        av.replaceChildren(img);
      } else av.textContent = nombre.charAt(0).toUpperCase();
    }
    me.title = yo.email || "";
    armarMenu(me, nombre, yo.email || "");
  };
  // Menú de la cuenta: Mi panel, Bocetador y Salir de la cuenta
  const salir = () => { try { sessionStorage.removeItem("boceto-yo"); } catch (e) {} location.href = "/auth/salir"; };
  function armarMenu(me, nombre, email) {
    if (me.dataset.menu) return; me.dataset.menu = "1";
    const caja = me.parentNode; caja.classList.add("s-acc-rel");
    const menu = document.createElement("div"); menu.className = "s-menu"; menu.id = "menuCuenta"; menu.setAttribute("role", "menu"); menu.hidden = true;
    const h = document.createElement("div"); h.className = "s-menu-h";
    const b = document.createElement("b"); b.textContent = nombre; const sm = document.createElement("small"); sm.textContent = email; h.append(b, sm);
    const item = (txt, href) => { const a = document.createElement(href ? "a" : "button"); a.setAttribute("role", "menuitem"); a.textContent = txt; if (href) a.href = href; else a.type = "button"; a.tabIndex = -1; return a; };
    const out = item("Salir de la cuenta"); out.classList.add("s-menu-salir"); out.addEventListener("click", salir);
    menu.append(h, item("Mi panel", "/panel.html"), item("Bocetador", "/bocetador/"), out);
    caja.appendChild(menu);
    me.setAttribute("aria-haspopup", "menu"); me.setAttribute("aria-controls", "menuCuenta"); me.setAttribute("aria-expanded", "false");
    const items = () => [...menu.querySelectorAll("[role=menuitem]")];
    const abrir = (si, foco) => { menu.hidden = !si; me.setAttribute("aria-expanded", String(si)); if (si && foco) items()[0].focus(); };
    me.addEventListener("click", (e) => { e.preventDefault(); abrir(menu.hidden, e.detail === 0); });
    me.addEventListener("keydown", (e) => { if (e.key === "ArrowDown") { e.preventDefault(); abrir(true, true); } });
    menu.addEventListener("keydown", (e) => {
      const l = items(), i = l.indexOf(document.activeElement);
      if (e.key === "Escape") { abrir(false); me.focus(); }
      else if (e.key === "ArrowDown") { e.preventDefault(); l[(i + 1) % l.length].focus(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); l[(i - 1 + l.length) % l.length].focus(); }
      else if (e.key === "Tab") abrir(false);
    });
    document.addEventListener("click", (e) => { if (!menu.hidden && !caja.contains(e.target)) abrir(false); });
  }
  document.querySelectorAll("[data-salir]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); salir(); }));
  let cache = null;
  try { cache = JSON.parse(sessionStorage.getItem("boceto-yo") || "null"); } catch (e) {}
  if (cache && Date.now() - cache.t < 5 * 60000) { pintar(cache.yo); return; }
  const fuente = window.bocetoSync ? window.bocetoSync.ready : fetch("/api/yo", { cache: "no-store" }).then((r) => r.json());
  Promise.resolve(fuente).then((yo) => {
    try { sessionStorage.setItem("boceto-yo", JSON.stringify({ t: Date.now(), yo: { ingresado: !!yo.ingresado, nombre: yo.nombre, email: yo.email, foto: yo.foto } })); } catch (e) {}
    pintar(yo);
  }).catch(() => {});
})();
