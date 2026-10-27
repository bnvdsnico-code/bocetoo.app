// Portada: la lámina cambia de disciplina y se vuelve a dibujar.
(() => {
  "use strict";
  const lam = document.querySelector(".lamina");
  if (!lam) return;
  const tabs = [...lam.querySelectorAll("[data-lamina]")];
  const colores = { interiores: "var(--interiores)", industrial: "var(--industrial)", grafico: "var(--grafico)", indumentaria: "var(--indumentaria)" };
  let auto = null, actual = "interiores";
  const mostrar = (c, foco) => {
    actual = c;
    tabs.forEach((t) => { const on = t.dataset.lamina === c; t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1; if (on && foco) t.focus(); });
    lam.querySelectorAll("[data-dib]").forEach((s) => { s.toggleAttribute("hidden", s.dataset.dib !== c); });
    lam.querySelectorAll("[data-nota]").forEach((n) => { n.hidden = n.dataset.nota !== c; });
    lam.querySelector(".nota").style.setProperty("--nota", colores[c]);
    lam.classList.remove("anim"); void lam.offsetWidth; lam.classList.add("anim");
  };
  const parar = () => { if (auto) { clearInterval(auto); auto = null; } };
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => { parar(); mostrar(t.dataset.lamina); });
    t.addEventListener("keydown", (e) => {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      e.preventDefault(); parar();
      const j = (i + (e.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
      mostrar(tabs.at(j).dataset.lamina, true);
    });
  });
  mostrar("interiores");
  // Rota sola mientras nadie la toca (salvo con movimiento reducido)
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    auto = setInterval(() => {
      if (document.hidden) return;
      const i = tabs.findIndex((t) => t.dataset.lamina === actual);
      mostrar(tabs.at((i + 1) % tabs.length).dataset.lamina);
    }, 7000);
    lam.addEventListener("pointerenter", parar, { once: true });
  }
})();
