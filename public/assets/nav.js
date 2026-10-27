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
  };
  let cache = null;
  try { cache = JSON.parse(sessionStorage.getItem("boceto-yo") || "null"); } catch (e) {}
  if (cache && Date.now() - cache.t < 5 * 60000) { pintar(cache.yo); return; }
  const fuente = window.bocetoSync ? window.bocetoSync.ready : fetch("/api/yo", { cache: "no-store" }).then((r) => r.json());
  Promise.resolve(fuente).then((yo) => {
    try { sessionStorage.setItem("boceto-yo", JSON.stringify({ t: Date.now(), yo: { ingresado: !!yo.ingresado, nombre: yo.nombre, email: yo.email, foto: yo.foto } })); } catch (e) {}
    pintar(yo);
  }).catch(() => {});
})();
