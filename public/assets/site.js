// Interacciones del sitio: cuestionario, devolución, plan semanal y chat con el asistente.
(() => {
  "use strict";
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const showIf = (name, on) => $$(`[data-if="${name}"]`).forEach((el) => { el.hidden = !on; });

  /* ---------- Cuestionario ---------- */
  const opts = $$(".q-opt");
  if (opts.length) {
    let answer = null;
    opts.forEach((b) => b.addEventListener("click", () => {
      answer = b.dataset.opt;
      opts.forEach((o) => o.setAttribute("aria-pressed", String(o === b)));
      ["needsAnswer", "isCorrect", "isWrong"].forEach((n) => showIf(n, false));
    }));
    $$('[data-action="check"]').forEach((b) => b.addEventListener("click", () => {
      showIf("needsAnswer", !answer);
      showIf("isCorrect", answer === "b");
      showIf("isWrong", !!answer && answer !== "b");
    }));
  }

  /* ---------- Devolución: marcas y observaciones ---------- */
  const notes = $$(".note");
  if (notes.length) {
    const select = (n) => {
      notes.forEach((b) => {
        const on = b.dataset.pick === String(n);
        b.setAttribute("aria-pressed", String(on));
        const body = b.querySelector(".note-body"); if (body) body.hidden = !on;
      });
      for (let i = 1; i <= 4; i++) showIf(`sel${i}`, i === n);
    };
    $$("[data-pick]").forEach((b) => b.addEventListener("click", () => select(Number(b.dataset.pick))));
  }

  /* ---------- Plan semanal y Google Calendar ---------- */
  const calLinks = document.getElementById("calLinks");
  if (calLinks) {
    const SESSIONS = window.BOCETO_SESIONES || [
      { day: 1, h: 19, m: 0, dur: 15, title: "Lección: Zonas de estar, lectura y paso", url: "/aprender/recorridos-y-pasos-libres.html" },
      { day: 3, h: 19, m: 0, dur: 30, title: "Entrega: Diagrama de zonas, versión 2", url: "/aprender/devolucion-diagrama-de-zonas.html" },
      { day: 4, h: 19, m: 0, dur: 15, title: "Lección: El brief, preguntas clave", url: "/cursos/grafico.html" },
      { day: 6, h: 10, m: 0, dur: 45, title: "Ejercicio: brief de una marca real", url: "/cursos/grafico.html" },
      { day: 0, h: 18, m: 0, dur: 10, title: "Repaso con el asistente", url: "/panel.html" }
    ];
    const DAYS = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"];
    const pad = (n) => String(n).padStart(2, "0");
    const stamp = (d) => `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}T${pad(d.getHours())}${pad(d.getMinutes())}00`;
    const tz = (() => { try { return Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) { return ""; } })();
    const nextDate = (s) => {
      const now = new Date(), d = new Date(now);
      d.setHours(s.h, s.m, 0, 0);
      let add = (s.day - now.getDay() + 7) % 7;
      if (add === 0 && d <= now) add = 7;
      d.setDate(d.getDate() + add);
      return d;
    };
    const render = () => {
      calLinks.innerHTML = "";
      (window.BOCETO_SESIONES || SESSIONS).forEach((s) => {
        const start = nextDate(s), end = new Date(start.getTime() + s.dur * 60000);
        const q = new URLSearchParams({
          action: "TEMPLATE", text: `boceto · ${s.title}`, dates: `${stamp(start)}/${stamp(end)}`,
          details: `Sesión de ${s.dur} minutos en boceto.\n${location.origin}${s.url}`
        });
        if (tz) q.set("ctz", tz);
        const a = document.createElement("a");
        a.className = "cal-link"; a.target = "_blank"; a.rel = "noopener";
        a.href = `https://calendar.google.com/calendar/render?${q.toString()}`;
        const b = document.createElement("b"); b.textContent = `+ ${DAYS[s.day]} ${pad(s.h)}:${pad(s.m)}`;
        a.append(b, document.createTextNode(" " + s.title));
        calLinks.appendChild(a);
      });
    };
    let open = false;
    $$('[data-action="toggle-cal"]').forEach((b) => b.addEventListener("click", () => {
      open = !open;
      showIf("connected", open); showIf("notConnected", !open);
      if (open) render();
    }));
  }

  /* ---------- Cuestionarios de las clases ---------- */
  $$("[data-quiz]").forEach((quiz) => {
    const okFb = quiz.querySelector(".fb.ok"), noFb = quiz.querySelector(".fb.no");
    $$(".opt", quiz).forEach((b) => b.addEventListener("click", () => {
      const ok = b.dataset.ok === "1";
      $$(".opt", quiz).forEach((o) => { if (o.dataset.state === "no" || !ok) o.removeAttribute("data-state"); });
      b.dataset.state = ok ? "ok" : "no";
      okFb.hidden = !ok; noFb.hidden = ok;
    }));
  });

  /* ---------- Progreso del curso (en este navegador) ---------- */
  const curso = document.body.dataset.curso;
  if (curso) {
    const KEY = `boceto-progreso-${curso}`;
    const total = Number(document.body.dataset.total) || 80;
    const load = () => { try { return new Set(JSON.parse(localStorage.getItem(KEY) || "[]")); } catch (e) { return new Set(); } };
    const store = (set) => { try { localStorage.setItem(KEY, JSON.stringify([...set])); } catch (e) {} };
    const paint = () => {
      const done = load();
      $$("[data-cid]").forEach((a) => a.classList.toggle("done", done.has(a.dataset.cid)));
      const pct = Math.round((done.size / total) * 100);
      $$("[data-progress-bar]").forEach((b) => { b.style.width = pct + "%"; });
      $$("[data-progress-text]").forEach((t) => { t.textContent = pct + "%"; });
      $$("[data-complete]").forEach((b) => {
        const on = done.has(b.dataset.complete);
        b.setAttribute("aria-pressed", String(on));
        b.textContent = on ? "✓ Clase completada" : "Marcar clase como completada";
      });
      const cont = document.querySelector("[data-continue]");
      if (cont && done.size) {
        const next = $$(".p-week a[data-cid]").find((a) => !done.has(a.dataset.cid));
        if (next) { cont.href = next.getAttribute("href"); cont.textContent = "Seguir donde dejaste"; }
      }
    };
    $$("[data-complete]").forEach((b) => b.addEventListener("click", () => {
      const done = load(), id = b.dataset.complete;
      done.has(id) ? done.delete(id) : done.add(id);
      store(done); paint();
      if (window.bocetoSync) window.bocetoSync.push();
    }));
    paint();
    if (window.bocetoSync) window.bocetoSync.ready.then(paint);
  }

  /* ---------- Entregas hechas en el Bocetador (aviso dentro de la clase) ---------- */
  const fechaCorta = (iso) => { try { return new Date(iso).toLocaleDateString("es-AR", { day: "numeric", month: "numeric" }); } catch (e) { return ""; } };
  const paintEntregas = () => {
    const entregas = (() => { try { return JSON.parse(localStorage.getItem("boceto-entregas") || "{}") || {}; } catch (e) { return {}; } })();
    $$("[data-entrega]").forEach((p) => {
      const e = entregas[p.dataset.entrega];
      if (!e || (curso && e.carrera && e.carrera !== curso)) return;
      p.hidden = false;
      p.textContent = `✓ ${e.e ? "Entregada" : "Guardada"} el ${fechaCorta(e.fecha)}` + (e.corregir ? ` · ${e.corregir} ${e.corregir === 1 ? "punto" : "puntos"} para corregir` : e.corregir === 0 ? " · sin correcciones" : "");
      const a = p.previousElementSibling;
      if (a && a.tagName === "A") a.textContent = e.e ? "Ver o mejorar la entrega →" : "Seguir la práctica en el Bocetador →";
    });
  };
  paintEntregas();
  if (window.bocetoSync) window.bocetoSync.ready.then(paintEntregas);

  /* ---------- Chat con el asistente ---------- */
  const ERRORS = {
    rate_limited: "Hay muchas consultas seguidas. Probá de nuevo en un minuto.",
    ai_unavailable: "El asistente todavía no está activo en este sitio.",
    bad_request: "No pude procesar esa pregunta. Probá escribirla de otra forma.",
    too_large: "La consulta es demasiado larga. Probá con algo más corto."
  };
  // Dentro de una vista de Claude (vista previa) se usa el asistente de Claude directamente.
  const SYSTEM = "Sos el asistente de aprendizaje de boceto, una escuela online de diseño sin profesores (Interiores y Mobiliario, Industrial, Gráfico, Indumentaria). Respondés en español rioplatense, con voseo, cálido, claro y concreto, como un buen docente de taller. Si te piden algo que no es de diseño o de la escuela, volvés al tema con amabilidad. No inventes precios, fechas ni políticas de la escuela.";
  let samplePromise = null;
  const claudeSample = () => samplePromise || (samplePromise = (window.claude && window.claude.use)
    ? Promise.resolve(window.claude.use("sample")).catch(() => null) : Promise.resolve(null));
  async function askAssistant(messages) {
    const sample = await claudeSample();
    if (sample) {
      const turns = messages.map((m, i) => i === 0 ? { role: m.role, content: SYSTEM + "\n\n" + m.content } : m);
      try { const { text } = await sample(turns, { cache: false }); return text; }
      catch (e) {
        const code = e && e.code;
        throw new Error(code === "not_granted" ? "Para usar el asistente tenés que permitirlo." : code === "rate_limited" ? ERRORS.rate_limited : "Se cortó la conexión con el asistente. Probá de nuevo.");
      }
    }
    let res;
    try {
      res = await fetch("/api/asistente", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ messages, maxTokens: 700 }) });
    } catch (e) { throw new Error("No hay conexión. Revisá internet y probá de nuevo."); }
    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.text) throw new Error(ERRORS[data.error] || "Se cortó la conexión con el asistente. Probá de nuevo.");
    return data.text;
  }

  $$('form[data-chat]').forEach((form) => {
    const section = form.closest("section") || document.body;
    const box = section.querySelector("#chat") || document.getElementById("chat");
    const input = form.querySelector('input[type="text"]');
    const send = form.querySelector('button[type="submit"]');
    if (!box || !input) return;
    const bg = getComputedStyle(section).backgroundColor;
    const dark = /rgb\(\s*(\d+),\s*(\d+),\s*(\d+)/.exec(bg);
    box.classList.add(dark && (+dark[1] + +dark[2] + +dark[3]) < 150 ? "dark" : "light");
    const page = (document.querySelector("article") || document.querySelector("main") || document.body).innerText.replace(/\s+\n/g, "\n").slice(0, 5000);
    const turns = [];
    const bubble = (cls, text) => { const p = document.createElement("p"); p.className = `bubble ${cls}`; p.textContent = text; box.appendChild(p); return p; };

    async function submit(text) {
      text = text.trim(); if (!text || send.disabled) return;
      input.value = ""; send.disabled = true;
      bubble("me", text);
      const wait = bubble("ai wait", "Pensando…");
      turns.push({ role: "user", content: text });
      const msgs = turns.map((t, i) => i === 0 ? { role: "user", content: `Esto es lo que el alumno ve en la página de boceto en este momento:\n"""\n${page}\n"""\n\nRespondé en menos de 120 palabras, en texto plano, sin markdown.\n\nPregunta del alumno: ${t.content}` } : t);
      try {
        const answer = await askAssistant(msgs);
        wait.textContent = answer; wait.classList.remove("wait");
        turns.push({ role: "assistant", content: answer });
      } catch (e) {
        wait.textContent = e.message; wait.classList.remove("wait"); wait.classList.add("err");
        turns.pop();
      } finally {
        send.disabled = false; input.focus();
        wait.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }
    }
    form.addEventListener("submit", (e) => { e.preventDefault(); submit(input.value); });
    $$('button[type="button"]', section).forEach((b) => {
      if (b.getAttribute("aria-label") === "Adjuntar imagen") {
        b.addEventListener("click", () => { location.href = "/bocetador/?carrera=" + (document.body.dataset.curso || "interiores"); });
        b.title = "Subí la foto de tu plano en el Bocetador";
      } else {
        b.addEventListener("click", () => submit(b.textContent));
      }
    });
  });
})();
