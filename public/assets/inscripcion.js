// Inscripción con suscripción de Mercado Pago (modelo con plan).
// La tarjeta se tokeniza con MercadoPago.js CardForm; al servidor solo viajan la oferta elegida, el email y el token de un solo uso.
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const STORE = "boceto-suscripcion";
  const PRECIOS = { diplomatura: { amount: 63000, label: "ARS 63.000 por mes · 4 cuotas" }, todas: { amount: 83000, label: "ARS 83.000 por mes" } };
  const NOMBRES = { interiores: "Interiores y Mobiliario", industrial: "Industrial", grafico: "Gráfico", indumentaria: "Indumentaria" };
  const ESTADOS = {
    authorized: ["ok", "✓ Suscripción activa. Ya podés cursar; la cuota se debita sola cada mes."],
    pending: ["warn", "Pendiente: Mercado Pago está confirmando el primer cobro. Volvé a actualizar en unos minutos."],
    paused: ["warn", "Suscripción pausada: no se cobran cuotas y el acceso queda en pausa hasta que la reactives."],
    canceled: ["error", "Suscripción cancelada. Si querés volver, podés suscribirte de nuevo cuando quieras."]
  };

  const form = $("subscription-card-form"), cta = $("suscribirme");
  const elInit = $("estadoInit"), elProceso = $("estadoProceso"), elError = $("estadoError");
  let inFlight = false, cardForm = null;

  const showError = (msg) => { elError.textContent = msg; elError.hidden = false; };
  const clearError = () => { elError.hidden = true; elError.textContent = ""; };
  const readSaved = () => { try { return JSON.parse(localStorage.getItem(STORE) || "null"); } catch (e) { return null; } };
  const save = (v) => { try { localStorage.setItem(STORE, JSON.stringify(v)); } catch (e) {} };

  /* ---------- Oferta elegida (el precio real lo decide el servidor) ---------- */
  const planActual = () => (document.querySelector('input[name="plan"]:checked') || {}).value || "diplomatura";
  function pintarOferta() {
    const p = planActual();
    $("carreraWrap").hidden = p !== "diplomatura";
    $("total").textContent = PRECIOS[p].label;
  }
  const qs = new URLSearchParams(location.search);
  if (qs.get("plan") === "todas") document.querySelector('input[value="todas"]').checked = true;
  if (NOMBRES[qs.get("carrera")]) $("carrera").value = qs.get("carrera");
  document.querySelectorAll('input[name="plan"]').forEach((r) => r.addEventListener("change", pintarOferta));
  pintarOferta();

  /* ---------- Estado de una suscripción guardada en este navegador ---------- */
  function pintarSuscripcion(s) {
    const box = $("miSuscripcion"); box.hidden = false;
    const [tono, texto] = ESTADOS[s.status] || ESTADOS.pending;
    const quien = s.plan === "todas" ? "Todas las diplomaturas" : `Diplomatura en ${NOMBRES[s.carrera] || s.carrera}`;
    const prox = s.proximoCobro ? ` Próximo cobro: ${new Date(s.proximoCobro).toLocaleDateString("es-AR")}.` : "";
    const deuda = s.status === "authorized" && s.alDia === false
      ? " ⚠ El último cobro no pasó: Mercado Pago lo reintenta. Revisá que tu tarjeta tenga saldo o actualizala en tu cuenta de Mercado Pago." : "";
    const el = $("estadoSub"); el.className = `i-alert ${deuda ? "warn" : tono}`; el.textContent = `${quien}. ${texto}${prox}${deuda}`;
    box.querySelector('[data-accion="pause"]').hidden = s.status !== "authorized";
    box.querySelector('[data-accion="reactivate"]').hidden = s.status !== "paused";
    box.querySelector('[data-accion="cancel"]').hidden = s.status === "canceled";
    // Matrícula: se muestra hasta que el pago queda aprobado
    const mb = $("matriculaBox"), mt = $("matriculaTxt");
    mb.hidden = s.status === "canceled" || s.matricula === "approved";
    if (s.matricula === "approved") return;
    if (s.matricula === "pending" || s.matricula === "in_process") { mt.textContent = "Tu pago de la matrícula está pendiente: Mercado Pago lo acredita apenas se confirme."; $("pagarMatricula").hidden = true; }
    else if (s.matricula === "rejected") { mt.textContent = "El pago de la matrícula no pasó. Probá de nuevo con otro medio de pago."; $("pagarMatricula").hidden = false; }
  }
  // Al volver de Mercado Pago: se confirma el pago del lado del servidor
  async function confirmarMatricula() {
    const saved = readSaved(), pid = qs.get("payment_id") || qs.get("collection_id");
    if (!saved || !qs.get("matricula")) return;
    try {
      const r = await fetch("/api/matricula/confirmar", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ id: saved.id, llave: saved.llave, paymentId: pid }) });
      const d = await r.json().catch(() => ({}));
      if (d.matricula) { saved.matricula = d.matricula; save(saved); pintarSuscripcion(saved); }
    } catch (e) { /* el webhook lo actualiza igual */ }
    history.replaceState(null, "", location.pathname);
  }
  async function consultar() {
    const saved = readSaved(); if (!saved) return;
    pintarSuscripcion(saved);
    try {
      const r = await fetch(`/api/subscriptions/${encodeURIComponent(saved.id)}`, { headers: { "x-llave": saved.llave }, cache: "no-store" });
      const d = await r.json();
      if (r.ok) { Object.assign(saved, d); save(saved); pintarSuscripcion(saved); }
    } catch (e) { /* se muestra el último estado conocido */ }
  }
  document.querySelectorAll("[data-accion]").forEach((b) => b.addEventListener("click", async () => {
    const saved = readSaved(); if (!saved || b.disabled) return;
    const accion = b.dataset.accion;
    if (accion === "refresh") { consultar(); return; }
    if (accion === "cancel" && !window.confirm("¿Seguro que querés cancelar la suscripción? Se dejan de cobrar las cuotas.")) return;
    b.disabled = true;
    try {
      const r = await fetch(`/api/subscriptions/${encodeURIComponent(saved.id)}/${accion}`, { method: "POST", headers: { "x-llave": saved.llave } });
      const d = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(d.message || "No se pudo hacer el cambio. Intentá nuevamente.");
      saved.status = d.status; save(saved); pintarSuscripcion(saved);
    } catch (e) { $("estadoSub").className = "i-alert error"; $("estadoSub").textContent = e.message; }
    finally { b.disabled = false; }
  }));

  /* ---------- Formulario seguro de Mercado Pago ---------- */
  async function iniciarPago() {
    cta.disabled = true;
    let publicKey;
    try {
      const r = await fetch("/api/mp-config", { cache: "no-store" });
      const d = await r.json();
      if (!r.ok || !d.publicKey) throw new Error(d.message || "Los pagos todavía no están configurados.");
      publicKey = d.publicKey;
    } catch (e) {
      elInit.hidden = true;
      showError(`${e.message || "No se pudo preparar el pago."} Probá recargar la página en unos minutos.`);
      return;
    }
    if (typeof window.MercadoPago !== "function") {
      elInit.hidden = true;
      showError("No se pudo cargar Mercado Pago. Si usás un bloqueador de anuncios, desactivalo para este sitio y recargá la página.");
      return;
    }
    const mp = new window.MercadoPago(publicKey, { locale: "es-AR" });
    // Se monta cuando la página ya es visible, una sola vez.
    requestAnimationFrame(() => {
      cardForm = mp.cardForm({
        amount: String(PRECIOS[planActual()].amount),
        iframe: true,
        form: {
          id: "subscription-card-form",
          cardNumber: { id: "subscription__cardNumber", placeholder: "1234 1234 1234 1234" },
          expirationDate: { id: "subscription__expirationDate", placeholder: "MM/AA" },
          securityCode: { id: "subscription__securityCode", placeholder: "CVC" },
          cardholderName: { id: "subscription__cardholderName" },
          issuer: { id: "subscription__issuer" },
          installments: { id: "subscription__installments" },
          identificationType: { id: "subscription__identificationType" },
          identificationNumber: { id: "subscription__identificationNumber" },
          cardholderEmail: { id: "subscription__payerEmail" }
        },
        callbacks: {
          onFormMounted: (error) => {
            elInit.hidden = true;
            if (error) { showError("No se pudo mostrar el formulario de tarjeta. Recargá la página e intentá nuevamente."); return; }
            const hosts = ["subscription__cardNumber", "subscription__expirationDate", "subscription__securityCode"].map($);
            const okHosts = hosts.every((h) => h.querySelectorAll("iframe").length === 1 && h.offsetHeight > 0);
            if (!okHosts) { showError("El formulario de tarjeta no cargó bien. Recargá la página."); return; }
            cta.disabled = false;
          },
          onSubmit: (event) => { event.preventDefault(); enviar(); },
          onFetching: () => () => {}
        }
      });
    });
  }

  async function enviar() {
    if (inFlight || !cardForm) return;
    clearError();
    const datos = cardForm.getCardFormData();
    const email = (datos.cardholderEmail || $("subscription__payerEmail").value || "").trim();
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { showError("Revisá el email: lo usamos para tu cuenta y tus avisos de pago."); return; }
    if (!datos.token) { showError("Revisá los datos de la tarjeta e intentá nuevamente."); return; }
    inFlight = true; cta.disabled = true; cta.textContent = "Procesando…"; elProceso.hidden = false;
    try {
      const r = await fetch("/api/subscriptions", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ plan: planActual(), carrera: $("carrera").value, email, cardToken: datos.token })
      });
      const d = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(d.message || "No se pudo crear la suscripción. Intentá nuevamente.");
      save({ id: d.id, llave: d.llave, status: d.status, plan: d.plan, carrera: d.carrera });
      $("pagoCard").hidden = true;
      pintarSuscripcion(d);
      $("miSuscripcion").scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (e) {
      showError(e.message);
      cta.disabled = false; cta.textContent = "Suscribirme";
      try { cardForm.unmount(); } catch (x) {}
      cardForm = null; elInit.hidden = false; iniciarPago(); // el token es de un solo uso: se arma un formulario nuevo
    } finally {
      inFlight = false; elProceso.hidden = true;
    }
  }

  form.addEventListener("submit", (e) => e.preventDefault());
  consultar().then(confirmarMatricula);
  const saved = readSaved();
  if (saved && saved.status && saved.status !== "canceled") $("pagoCard").hidden = true;
  else {
    // Para suscribirse hay que ingresar con Google: la diplomatura queda asociada a esa cuenta.
    fetch("/api/yo", { cache: "no-store" }).then((r) => r.json()).then((yo) => {
      if (!yo.ingresado) {
        form.hidden = true; elInit.hidden = true;
        const box = $("ingresoBox"); box.hidden = false;
        $("ingresoGoogle").href = "/auth/google?volver=" + encodeURIComponent(location.pathname + location.search);
        return;
      }
      $("cuentaTxt").textContent = "Ingresaste como " + yo.email + ". La diplomatura queda asociada a esta cuenta.";
      $("cuentaTxt").hidden = false;
      if (!$("subscription__payerEmail").value) $("subscription__payerEmail").value = yo.email;
      iniciarPago();
    }).catch(() => iniciarPago());
  }
})();
