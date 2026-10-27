// Panel de administración: lee /api/admin/resumen y lo muestra. Solo funciona con una cuenta autorizada.
(() => {
  "use strict";
  const C = {
    interiores: { n: "Interiores", col: "#C2410C" }, industrial: { n: "Industrial", col: "#1D4ED8" },
    grafico: { n: "Gráfico", col: "#6D28D9" }, indumentaria: { n: "Indumentaria", col: "#BE185D" }
  };
  const PLANES = { diplomatura: "Tu diplomatura", todas: "Todas las diplomaturas" };
  const $ = (id) => document.getElementById(id);
  const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
  const pesos = (n) => "$" + Number(n || 0).toLocaleString("es-AR");
  const fecha = (iso, conHora) => {
    if (!iso) return "—";
    try { return new Date(iso).toLocaleString("es-AR", conHora ? { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" } : { day: "numeric", month: "short", year: "numeric" }); } catch (e) { return "—"; }
  };
  const hace = (iso) => {
    if (!iso) return "—";
    const m = Math.round((Date.now() - Date.parse(iso)) / 60000);
    if (m < 60) return `hace ${Math.max(m, 1)} min`;
    const h = Math.round(m / 60); if (h < 48) return `hace ${h} h`;
    return `hace ${Math.round(h / 24)} días`;
  };
  const estado = (s) => ({ authorized: ["Activa", "b-ok"], paused: ["Pausada", "b-warn"], canceled: ["Cancelada", "b-mut"], pending: ["Sin cobrar", "b-info"] }[s] || [s || "—", "b-mut"]);
  let datos = null;

  async function cargar() {
    $("estado").hidden = false; $("estado").textContent = "Cargando…";
    let r;
    try { r = await fetch("/api/admin/resumen", { cache: "no-store" }); } catch (e) { $("estado").textContent = "Sin conexión. Probá de nuevo."; return; }
    if (r.status === 401) { $("estado").innerHTML = 'Ingresá con tu cuenta de Google para ver el panel. <a href="/auth/google?volver=/admin.html">Ingresar con Google</a>'; return; }
    if (r.status === 403) {
      const d = await r.json().catch(() => ({}));
      $("estado").textContent = `La cuenta ${d.email || ""} no tiene acceso al panel de administración.`; return;
    }
    if (!r.ok) { $("estado").textContent = "No se pudo cargar el panel. Probá de nuevo en un rato."; return; }
    datos = await r.json();
    $("estado").hidden = true;
    $("quien").textContent = "Actualizado " + fecha(datos.generado, true);
    pintarKpis(); pintarSolicitudes(); pintarAlumnos();
  }

  function pintarKpis() {
    const t = datos.totales, box = $("kpis");
    box.replaceChildren(); box.hidden = false;
    const kpi = (v, l, d, alerta) => { const k = el("div", "kpi" + (alerta ? " alerta" : "")); k.append(el("span", "v", v), el("span", "l", l)); if (d) k.append(el("span", "d", d)); box.append(k); };
    kpi(String(t.solicitudesPendientes), "Pedidos sin atender", "Baja o arrepentimiento", t.solicitudesPendientes > 0);
    kpi(String(t.activas), "Suscripciones activas", `${t.porPlan.diplomatura} de una diplomatura · ${t.porPlan.todas} de todas`);
    kpi(pesos(t.ingresoMensual), "Ingreso mensual estimado", "Cuotas de las suscripciones activas, antes de comisiones");
    kpi(String(t.conProblemaDePago), "Con problema de pago", "La última cuota no se pudo cobrar", t.conProblemaDePago > 0);
    kpi(String(t.matriculasPagas), "Matrículas pagas");
    kpi(String(t.cuentas), "Cuentas", "Ingresaron con Google o se suscribieron");
    kpi(String(t.pausadas + t.canceladas), "Pausadas o canceladas", `${t.pausadas} pausadas · ${t.canceladas} canceladas`);
    kpi(String(t.certificados), "Certificados emitidos");
  }

  function tarjetaSolicitud(s) {
    const hecha = s.estado === "atendida";
    const horas = (Date.now() - Date.parse(s.fecha)) / 3600000;
    const card = el("article", "sol" + (hecha ? " hecha" : horas > 24 ? " vencida" : ""));
    const t = el("div", "t"); t.append(el("span", null, s.tipo === "baja" ? "Baja de servicio" : "Arrepentimiento"), el("small", null, s.codigo));
    card.append(t);
    card.append(el("span", null, `${s.nombre}${s.dni ? " · DNI " + s.dni : ""}`));
    const mail = el("a", null, s.email); mail.href = `mailto:${s.email}?subject=${encodeURIComponent("Tu solicitud " + s.codigo + " en boceto")}`; card.append(mail);
    if (s.detalle) card.append(el("span", "det", s.detalle));
    card.append(el("span", "mut", `Recibida ${fecha(s.fecha, true)} (${hace(s.fecha)})` + (!hecha && horas > 24 ? " · pasaron más de 24 horas" : "")));
    if (hecha) card.append(el("span", "mut", `Atendida ${fecha(s.atendidaEl, true)}`));
    const acc = el("div", "acc");
    const b = el("button", "btn" + (hecha ? "" : " btn-dark"), hecha ? "Volver a pendiente" : "Marcar como atendido");
    b.type = "button";
    b.addEventListener("click", async () => {
      b.disabled = true;
      const r = await fetch(`/api/admin/solicitudes/${s.codigo}`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ estado: hecha ? "recibida" : "atendida" }) }).catch(() => null);
      if (r && r.ok) { Object.assign(s, await r.json()); datos.totales.solicitudesPendientes += hecha ? 1 : -1; pintarKpis(); pintarSolicitudes(); }
      else { b.disabled = false; b.textContent = "No se pudo guardar, probá de nuevo"; }
    });
    acc.append(b); card.append(acc);
    return card;
  }

  function pintarSolicitudes() {
    $("secSolicitudes").hidden = false;
    const pend = datos.solicitudes.filter((s) => s.estado !== "atendida").sort((a, b) => String(a.fecha).localeCompare(String(b.fecha)));
    const hechas = datos.solicitudes.filter((s) => s.estado === "atendida");
    $("pendientes").replaceChildren(...(pend.length ? pend.map(tarjetaSolicitud) : [el("p", "empty", "No hay pedidos pendientes.")]));
    $("atendidas").replaceChildren(...hechas.map(tarjetaSolicitud));
    $("nAtendidas").textContent = hechas.length;
    $("atendidasBox").hidden = !hechas.length;
  }

  function filaAlumno(a) {
    const tr = el("tr");
    const td = (...kids) => { const c = el("td"); c.append(...kids); tr.append(c); return c; };
    const subs = a.suscripciones.slice().sort((x, y) => (x.status === "authorized" ? -1 : 0) - (y.status === "authorized" ? -1 : 0));
    const quien = el("div", "stack"); quien.append(el("div", "n", a.nombre || "(sin nombre)"), el("div", "e", a.email));
    td(quien);
    const planes = el("div", "stack"), estados = el("div", "stack"), cuotas = el("div", "stack"), mats = el("div", "stack");
    if (!subs.length) { planes.append(el("span", "mut", "—")); estados.append(el("span", "badge b-mut", "Sin suscripción")); cuotas.append(el("span", "mut", "—")); mats.append(el("span", "mut", "—")); }
    subs.forEach((s) => {
      planes.append(el("div", null, (PLANES[s.plan] || s.plan) + (s.carrera ? " · " + (C[s.carrera] ? C[s.carrera].n : s.carrera) : "")));
      const [txt, cls] = estado(s.status); const de = el("div"); de.append(el("span", "badge " + cls, txt)); estados.append(de);
      const c = el("div");
      if (s.alDia === false) c.append(el("span", "badge b-bad", "Falló el cobro"));
      else if (s.alDia === true) c.append(el("span", "badge b-ok", "Al día"));
      else c.append(el("span", "mut", "—"));
      if (s.status === "authorized" && s.proximoCobro) c.append(el("div", "e", "Próximo: " + fecha(s.proximoCobro)));
      cuotas.append(c);
      const dm = el("div"); dm.append(s.matricula === "approved" ? el("span", "badge b-ok", "Paga") : el("span", "badge b-mut", s.matricula ? "Pendiente" : "No")); mats.append(dm);
    });
    td(planes); td(estados); td(cuotas); td(mats);
    const av = el("div");
    const ks = Object.keys(a.avance || {});
    if (!ks.length) av.append(el("span", "mut", "Sin clases"));
    ks.forEach((c) => {
      const n = a.avance[c], row = el("div", "av"), bar = el("span", "bar"), fill = el("i");
      fill.style.width = Math.min(100, Math.round((n / 80) * 100)) + "%"; fill.style.background = C[c] ? C[c].col : "#111111";
      bar.append(fill); row.append(el("span", null, (C[c] ? C[c].n : c)), bar, el("span", "mut", `${n}/80`));
      av.append(row);
    });
    if (a.certificados.length) av.append(el("div", "e", "Certificado: " + a.certificados.map((c) => C[c.carrera] ? C[c.carrera].n : c.carrera).join(", ")));
    td(av);
    td(el("span", null, String(a.entregas || 0)));
    const ult = a.ultimaActividad || a.ultimoIngreso;
    const u = el("div", "stack"); u.append(el("div", null, hace(ult)), el("div", "e", fecha(ult)));
    td(u);
    return tr;
  }

  function pintarAlumnos() {
    $("secAlumnos").hidden = false;
    const q = $("buscar").value.trim().toLowerCase(), f = $("filtro").value;
    const lista = datos.alumnos.filter((a) => {
      if (q && !(a.email.includes(q) || (a.nombre || "").toLowerCase().includes(q))) return false;
      const act = a.suscripciones.filter((s) => s.status === "authorized");
      if (f === "activos") return act.length > 0;
      if (f === "problema") return act.some((s) => s.alDia === false);
      if (f === "sin") return !a.suscripciones.length;
      if (f === "bajas") return a.suscripciones.some((s) => s.status === "paused" || s.status === "canceled");
      return true;
    });
    const filas = lista.map(filaAlumno);
    if (!filas.length) { const tr = el("tr"), c = el("td", "mut", datos.alumnos.length ? "Ningún alumno coincide con el filtro." : "Todavía no hay alumnos."); c.colSpan = 8; tr.append(c); filas.push(tr); }
    $("filas").replaceChildren(...filas);
    $("cuenta").textContent = `${lista.length} de ${datos.alumnos.length}`;
  }

  $("buscar").addEventListener("input", () => datos && pintarAlumnos());
  $("filtro").addEventListener("change", () => datos && pintarAlumnos());
  $("actualizar").addEventListener("click", cargar);
  cargar();
})();
