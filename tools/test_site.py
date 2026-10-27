"""Prueba de punta a punta del sitio con Playwright (asistente simulado)."""
import json, threading, http.server, functools, pathlib, re, sys, time, urllib.request, urllib.parse
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
SHOTS = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "shots"
SHOTS.mkdir(parents=True, exist_ok=True)
PORT = 8765
BASE = f"http://127.0.0.1:{PORT}"

class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), functools.partial(H, directory=str(PUB)))
threading.Thread(target=srv.serve_forever, daemon=True).start()

PAGES = ["/", "/cursos/interiores.html", "/cursos/industrial.html", "/cursos/grafico.html", "/cursos/indumentaria.html",
         "/aprender/recorridos-y-pasos-libres.html", "/aprender/devolucion-diagrama-de-zonas.html", "/panel.html", "/cursos/interiores/programa.html", "/cursos/interiores/herramientas.html",
         "/cursos/interiores/proveedores.html", "/cursos/interiores/semana-03/clase-3.html", "/cursos/interiores/semana-16/clase-5.html",
         "/cursos/industrial/programa.html", "/cursos/industrial/herramientas.html", "/cursos/industrial/proveedores.html",
         "/cursos/industrial/semana-01/clase-3.html", "/cursos/industrial/semana-09/clase-1.html", "/cursos/industrial/semana-16/clase-5.html",
         "/cursos/grafico/programa.html", "/cursos/grafico/herramientas.html", "/cursos/grafico/proveedores.html",
         "/cursos/grafico/semana-01/clase-2.html", "/cursos/grafico/semana-08/clase-3.html", "/cursos/grafico/semana-16/clase-5.html",
         "/cursos/indumentaria/programa.html", "/cursos/indumentaria/herramientas.html", "/cursos/indumentaria/proveedores.html",
         "/cursos/indumentaria/semana-01/clase-2.html", "/cursos/indumentaria/semana-07/clase-2.html", "/cursos/indumentaria/semana-16/clase-5.html",
         "/bocetador/", "/404.html"]
results, problems = [], []
def check(cond, msg):
    results.append((bool(cond), msg))
    if not cond: problems.append(msg)

api_calls = []
def fake_api(route):
    body = json.loads(route.request.post_data or "{}")
    api_calls.append(body)
    last = body["messages"][-1]["content"]
    if "Respondé SOLO con un objeto JSON" in last:
        text = json.dumps({"resumen": "Buen croquis, las proporciones generales funcionan.", "puntos": [
            {"x": 0.3, "y": 0.35, "tipo": "bien", "titulo": "Buena línea de contorno", "texto": "El trazo es seguro y continuo."},
            {"x": 0.6, "y": 0.55, "tipo": "corregir", "titulo": "Ajustá la perspectiva", "texto": "Las fugas de la derecha no convergen."},
            {"x": 0.8, "y": 0.8, "tipo": "sugerencia", "titulo": "Sumá sombras", "texto": "Una sombra proyectada le daría volumen."}]}, ensure_ascii=False)
    else:
        text = "Respuesta de prueba del asistente."
    route.fulfill(status=200, content_type="application/json", body=json.dumps({"text": text, "truncated": False}))

def block_external(route):
    u = route.request.url
    if u.startswith(BASE): return route.continue_()
    return route.abort()

def new_page(browser, w, h, mobile=False):
    ctx = browser.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile, accept_downloads=True)
    ctx.route("**/*", block_external)
    ctx.route(f"{BASE}/api/asistente", fake_api)
    ctx.route(f"{BASE}/api/yo", lambda r: r.fulfill(status=200, content_type="application/json",
        body=json.dumps({"ingresado": True, "email": "ana@example.com", "nombre": "Ana Pérez", "carreras": ["grafico"], "suscripciones": []})))
    ctx.route(f"{BASE}/api/progreso", lambda r: r.fulfill(status=200, content_type="application/json", body="{}" if r.request.method == "PUT" else json.dumps({"progreso": {}, "entregas": {}, "ultima": None})))
    p = ctx.new_page()
    errs = []
    p.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    p.on("console", lambda m: errs.append(f"console: {m.text}") if m.type == "error" and "ERR_FAILED" not in m.text and "net::" not in m.text else None)
    return ctx, p, errs

with sync_playwright() as pw:
    br = pw.chromium.launch()

    # 1) Todas las páginas: errores, desborde horizontal, capturas
    for w, h, mob, tag in [(1440, 900, False, "desk"), (390, 844, True, "phone")]:
        for path in PAGES:
            ctx, p, errs = new_page(br, w, h, mob)
            p.goto(BASE + path, wait_until="load"); p.wait_for_timeout(400)
            over = p.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            check(not errs, f"{tag} {path}: sin errores de JS ({'; '.join(errs)[:300]})")
            check(over <= 1, f"{tag} {path}: sin desborde horizontal (sobran {over}px)")
            name = (path.strip("/").replace("/", "_") or "inicio").replace(".html", "")
            p.screenshot(path=str(SHOTS / f"{tag}-{name}.png"), full_page=(path != "/bocetador/"))
            ctx.close()

    # 2) Enlaces internos y anclas
    ctx, p, errs = new_page(br, 1440, 900)
    seen = set()
    for path in PAGES[:-1]:
        p.goto(BASE + path)
        hrefs = p.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
        for href in hrefs:
            if href.startswith(("http", "mailto:", "tel:")): continue
            full = urllib.parse.urljoin(BASE + path, href)
            key = (path, href)
            if key in seen: continue
            seen.add(key)
            url, _, frag = full.partition("#")
            try:
                code = urllib.request.urlopen(url).status
            except Exception as e:
                code = getattr(e, "code", 0)
            check(code == 200, f"enlace {href} en {path} responde {code}")
            if frag:
                p2 = ctx.new_page(); p2.goto(url)
                check(p2.locator(f"#{frag}").count() > 0, f"ancla #{frag} existe en {url.replace(BASE, '')} (desde {path})")
                p2.close()
    ctx.close()

    # 3) Lección: cuestionario y chat
    ctx, p, errs = new_page(br, 1440, 900)
    p.goto(BASE + "/aprender/recorridos-y-pasos-libres.html")
    p.click('[data-action="check"]')
    check(p.locator('[data-if="needsAnswer"]').is_visible(), "cuestionario: pide elegir una opción")
    p.click('.q-opt[data-opt="a"]'); p.click('[data-action="check"]')
    check(p.locator('[data-if="isWrong"]').is_visible() and not p.locator('[data-if="isCorrect"]').is_visible(), "cuestionario: respuesta incorrecta da pista")
    p.click('.q-opt[data-opt="b"]'); p.click('[data-action="check"]')
    check(p.locator('[data-if="isCorrect"]').is_visible(), "cuestionario: respuesta correcta")
    n0 = len(api_calls)
    p.fill("#pregunta", "¿Cuánto paso dejo entre el sillón y la biblioteca?"); p.press("#pregunta", "Enter")
    p.wait_for_selector("#chat .bubble.ai:not(.wait)")
    check(p.locator("#chat .bubble.ai").last.inner_text() == "Respuesta de prueba del asistente.", "lección: el chat muestra la respuesta")
    check(len(api_calls) == n0 + 1 and "Recorridos y pasos libres" in api_calls[-1]["messages"][0]["content"], "lección: el chat manda el contenido de la lección como contexto")
    p.click("text=Haceme una pregunta de práctica"); p.wait_for_timeout(500)
    check(len(api_calls) == n0 + 2 and len(api_calls[-1]["messages"]) == 3, "lección: los accesos rápidos preguntan y mantienen la conversación")
    check(not errs, f"lección interactiva sin errores ({errs[:2]})")
    ctx.close()

    # 4) Devolución: marcas
    ctx, p, errs = new_page(br, 1440, 900)
    p.goto(BASE + "/aprender/devolucion-diagrama-de-zonas.html")
    p.click('button[aria-label^="Observación 3"]')
    check(p.locator('.note[data-pick="3"]').get_attribute("aria-pressed") == "true" and p.locator('.note[data-pick="3"] .note-body').is_visible(), "devolución: la marca 3 abre su observación")
    check(p.locator('[data-if="sel3"]').count() == 1 and not p.locator('[data-if="sel1"]').evaluate("e => !e.hidden"), "devolución: se mueve el resaltado de la marca")
    p.click('.note[data-pick="2"]')
    check(p.locator('[data-if="sel2"]').evaluate("e => !e.hidden"), "devolución: la observación 2 resalta su marca")
    check(not errs, f"devolución sin errores ({errs[:2]})")
    ctx.close()

    # 5) Panel: calendario y chat
    ctx, p, errs = new_page(br, 1440, 900)
    p.goto(BASE + "/panel.html")
    p.wait_for_selector("#semanaGrid a")
    p.click("text=Agregar a Google Calendar")
    links = p.eval_on_selector_all("#calLinks a", "els => els.map(e => e.href)")
    check(len(links) == 6 and all("calendar.google.com/calendar/render?action=TEMPLATE" in l and "dates=" in l for l in links), f"panel: 6 enlaces (5 clases + repaso) a Google Calendar ({len(links)})")
    p.click("text=Ocultar")
    check(p.locator('[data-if="notConnected"]').first.evaluate("e => !e.hidden"), "panel: se puede ocultar el calendario")
    n0 = len(api_calls)
    p.click("text=Armame un plan para esta semana")
    p.wait_for_selector("#chat .bubble.ai:not(.wait)")
    check(len(api_calls) == n0 + 1, "panel: el asistente responde")
    check(not errs, f"panel sin errores ({errs[:2]})")
    ctx.close()


    # 6a) Curso: las 80 clases sin errores ni desbordes, y su interacción
    import json as _json
    clases = []
    for curso in ["interiores", "industrial", "grafico", "indumentaria"]:
        temario = _json.loads((ROOT / f"content/{curso}/temario.json").read_text(encoding="utf-8"))
        cl = [f"/cursos/{curso}/semana-{w['n']:02d}/clase-{d}.html" for u in temario["unidades"] for w in u["semanas"] for d in range(1, 6)]
        check(len(cl) == 80, f"curso {curso}: el temario tiene 80 clases")
        clases += cl
    ctx, p, errs = new_page(br, 1440, 900)
    bad = []
    for path in clases:
        p.goto(BASE + path, wait_until="load")
        n_quiz = p.locator("[data-quiz]").count()
        ok_opts = p.eval_on_selector_all("[data-quiz]", "qs => qs.every(q => q.querySelectorAll('.opt[data-ok=\"1\"]').length === 1)")
        over = p.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        if n_quiz < 2 or not ok_opts or over > 1 or p.locator("h1").count() != 1: bad.append(path)
    check(not bad, f"cursos: las 320 clases tienen título, al menos 2 preguntas con una sola correcta y sin desbordes ({bad[:3]})")
    check(not errs, f"cursos: sin errores de JS en las 320 clases ({errs[:2]})")
    ctx.close()
    ctx, p, errs = new_page(br, 390, 844, True)
    over_bad = []
    for path in clases[::7]:
        p.goto(BASE + path); 
        if p.evaluate("document.documentElement.scrollWidth - window.innerWidth") > 1: over_bad.append(path)
    check(not over_bad, f"curso en celular: sin desbordes en una muestra de clases ({over_bad[:3]})")
    ctx.close()
    ctx, p, errs = new_page(br, 1440, 900)
    p.goto(BASE + "/cursos/interiores/semana-03/clase-3.html")
    q = p.locator("[data-quiz]").first
    q.locator('.opt[data-ok="0"]').first.click()
    check(q.locator(".fb.no").is_visible() and not q.locator(".fb.ok").is_visible(), "clase: una respuesta incorrecta pide probar otra")
    q.locator('.opt[data-ok="1"]').click()
    check(q.locator(".fb.ok").is_visible(), "clase: la respuesta correcta muestra la explicación")
    p.click("[data-complete]")
    check(p.locator("[data-complete]").get_attribute("aria-pressed") == "true" and p.inner_text("[data-progress-text]") != "0%", "clase: marcar como completada actualiza el progreso")
    check(p.locator('.c-side a[data-cid="s03d3"]').get_attribute("class") == "done", "clase: el menú marca la clase completada")
    p.click("a.next"); p.wait_for_load_state()
    check(p.url.endswith("/semana-03/clase-4.html"), "clase: el botón siguiente lleva a la próxima clase")
    p.goto(BASE + "/cursos/interiores/programa.html")
    check(p.inner_text("[data-continue]") == "Seguir donde dejaste", "programa: ofrece seguir donde dejaste")
    n0 = len(api_calls)
    p.goto(BASE + "/cursos/interiores/semana-09/clase-1.html")
    p.fill("#pregunta", "¿Qué diferencia hay entre lumen y lux?"); p.press("#pregunta", "Enter")
    p.wait_for_selector("#chat .bubble.ai:not(.wait)")
    check(len(api_calls) == n0 + 1 and "Lúmenes, lux y temperatura de color" in api_calls[-1]["messages"][0]["content"], "clase: el asistente recibe el contenido de la clase")
    check(not errs, f"curso interactivo sin errores ({errs[:2]})")
    ctx.close()

    # 6b) Curso de Industrial: color propio, chip y Bocetador en la carrera correcta
    ctx, p, errs = new_page(br, 1440, 900)
    p.goto(BASE + "/cursos/industrial/semana-02/clase-3.html")
    acc = p.evaluate("getComputedStyle(document.body).getPropertyValue('--acc').trim()")
    check(acc.upper() == "#1D4ED8", f"industrial: usa el azul de la carrera ({acc})")
    check(p.locator("text=¿Cómo aplico esto en mi lámpara?").count() == 1, "industrial: acceso rápido propio del curso")
    p.click('button[aria-label="Adjuntar imagen"]'); p.wait_for_load_state()
    check("carrera=industrial" in p.url or p.url.endswith("/bocetador/"), f"industrial: adjuntar lleva al Bocetador de Industrial ({p.url})")
    p.goto(BASE + "/cursos/industrial.html")
    check(p.locator('a[href="/cursos/industrial/programa.html"]').count() >= 1, "ficha industrial: enlaza al programa")
    check(not errs, f"industrial sin errores ({errs[:2]})")
    ctx.close()

    ctx, p, errs = new_page(br, 1440, 900)
    p.goto(BASE + "/cursos/grafico/semana-05/clase-4.html")
    acc = p.evaluate("getComputedStyle(document.body).getPropertyValue('--acc').trim()")
    check(acc.upper() == "#6D28D9", f"gráfico: usa el violeta de la carrera ({acc})")
    check(p.locator("text=¿Cómo aplico esto en mi marca?").count() == 1, "gráfico: acceso rápido propio del curso")
    p.goto(BASE + "/cursos/grafico.html")
    check(p.locator('a[href="/cursos/grafico/programa.html"]').count() >= 1 and p.locator('a[href="/cursos/grafico/semana-01/clase-1.html"]').count() >= 1, "ficha gráfico: enlaza al programa y a la primera clase")
    check(not errs, f"gráfico sin errores ({errs[:2]})")
    ctx.close()

    ctx, p, errs = new_page(br, 1440, 900)
    p.goto(BASE + "/cursos/indumentaria/semana-07/clase-2.html")
    acc = p.evaluate("getComputedStyle(document.body).getPropertyValue('--acc').trim()")
    check(acc.upper() == "#BE185D", f"indumentaria: usa el color de la carrera ({acc})")
    check(p.locator("text=¿Cómo aplico esto en mi colección?").count() == 1, "indumentaria: acceso rápido propio del curso")
    p.goto(BASE + "/cursos/indumentaria.html")
    check(p.locator('a[href="/cursos/indumentaria/programa.html"]').count() >= 1 and p.locator('a[href="/cursos/indumentaria/semana-01/clase-1.html"]').count() >= 1, "ficha indumentaria: enlaza al programa y a la primera clase")
    check(not errs, f"indumentaria sin errores ({errs[:2]})")
    ctx.close()

    # 6) Bocetador
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (1200, 900), (214, 208, 196)); d = ImageDraw.Draw(img)
    for i in range(6): d.line([(150 + i * 140, 150), (250 + i * 120, 750)], fill=(70, 70, 75), width=5)
    d.rectangle([300, 300, 800, 600], outline=(40, 40, 45), width=6)
    photo = SHOTS / "croquis-prueba.jpg"; img.save(photo, quality=88)

    ctx, p, errs = new_page(br, 1440, 900)
    p.goto(BASE + "/bocetador/?carrera=industrial"); p.wait_for_timeout(500)
    check(p.locator('#carreras button[data-k="industrial"]').get_attribute("aria-pressed") == "true", "bocetador: abre en la carrera pedida por la URL")
    def shapes(k):
        p.wait_for_timeout(700)
        data = p.evaluate("JSON.parse(localStorage.getItem('bocetador-v1') || '{}')")
        return len(data.get("sheets", {}).get(k, {}).get("shapes", []))
    p.click('#carreras button[data-k="interiores"]'); p.wait_for_timeout(300)
    base_n = shapes("interiores")
    box = p.locator("#cv").bounding_box(); cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    def drag(x0, y0, x1, y1, steps=12):
        p.mouse.move(x0, y0); p.mouse.down(); p.mouse.move(x1, y1, steps=steps); p.mouse.up()
    p.keyboard.press("b"); drag(cx - 200, cy - 150, cx - 60, cy - 90)
    p.keyboard.press("l"); drag(cx - 100, cy + 120, cx + 160, cy + 125)
    p.keyboard.press("r"); drag(cx + 60, cy - 160, cx + 200, cy - 60)
    p.keyboard.press("e"); drag(cx - 260, cy + 40, cx - 200, cy + 90)
    p.keyboard.press("d"); drag(cx - 100, cy + 200, cx + 140, cy + 200)
    n = shapes("interiores")
    check(n == base_n + 5, f"bocetador: lápiz, línea, rectángulo, elipse y cota agregan trazos ({base_n} → {n})")
    p.click("#undo"); check(shapes("interiores") == n - 1, "bocetador: deshacer")
    p.click("#redo"); check(shapes("interiores") == n, "bocetador: rehacer")
    p.keyboard.press("x"); p.mouse.move(cx - 100, cy + 200); p.mouse.down(); p.mouse.move(cx + 140, cy + 200, steps=20); p.mouse.up()
    check(shapes("interiores") < n, "bocetador: la goma borra")
    for k in ["industrial", "grafico", "indumentaria", "interiores"]:
        p.click(f'#carreras button[data-k="{k}"]'); p.wait_for_timeout(250)
        p.screenshot(path=str(SHOTS / f"bocetador-{k}.png"))
    p.select_option("#grid", "isometrica"); p.wait_for_timeout(200); p.select_option("#grid", "cuadricula")
    p.click("#zoomIn"); p.click("#fit")
    # exportar
    with p.expect_download() as dl:
        p.click("#export")
    path = dl.value.path()
    check(dl.value.suggested_filename == "boceto-interiores.png" and pathlib.Path(path).stat().st_size > 1000, "bocetador: exporta PNG")
    # foto del croquis + corrección
    p.set_input_files("#photoInput", str(photo)); p.wait_for_timeout(900)
    check(p.locator("#photoCtl").is_visible(), "bocetador: carga la foto del croquis y muestra sus controles")
    p.fill("#photoOpacity", "0.6"); p.dispatch_event("#photoOpacity", "input")
    p.screenshot(path=str(SHOTS / "bocetador-foto.png"))
    n0 = len(api_calls)
    p.click("#aiReview")
    p.wait_for_selector("#review button", timeout=8000)
    check(p.locator("#review button").count() == 3, "bocetador: la corrección muestra 3 observaciones")
    req = api_calls[n0]
    check(req.get("image", {}).get("mediaType") == "image/jpeg" and len(req["image"]["data"]) > 10000, "bocetador: manda la foto al asistente como JPEG")
    check("foto de un croquis" in req["messages"][-1]["content"], "bocetador: el pedido aclara que es un croquis en papel")
    p.locator("#review button").nth(1).click()
    check(p.locator("#review button").nth(1).get_attribute("aria-pressed") == "true", "bocetador: elegir una observación la resalta")
    p.screenshot(path=str(SHOTS / "bocetador-correccion.png"))
    p.click("#aiExercise"); p.wait_for_timeout(500)
    check("Respuesta de prueba" in p.inner_text("#aiOut"), "bocetador: propone un ejercicio")
    p.reload(); p.wait_for_timeout(800)
    check(p.locator("#review button").count() == 3 and p.locator("#photoCtl").is_visible(), "bocetador: la foto y la corrección quedan guardadas al recargar")
    check(not errs, f"bocetador sin errores ({errs[:3]})")
    ctx.close()

    # 7) Bocetador en celular con toque
    ctx, p, errs = new_page(br, 390, 844, True)
    p.goto(BASE + "/bocetador/"); p.wait_for_timeout(500)
    check(p.locator("#tools").is_visible() and not p.locator("#panel").is_visible(), "celular: herramientas abajo y panel cerrado")
    p.click("#togglePanel"); p.wait_for_timeout(200)
    check(p.locator("#panel").is_visible(), "celular: el panel de ayudas se abre")
    p.screenshot(path=str(SHOTS / "phone-bocetador-panel.png"))
    p.click("#closePanel")
    box = p.locator("#cv").bounding_box()
    p.locator('.tool[data-tool="pencil"]').click()
    before = p.evaluate("JSON.parse(localStorage.getItem('bocetador-v1')||'{}').sheets?.interiores?.shapes?.length || 0")
    p.evaluate("""([x,y]) => { const c = document.getElementById('cv');
      const ev = (t, px, py) => c.dispatchEvent(new PointerEvent(t, {pointerId: 7, pointerType: 'touch', clientX: px, clientY: py, bubbles: true, isPrimary: true, pressure: .5}));
      ev('pointerdown', x, y); for (let i = 1; i <= 15; i++) ev('pointermove', x + i * 8, y + i * 4); ev('pointerup', x + 120, y + 60); }""", [box["x"] + 60, box["y"] + 120])
    p.wait_for_timeout(700)
    after = p.evaluate("JSON.parse(localStorage.getItem('bocetador-v1')||'{}').sheets?.interiores?.shapes?.length || 0")
    check(after == before + 1, f"celular: se dibuja con el dedo ({before} → {after})")
    check(not errs, f"bocetador celular sin errores ({errs[:3]})")
    ctx.close()
    br.close()

srv.shutdown()
ok = sum(1 for r in results if r[0])
print(f"\n{ok}/{len(results)} pruebas OK")
for good, msg in results:
    if not good: print("FALLA:", msg)
