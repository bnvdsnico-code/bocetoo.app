// Portada: la lámina es una mini demo del Bocetador. Cada disciplina tiene una pieza
// para corregir arrastrándola (mouse, dedo o flechas del teclado).
(() => {
  "use strict";
  const lam = document.querySelector(".lamina");
  if (!lam) return;
  const tabs = [...lam.querySelectorAll("[data-lamina]")];
  const nota = lam.querySelector(".nota");
  const notaT = lam.querySelector("[data-nota-t]");
  const notaN = lam.querySelector("[data-nota-n]");
  const notaA = lam.querySelector("[data-nota-a]");
  const svg = (c) => lam.querySelector(`[data-dib="${c}"]`);
  const $ = (c, sel) => svg(c).querySelector(sel);
  const PXCM = 374 / 400; // la planta mide 4 m en 374 unidades

  // Cada demo: valor inicial, rango, paso de teclado, si está bien y cómo se dibuja
  const demos = {
    interiores: {
      v: 250, min: 112, max: 280, paso: 4,
      ok: (v) => { const cm = (404 - (v + 112)) / PXCM; return cm >= 85 && cm <= 110; },
      snap: (v) => v,
      pintar(v) {
        $("interiores", "[data-arr]").setAttribute("transform", `translate(${v - 250} 0)`);
        const x1 = v + 112, x2 = 404, cm = Math.round((x2 - x1) / PXCM);
        $("interiores", "[data-medida-l]").setAttribute("d", `M${x1} 240H${x2} M${x1} 232v16 M${x2} 232v16`);
        const t = $("interiores", "[data-medida-t]");
        t.setAttribute("x", (x1 + x2) / 2); t.setAttribute("y", 202); t.textContent = cm + " cm";
        return { x: (x1 + x2) / 2, y: 160, cm };
      },
      texto: (r, ok) => ok ? `¡Bien! Quedan ${r.cm} cm de paso: ya se circula cómodo entre la mesa y la butaca.`
        : r.cm < 85 ? `Entre la mesa ratona y la butaca quedan ${r.cm} cm: el paso mínimo es de 90 cm. Arrastrá la mesa hacia la izquierda.`
        : `Ahora quedan ${r.cm} cm de paso, de más: la mesa queda lejos del sillón. Acercala un poco.`
    },
    industrial: {
      v: 276, min: 160, max: 320, paso: 3,
      ok: (v) => Math.abs(v - 225) <= 6,
      snap: (v) => (Math.abs(v - 225) <= 6 ? 225 : v),
      pintar(v) {
        $("industrial", "[data-esq-l]").setAttribute("d", `M280 330L410 ${v} M410 146V${v}`);
        $("industrial", "[data-arr]").setAttribute("transform", `translate(0 ${v - 276})`);
        return { x: 452, y: v };
      },
      texto: (r, ok) => ok ? "¡Eso! Las dos aristas de abajo fugan al mismo punto y la caja se apoya bien."
        : "La arista de abajo no va al punto de fuga de la derecha: arrastrá la esquina hasta la línea azul."
    },
    grafico: {
      v: 26, min: -20, max: 60, paso: 2,
      ok: (v) => Math.abs(v) <= 3,
      snap: (v) => (Math.abs(v) <= 3 ? 0 : v),
      pintar(v) {
        $("grafico", "[data-arr]").setAttribute("transform", `translate(${v} 0)`);
        return { x: 150, y: 214 };
      },
      texto: (r, ok) => ok ? "Alineado. El titular y el texto comparten el mismo margen y el afiche se ordena."
        : "El titular se sale de la retícula: arrastralo hasta la primera columna, la misma del texto."
    },
    indumentaria: {
      v: 196, min: 110, max: 250, paso: 3,
      ok: (v) => Math.abs(v - 150) <= 6,
      snap: (v) => (Math.abs(v - 150) <= 6 ? 150 : v),
      pintar(w) {
        $("indumentaria", "[data-vestido]").setAttribute("d",
          `M250 92C254 ${w - 30} 262 ${w - 8} 264 ${w}L296 ${w}C298 ${w - 8} 306 ${w - 30} 310 92 M264 ${w}L232 300Q280 312 328 300L296 ${w}`);
        $("indumentaria", "[data-cint]").setAttribute("y", w - 3.5);
        $("indumentaria", "[data-cint]").setAttribute("x", 256);
        $("indumentaria", "[data-cint]").setAttribute("width", 48);
        $("indumentaria", "[data-cint-z]").setAttribute("y", w - 14);
        return { x: 362, y: w };
      },
      texto: (r, ok) => ok ? "¡Muy bien! La cintura cae al final de la cabeza 3 y el figurín gana proporción."
        : "La cintura quedó baja y la figura se ve achatada: subí el cinturón hasta el final de la cabeza 3."
    }
  };

  let actual = "interiores", auto = null;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const actualizar = (c) => {
    const d = demos[c];
    const r = d.pintar(d.v);
    const ok = d.ok(d.v);
    const s = svg(c);
    s.classList.toggle("ok", ok);
    s.querySelector("[data-marca]").setAttribute("transform", `translate(${r.x} ${r.y})`);
    s.querySelector("[data-marca-n]").textContent = ok ? "✓" : "1";
    const arr = s.querySelector("[data-arr]");
    arr.setAttribute("aria-valuenow", String(Math.round(((d.v - d.min) / (d.max - d.min)) * 100)));
    arr.setAttribute("aria-valuetext", d.texto(r, ok));
    if (c !== actual) return;
    nota.classList.toggle("ok", ok);
    notaN.textContent = ok ? "✓" : "1";
    notaT.textContent = d.texto(r, ok);
    notaA.hidden = !ok;
    notaA.href = `/bocetador/?carrera=${c}`;
  };

  const mostrar = (c, foco) => {
    actual = c;
    tabs.forEach((t) => { const on = t.dataset.lamina === c; t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1; if (on && foco) t.focus(); });
    lam.querySelectorAll("[data-dib]").forEach((s) => s.toggleAttribute("hidden", s.dataset.dib !== c));
    nota.style.setProperty("--nota", `var(--${c})`);
    actualizar(c);
    lam.classList.remove("anim"); void lam.offsetWidth; lam.classList.add("anim");
  };
  const parar = () => { if (auto) { clearInterval(auto); auto = null; } };

  // Arrastre
  Object.keys(demos).forEach((c) => {
    const d = demos[c], s = svg(c), arr = s.querySelector("[data-arr]");
    const horizontal = c === "interiores" || c === "grafico";
    const punto = (e) => { const p = new DOMPoint(e.clientX, e.clientY).matrixTransform(s.getScreenCTM().inverse()); return horizontal ? p.x : p.y; };
    let ini = null;
    const mover = (v) => { d.v = Math.min(d.max, Math.max(d.min, v)); actualizar(c); };
    arr.addEventListener("pointerdown", (e) => {
      e.preventDefault(); parar(); lam.classList.remove("anim"); s.classList.add("tocado");
      arr.setPointerCapture(e.pointerId); ini = { p: punto(e), v: d.v }; arr.classList.add("arrastrando");
    });
    arr.addEventListener("pointermove", (e) => { if (ini) mover(ini.v + punto(e) - ini.p); });
    const soltar = () => { if (!ini) return; ini = null; arr.classList.remove("arrastrando"); mover(d.snap(d.v)); };
    arr.addEventListener("pointerup", soltar);
    arr.addEventListener("pointercancel", soltar);
    arr.addEventListener("keydown", (e) => {
      const mas = horizontal ? "ArrowRight" : "ArrowDown", menos = horizontal ? "ArrowLeft" : "ArrowUp";
      let v = null;
      if (e.key === mas || e.key === (horizontal ? "ArrowDown" : "ArrowRight")) v = d.v + d.paso;
      else if (e.key === menos || e.key === (horizontal ? "ArrowUp" : "ArrowLeft")) v = d.v - d.paso;
      else if (e.key === "Home") v = d.min; else if (e.key === "End") v = d.max;
      if (v === null) return;
      e.preventDefault(); parar(); s.classList.add("tocado"); mover(d.snap(v));
    });
    arr.addEventListener("focus", parar);
  });

  tabs.forEach((t, i) => {
    t.addEventListener("click", () => { parar(); mostrar(t.dataset.lamina); });
    t.addEventListener("keydown", (e) => {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      e.preventDefault(); parar();
      const j = (i + (e.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
      mostrar(tabs.at(j).dataset.lamina, true);
    });
  });
  Object.keys(demos).forEach(actualizar);
  mostrar("interiores");
  // Rota sola mientras nadie la toca (salvo con movimiento reducido)
  if (!reduce) {
    auto = setInterval(() => {
      if (document.hidden) return;
      const i = tabs.findIndex((t) => t.dataset.lamina === actual);
      mostrar(tabs.at((i + 1) % tabs.length).dataset.lamina);
    }, 9000);
    lam.addEventListener("pointerenter", parar, { once: true });
    lam.addEventListener("focusin", parar, { once: true });
  }
})();
