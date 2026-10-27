// Sincroniza el progreso del navegador con la cuenta del alumno (si ingresó con Google).
// En el navegador: "boceto-progreso-<carrera>" (clases completadas), "boceto-entregas" y "boceto-ultima".
// window.bocetoSync.ready → se resuelve con /api/yo cuando ya está todo combinado.
(() => {
  "use strict";
  const CARRERAS = ["interiores", "industrial", "grafico", "indumentaria"];
  const get = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k) || "null"); return v == null ? d : v; } catch (e) { return d; } };
  const set = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } };
  const imgUrl = (c, k) => `/api/progreso/img/${c}/${k}`;
  let yo = null, timer = null;

  // Última clase vista (para "Seguí donde dejaste")
  const b = document.body;
  if (b && b.dataset.curso && b.dataset.clase) set("boceto-ultima", { carrera: b.dataset.curso, clase: b.dataset.clase, fecha: new Date().toISOString() });

  const snapshot = () => {
    const progreso = {};
    CARRERAS.forEach((c) => { progreso[c] = get("boceto-progreso-" + c, []); });
    const entregas = {};
    Object.values(get("boceto-entregas", {})).forEach((e) => { if (e && e.clase) { const { img, ...meta } = e; entregas[`${e.carrera}:${e.clase}`] = meta; } });
    return { progreso, entregas, ultima: get("boceto-ultima", null) };
  };
  const send = () => yo && yo.ingresado
    ? fetch("/api/progreso", { method: "PUT", headers: { "content-type": "application/json" }, body: JSON.stringify(snapshot()), keepalive: true }).catch(() => {})
    : Promise.resolve();
  const sendImg = (c, k, dataUrl) => yo && yo.ingresado && /^data:image\/jpeg;base64,/.test(dataUrl || "")
    ? fetch(imgUrl(c, k), { method: "PUT", body: dataUrl }).then((r) => r.ok).catch(() => false)
    : Promise.resolve(false);

  async function start() {
    try { yo = await fetch("/api/yo", { cache: "no-store" }).then((r) => r.json()); } catch (e) { return { ingresado: false }; }
    if (!yo.ingresado) return yo;
    // Si en este navegador había otra cuenta, no se mezclan los avances.
    const antes = get("boceto-cuenta", null);
    if (antes && antes !== yo.email) {
      CARRERAS.forEach((c) => localStorage.removeItem("boceto-progreso-" + c));
      ["boceto-entregas", "boceto-ultima"].forEach((k) => localStorage.removeItem(k));
    }
    set("boceto-cuenta", yo.email);
    let srv;
    try { srv = await fetch("/api/progreso", { cache: "no-store" }).then((r) => (r.ok ? r.json() : null)); } catch (e) { srv = null; }
    if (!srv) return yo;
    // Clases completadas: se suman las de los dos lados
    CARRERAS.forEach((c) => {
      const all = new Set([...get("boceto-progreso-" + c, []), ...((srv.progreso || {})[c] || [])]);
      set("boceto-progreso-" + c, [...all]);
    });
    // Entregas: gana la más reciente; las que solo están en la cuenta traen su imagen desde el servidor
    const local = get("boceto-entregas", {});
    const subir = [];
    Object.values(srv.entregas || {}).forEach((e) => {
      const l = local[e.clase];
      if (!l || (l.carrera === e.carrera && String(l.fecha) < e.fecha)) local[e.clase] = { ...e, img: e.img ? imgUrl(e.carrera, e.clase) : null };
    });
    Object.values(local).forEach((l) => {
      const s = (srv.entregas || {})[`${l.carrera}:${l.clase}`];
      if (l.img && String(l.img).startsWith("data:") && (!s || !s.img || s.fecha < l.fecha)) subir.push(l);
    });
    set("boceto-entregas", local);
    const su = srv.ultima, lu = get("boceto-ultima", null);
    if (su && (!lu || String(lu.fecha) < su.fecha)) set("boceto-ultima", su);
    await send();
    subir.forEach((l) => sendImg(l.carrera, l.clase, l.img));
    return yo;
  }

  const ready = start();
  window.bocetoSync = {
    ready,
    push() { clearTimeout(timer); timer = setTimeout(send, 400); },
    pushImg: (c, k, dataUrl) => ready.then(() => send()).then(() => sendImg(c, k, dataUrl))
  };
})();
