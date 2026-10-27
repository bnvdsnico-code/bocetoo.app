// Panel del alumno: arma todo con su avance real (cuenta de Google + lo guardado en el navegador).
(async () => {
  "use strict";
  const CARRERAS = ["interiores", "industrial", "grafico", "indumentaria"];
  const C = {
    interiores: { n: "Interiores y Mobiliario", corto: "Interiores", col: "#C2410C", soft: "#FDBA8C" },
    industrial: { n: "Diseño Industrial", corto: "Industrial", col: "#1D4ED8", soft: "#93C5FD" },
    grafico: { n: "Diseño Gráfico", corto: "Gráfico", col: "#6D28D9", soft: "#C4A8FA" },
    indumentaria: { n: "Diseño de Indumentaria", corto: "Indumentaria", col: "#BE185D", soft: "#F9A8D4" }
  };
  const $ = (id) => document.getElementById(id);
  const get = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k) || "null"); return v == null ? d : v; } catch (e) { return d; } };
  const el = (tag, css, text) => { const n = document.createElement(tag); if (css) n.style.cssText = css; if (text != null) n.textContent = text; return n; };
  const semanaDe = (cid) => Number(cid.slice(1, 3));
  const diaDe = (cid) => Number(cid.slice(4));

  // 1. Cuenta
  let yo = { ingresado: false };
  try { yo = window.bocetoSync ? await window.bocetoSync.ready : await fetch("/api/yo", { cache: "no-store" }).then((r) => r.json()); } catch (e) {}
  if (!yo.ingresado && yo.googleListo) { location.replace("/acceso.html?volver=/panel.html"); return; }
  const activas = yo.carreras || [];
  if (yo.ingresado) {
    const nombre = (yo.nombre || yo.email.split("@")[0]).trim();
    $("saludo").textContent = "Hola, " + nombre.split(" ")[0];
    $("cuentaNombre").textContent = nombre;
    $("cuentaInicial").textContent = nombre.charAt(0).toUpperCase();
    $("cuentaPlan").textContent = activas.length === 4 ? "Todas las diplomaturas" : activas.length ? activas.map((x) => C[x].corto).join(" · ") : "Sin diplomatura activa";
    $("cuenta").href = "/acceso.html";
    $("cuenta").title = "Tu cuenta: " + yo.email;
  }

  // 2. Avance
  const hechas = {}; CARRERAS.forEach((c) => { hechas[c] = new Set(get("boceto-progreso-" + c, [])); });
  const entregas = Object.values(get("boceto-entregas", {})).filter((e) => e && e.clase && C[e.carrera]);
  const ultima = get("boceto-ultima", null);
  const mias = CARRERAS.filter((c) => activas.includes(c) || hechas[c].size || entregas.some((e) => e.carrera === c));
  let principal = ultima && C[ultima.carrera] && (mias.includes(ultima.carrera) || !mias.length) ? ultima.carrera : (activas[0] || mias[0] || null);
  if (principal && !mias.includes(principal)) mias.unshift(principal);

  const [indice, ...listas] = await Promise.all([
    fetch("/assets/cursos.json").then((r) => r.json()).catch(() => ({})),
    ...mias.map((c) => fetch(`/cursos/${c}/consignas.json`).then((r) => r.json()).catch(() => ({})))
  ]);
  const clases = {}; mias.forEach((c, i) => { clases[c] = listas[i]; });
  const orden = (c) => Object.keys(clases[c] || {});
  const siguiente = (c) => orden(c).find((k) => !hechas[c].has(k)) || null;
  const pct = (c) => Math.round((hechas[c].size / (orden(c).length || 80)) * 100);
  const entregada = (c, k) => entregas.some((e) => e.carrera === c && e.clase === k && e.e);
  const urlClase = (c, k) => (clases[c][k] && clases[c][k].u) || `/cursos/${c}/semana-${k.slice(1, 3)}/clase-${diaDe(k)}.html`;
  const conBarra = (c, alto, full, half, empty) => {
    const spans = [];
    for (let w = 1; w <= 16; w++) {
      const n = [1, 2, 3, 4, 5].filter((d) => hechas[c].has(`s${String(w).padStart(2, "0")}d${d}`)).length;
      spans.push(el("span", `height: ${alto}px; border-radius: ${alto / 2}px; background: ${n === 5 ? full : n ? half : empty}`));
    }
    return spans;
  };

  // 3. Seguí donde dejaste
  let proxima = null;
  if (principal) {
    let k = siguiente(principal);
    if (ultima && ultima.carrera === principal && clases[principal][ultima.clase] && !hechas[principal].has(ultima.clase)) k = ultima.clase;
    proxima = k;
    const c = C[principal];
    $("seguirBox").style.background = c.col;
    $("seguirBar").replaceChildren(...conBarra(principal, 8, "#FFFFFF", c.soft, "rgba(0,0,0,0.22)"));
    if (!k) {
      $("seguirKick").textContent = "Diplomatura terminada";
      $("seguir").textContent = "¡Completaste " + c.n + "!";
      $("seguirMeta").textContent = "Hiciste las 80 clases. Repasá lo que quieras desde el programa.";
      $("seguirPaso").textContent = "16 semanas de 16 · 100%";
      $("seguirCta").textContent = "Ver el programa"; $("seguirCta").href = `/cursos/${principal}/programa.html`;
    } else {
      const it = clases[principal][k], w = semanaDe(k);
      const sinAcceso = yo.ingresado && !activas.includes(principal) && k !== "s01d1";
      $("seguirKick").textContent = hechas[principal].size ? "Seguí donde dejaste" : "Tu próxima clase";
      $("seguir").textContent = it.t;
      $("seguirMeta").textContent = `${c.n} · Semana ${w} · ${(indice[principal] && indice[principal].semanas[w]) || ""}`.replace(/ · $/, "");
      $("seguirPaso").textContent = `Semana ${w} de 16 · clase ${diaDe(k)} de 5 · ${pct(principal)}% de la diplomatura`;
      if (sinAcceso) {
        $("seguirPaso").textContent += " · para seguir necesitás suscribirte";
        $("seguirCta").textContent = "Suscribirme para seguir"; $("seguirCta").href = `/inscripcion.html?plan=diplomatura&carrera=${principal}`;
      } else {
        $("seguirCta").textContent = hechas[principal].size ? "Seguir aprendiendo" : "Empezar la clase"; $("seguirCta").href = urlClase(principal, k);
      }
    }
  } else {
    $("seguirKick").textContent = "Empezá por acá";
    $("seguir").textContent = "La primera clase de cada diplomatura es gratis";
    $("seguirMeta").textContent = "Elegí una abajo y probala. Cuando te suscribas, acá vas a ver tu avance.";
    $("seguirBar").remove(); $("seguirPaso").remove();
    $("seguirCta").textContent = "Ver planes"; $("seguirCta").href = "/inscripcion.html";
  }

  // 4. Entregas
  const lista = $("entregasLista");
  const tarjeta = (href, tag, tagCol, bg, titulo, sub) => {
    const a = el("a", `text-decoration: none; display: flex; flex-direction: column; gap: 6px; padding: 16px; border-radius: 18px; background: ${bg}`);
    a.href = href;
    a.append(el("span", `font-size: 12px; font-weight: 700; letter-spacing: 0.06em; color: ${tagCol}`, tag), el("span", "font-size: 16px; font-weight: 600", titulo), el("span", "font-size: 14px; color: #3A3A3A", sub));
    return a;
  };
  let pendiente = null;
  if (principal && proxima) pendiente = orden(principal).find((k) => clases[principal][k].e && !entregada(principal, k) && !hechas[principal].has(k)) || null;
  if (pendiente) {
    const it = clases[principal][pendiente];
    lista.append(tarjeta(urlClase(principal, pendiente), "○ PRÓXIMA ENTREGA", "#3A3A3A", "#F3F3F1", it.t, `${C[principal].corto} · ${it.k}`));
  }
  entregas.slice().sort((a, b) => String(b.fecha).localeCompare(String(a.fecha))).slice(0, pendiente ? 3 : 4).forEach((e) => {
    const pend = e.corregir > 0, sin = e.corregir == null;
    const [tag, bg, ink] = !e.e ? ["○ PRÁCTICA GUARDADA", "#F3F3F1", "#3A3A3A"] : pend ? ["! PARA CORREGIR", "#FFF1E6", "#9A3412"] : sin ? ["● ENTREGADA · SIN CORRECCIÓN", "#F3F3F1", "#3A3A3A"] : ["✓ CORREGIDA", "#E7F0FF", "#1E3A8A"];
    const sub = `${C[e.carrera].corto} · ${e.k}` + (e.e && pend ? ` · ${e.corregir} ${e.corregir === 1 ? "ajuste" : "ajustes"}` : e.e && sin ? " · pedí la corrección" : "");
    lista.append(tarjeta(`/bocetador/?carrera=${e.carrera}&clase=${e.clase}`, tag, ink, bg, e.t, sub));
  });
  if (!lista.children.length) lista.append(el("p", "margin: 0; font-size: 15px; line-height: 1.5; color: #555555", "Cuando hagas un ejercicio en el Bocetador y lo entregues, aparece acá con su corrección."));

  // 5. Tu semana de estudio: las próximas 5 clases, de lunes a viernes a las 19
  const DIAS = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"];
  const plan = principal && proxima ? orden(principal).filter((k) => !hechas[principal].has(k) && orden(principal).indexOf(k) >= orden(principal).indexOf(proxima)).slice(0, 5) : [];
  const grid = $("semanaGrid");
  const sesiones = [];
  DIAS.forEach((d, i) => {
    const col = el("div", "border-radius: 16px; background: #F7F6F4; padding: 14px; display: flex; flex-direction: column; gap: 10px; min-height: 150px");
    col.append(el("span", "font-size: 13px; font-weight: 700", d));
    const k = plan[i];
    if (i < 5 && k) {
      const it = clases[principal][k];
      const box = el("a", `text-decoration: none; background: ${it.e ? "#FFF1E6" : "#FFFFFF"}; border-left: 4px solid ${C[principal].col}; border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 4px`);
      box.href = urlClase(principal, k);
      box.append(el("span", `font-size: 12px; ${it.e ? "font-weight: 700; color: #9A3412" : "color: #555555"}`, it.e ? "19:00 · CON ENTREGA" : "19:00 · 1 hora"), el("span", "font-size: 13px; font-weight: 600; line-height: 1.3", it.t));
      col.append(box);
      sesiones.push({ day: i + 1, h: 19, m: 0, dur: 60, title: `${it.t} (${C[principal].corto} · ${it.k})`, url: urlClase(principal, k) });
    } else if (i === 5 && plan.length) {
      const box = el("div", "background: #FFFFFF; border-left: 4px solid #111111; border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 4px");
      box.append(el("span", "font-size: 12px; color: #555555", "10:00 · 20 min"), el("span", "font-size: 13px; font-weight: 600; line-height: 1.3", "Repaso de la semana con el asistente"));
      col.append(box);
      sesiones.push({ day: 6, h: 10, m: 0, dur: 20, title: "Repaso de la semana con el asistente", url: "/panel.html#asistente" });
    } else col.append(el("span", "font-size: 13px; color: #555555", "Libre"));
    grid.append(col);
  });
  window.BOCETO_SESIONES = sesiones;
  if (!sesiones.length) {
    $("semanaBajada").textContent = principal ? "Terminaste todas las clases: no hay nada pendiente esta semana." : "Cuando empieces una diplomatura, acá te armamos la semana con tus próximas clases.";
    $("calBoton").hidden = true; $("calBoton").style.display = "none";
  }

  // 6. Mis diplomaturas
  const cursos = $("cursosGrid");
  CARRERAS.forEach((c) => {
    const mia = mias.includes(c), activa = activas.includes(c);
    if (mia) {
      const a = el("a", "text-decoration: none; border: 1.5px solid #E2E2E2; border-radius: 22px; padding: 22px; display: flex; flex-direction: column; gap: 14px");
      a.href = `/cursos/${c}/programa.html`;
      const k = siguiente(c);
      const bar = el("span", "display: grid; grid-template-columns: repeat(16, minmax(0, 1fr)); gap: 3px"); bar.setAttribute("aria-hidden", "true");
      bar.append(...conBarra(c, 6, C[c].col, C[c].soft, "#E2E2E2"));
      a.append(el("span", `align-self: flex-start; font-size: 12px; font-weight: 600; color: #FFFFFF; background: ${C[c].col}; padding: 5px 12px; border-radius: 999px`, C[c].corto),
               el("span", "font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 20px; line-height: 1.2", (indice[c] && indice[c].titulo) || C[c].n), bar,
               el("span", "font-size: 14px; color: #555555", (k ? `Semana ${semanaDe(k)} de 16` : "Terminada") + ` · ${pct(c)}%` + (yo.ingresado && !activa ? " · sin suscripción activa" : "")));
      cursos.append(a);
    } else {
      const a = el("a", "text-decoration: none; border: 1.5px dashed #CFCFCF; border-radius: 22px; padding: 22px; display: flex; flex-direction: column; gap: 14px; background: #FAFAFA");
      const sumar = activas.length > 0;
      a.href = sumar ? `/inscripcion.html?plan=diplomatura&carrera=${c}` : `/cursos/${c}/semana-01/clase-1.html`;
      a.append(el("span", `font-size: 13px; font-weight: 600; color: ${C[c].col}`, sumar ? "Sumala a tu plan" : "Primera clase gratis"),
               el("span", "font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 20px; line-height: 1.2", (indice[c] && indice[c].titulo) || C[c].n),
               el("span", "font-size: 14px; line-height: 1.5; color: #3A3A3A", sumar ? "Con el plan Todas las diplomaturas tenés las cuatro." : "Probala sin suscribirte."));
      cursos.append(a);
    }
  });

  // 7. Portfolio
  const port = $("portfolioGrid");
  entregas.filter((e) => e.img).sort((a, b) => String(b.fecha).localeCompare(String(a.fecha))).slice(0, 6).forEach((e) => {
    const f = el("figure", "margin: 0; display: flex; flex-direction: column; gap: 10px");
    const a = el("a", "display: block; aspect-ratio: 4 / 3; border-radius: 18px; background: #FFFFFF; border: 1px solid #E2E2E2; overflow: hidden");
    a.href = `/bocetador/?carrera=${e.carrera}&clase=${e.clase}`;
    const img = el("img", "display: block; width: 100%; height: 100%; object-fit: contain"); img.src = e.img; img.alt = `Tu trabajo: ${e.t}`; img.loading = "lazy";
    a.append(img);
    const cap = el("figcaption", "display: flex; flex-direction: column; gap: 2px");
    cap.append(el("span", "font-size: 15px; font-weight: 600", e.t), el("span", "font-size: 13px; color: #555555", `${C[e.carrera].corto} · ${e.k}`));
    f.append(a, cap); port.append(f);
  });
  if (!port.children.length) {
    const f = el("a", "aspect-ratio: 4 / 3; border-radius: 18px; border: 1.5px dashed #CFCFCF; display: flex; align-items: center; justify-content: center; text-align: center; padding: 14px; box-sizing: border-box; font-size: 14px; color: #555555; text-decoration: none", "Tu primera entrega del Bocetador aparece acá");
    f.href = principal ? `/bocetador/?carrera=${principal}` : "/bocetador/";
    port.append(f);
  }

  // 8. Resumen bajo el saludo
  $("resumen").textContent = !principal ? "Probá gratis la primera clase de cualquier diplomatura."
    : !proxima ? `Terminaste ${C[principal].n}.`
    : `Vas por la semana ${semanaDe(proxima)} de ${C[principal].n}` + (pendiente ? " y tenés una entrega por delante." : ".");
})();
