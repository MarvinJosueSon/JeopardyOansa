# tablero.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from dbPreguntas import obtener_pregunta_random, marcar_pregunta_usada

CATEGORIAS_DEFAULT = ["Historia", "Personajes", "Lugares", "Milagros", "Versículos"]
VALORES_DEFAULT = [100, 200, 300, 400, 500]

PASTELES = [
    {"bg": "#AFC9F5", "fg": "#0D1B2A"},
    {"bg": "#BFE6C6", "fg": "#0B1F13"},
    {"bg": "#F7E6A8", "fg": "#2A2200"},
    {"bg": "#F3B7B7", "fg": "#2A0A0A"},
    {"bg": "#D7C6F7", "fg": "#1C102A"},
]


def _clear(app: tb.Window):
    for w in app.winfo_children():
        w.destroy()


def _ensure_settings(app: tb.Window):
    if not hasattr(app, "_settings"):
        app._settings = {"sound_on": True, "time_seconds": 15}


def _init_styles(app: tb.Window):
    style = app.style

    for i in range(5):
        bg = PASTELES[i]["bg"]
        fg = PASTELES[i]["fg"]

        style.configure(
            f"pastel{i}.TButton",
            font=("Segoe UI", 16, "bold"),
            padding=(8, 18),
            background=bg,
            foreground=fg,
            bordercolor="#2b2b2b",
            focusthickness=0,
        )
        style.map(
            f"pastel{i}.TButton",
            background=[("active", bg), ("pressed", bg)],
            foreground=[("active", fg), ("pressed", fg)],
            relief=[("pressed", "sunken")],
        )

        style.configure(
            f"pastel{i}_used.TButton",
            font=("Segoe UI", 16, "bold"),
            padding=(8, 18),
            background="#3f3f3f",
            foreground="#cfcfcf",
            bordercolor="#2b2b2b",
        )

        style.configure(
            f"pastel{i}_head.TLabel",
            font=("Segoe UI", 12, "bold"),
            background=bg,
            foreground=fg,
            padding=10,
        )

    style.configure("team_active.TFrame", borderwidth=2, relief="solid")
    style.configure("team_inactive.TFrame", borderwidth=0, relief="flat")


def precargar_preguntas(app, categorias, valores):
    """
    Carga 25 preguntas (5x5) UNA sola vez (al entrar al tablero).
    IMPORTANTE:
    - No uses lower() si tu BD guarda "Historia", etc.
    - NO marcar usada aquí (se marca cuando el usuario responde o se acaba el tiempo)
    """
    tablero = [[None for _ in range(5)] for _ in range(5)]

    for c in range(5):
        categoria = categorias[c].strip()

        for r in range(5):
            valor = valores[r]  # 100,200,300,400,500
            q = obtener_pregunta_random(categoria, valor)
            tablero[r][c] = q

    app._preguntas_tablero = tablero


def iniciar_tablero(app: tb.Window, on_back, categorias=None, valores=None):
    _clear(app)
    _ensure_settings(app)
    if hasattr(app, "_preguntas_tablero"):
        delattr(app, "_preguntas_tablero")
    if hasattr(app, "_tablero_usados"):
        delattr(app, "_tablero_usados")

    _init_styles(app)

    categorias = categorias if categorias and len(categorias) == 5 else CATEGORIAS_DEFAULT
    valores = valores if valores and len(valores) == 5 else VALORES_DEFAULT

    # Precargar SOLO si no existe (para no consultar en cada click)
    if not hasattr(app, "_preguntas_tablero"):
        precargar_preguntas(app, categorias, valores)

    equipos = getattr(app, "_equipos", ["Equipo 1", "Equipo 2"])[:4]

    if not hasattr(app, "_puntos"):
        app._puntos = {n: 0 for n in equipos}
    else:
        for n in equipos:
            if n not in app._puntos:
                app._puntos[n] = 0
        for n in list(app._puntos.keys()):
            if n not in equipos:
                del app._puntos[n]

    if not hasattr(app, "_equipo_activo"):
        app._equipo_activo = 0
    if app._equipo_activo >= len(equipos):
        app._equipo_activo = 0

    if not hasattr(app, "_tablero_usados"):
        app._tablero_usados = [[False for _ in range(5)] for _ in range(5)]

    app.title("Tablero 5×5")
    app.minsize(900, 650)

    root = tb.Frame(app, padding=16)
    root.pack(fill=BOTH, expand=True)

    # ===== Top bar =====
    top = tb.Frame(root)
    top.pack(fill=X, pady=(0, 12))

    tb.Button(top, text="⟵ Volver", bootstyle="secondary", command=on_back).pack(side="left")
    tb.Label(top, text="Tablero 5×5", font=("Segoe UI", 18, "bold")).pack(side="left", padx=14)

    # ===== Header categorías =====
    header = tb.Frame(root)
    header.pack(fill=X)

    for c in range(5):
        box = tb.Frame(header)
        box.pack(side="left", fill=X, expand=True, padx=6)
        tb.Label(box, text=categorias[c], style=f"pastel{c}_head.TLabel", anchor="center").pack(fill=X)

    # ===== Overlay pregunta =====
    overlay = tb.Frame(root, padding=18, bootstyle="secondary")
    overlay.place_forget()

    overlay_title = tb.Label(overlay, text="", font=("Segoe UI", 16, "bold"))
    overlay_title.pack(pady=(0, 6))

    timer_row = tb.Frame(overlay)
    timer_row.pack(fill=X, pady=(0, 10))
    timer_lbl = tb.Label(timer_row, text="", font=("Segoe UI", 12, "bold"))
    timer_lbl.pack(side="right")

    overlay_text = tb.Label(overlay, text="", wraplength=760, justify="center", font=("Segoe UI", 13))
    overlay_text.pack(pady=(0, 14))

    answers_box = tb.Frame(overlay)
    answers_box.pack(fill=X)

    feedback = tb.Label(overlay, text="", font=("Segoe UI", 12, "bold"))
    feedback.pack(pady=(12, 0))

    # ===== control timer =====
    timer_job = {"id": None}
    timer_state = {"seconds": 0}
    current_q = {"data": None, "r": None, "c": None, "valor": None}

    def _cancel_timer():
        if timer_job["id"] is not None:
            try:
                overlay.after_cancel(timer_job["id"])
            except Exception:
                pass
            timer_job["id"] = None

    def cerrar_overlay():
        _cancel_timer()
        overlay.place_forget()
        feedback.configure(text="")
        timer_lbl.configure(text="")

        for w in answers_box.winfo_children():
            w.destroy()

        current_q["data"] = None
        current_q["r"] = None
        current_q["c"] = None
        current_q["valor"] = None

    def mostrar_overlay(titulo: str, enunciado: str):
        overlay_title.configure(text=titulo)
        overlay_text.configure(text=enunciado)
        overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.62)
        overlay.lift()  # 🔥 sube el overlay por encima del tablero
        overlay.focus_force()  # opcional, para que “agarre” foco

    def marcar_celda_usada(r, c):
        app._tablero_usados[r][c] = True
        b = botones[r][c]
        b.configure(text="✓", style=f"pastel{c}_used.TButton", state=DISABLED)

    def refrescar_puntos():
        for _, nombre, lbl in tarjetas:
            lbl.configure(text=str(app._puntos.get(nombre, 0)))

    def sumar_puntos(valor):
        equipo = equipos[app._equipo_activo]
        app._puntos[equipo] += int(valor)
        refrescar_puntos()

    def _timeout():
        q = current_q["data"]
        if not q:
            cerrar_overlay()
            return

        for b in answers_box.winfo_children():
            try:
                b.configure(state=DISABLED)
            except Exception:
                pass

        feedback.configure(text="⏱️ Tiempo agotado", bootstyle="warning")

        # ✅ marcar usada la pregunta cuando se usó
        marcar_pregunta_usada(q["id"])
        marcar_celda_usada(current_q["r"], current_q["c"])

        overlay.after(1400, cerrar_overlay)

    def _tick():
        s = timer_state["seconds"]
        timer_lbl.configure(text=f"⏱️ {s}s")

        if s <= 0:
            timer_job["id"] = None
            _timeout()
            return

        timer_state["seconds"] -= 1
        timer_job["id"] = overlay.after(1000, _tick)

    def iniciar_timer():
        _cancel_timer()
        t = int(app._settings.get("time_seconds", 15))
        if t < 5:
            t = 5
        if t > 30:
            t = 30
        timer_state["seconds"] = t
        _tick()

    def responder(seleccion_texto):
        q = current_q["data"]
        if not q:
            return

        _cancel_timer()
        correcta = (seleccion_texto == q["respuesta_correcta"])

        for b in answers_box.winfo_children():
            try:
                b.configure(state=DISABLED)
            except Exception:
                pass

        if correcta:
            feedback.configure(text="✅ Correcto", bootstyle="success")
            sumar_puntos(current_q["valor"])
        else:
            feedback.configure(text=f"❌ Incorrecto • Correcta: {q['respuesta_correcta']}", bootstyle="danger")

        # ✅ marcar usada la pregunta cuando se usó
        marcar_pregunta_usada(q["id"])
        marcar_celda_usada(current_q["r"], current_q["c"])

        overlay.after(1400, cerrar_overlay)

    def construir_respuestas(q):
        for w in answers_box.winfo_children():
            w.destroy()

        opciones = []
        for k in ("opcion_a", "opcion_b", "opcion_c", "opcion_d"):
            v = q.get(k)
            if v:
                opciones.append(v)

        cols = 2 if len(opciones) >= 4 else 1
        rows = (len(opciones) + cols - 1) // cols

        for rr in range(rows):
            rowf = tb.Frame(answers_box)
            rowf.pack(fill=X, pady=6)

            for cc in range(cols):
                idx = rr * cols + cc
                if idx >= len(opciones):
                    break

                txt = opciones[idx]
                tb.Button(
                    rowf,
                    text=txt,
                    bootstyle="primary-outline",
                    command=lambda t=txt: responder(t)
                ).pack(side="left", fill=X, expand=True, padx=6)

        tb.Button(
            answers_box,
            text="Cancelar",
            bootstyle="secondary",
            command=cerrar_overlay
        ).pack(fill=X, pady=(12, 0))

    # ===== Grid 5x5 =====
    grid = tb.Frame(root)
    grid.pack(fill=BOTH, expand=True, pady=(14, 10))

    botones = [[None for _ in range(5)] for _ in range(5)]

    def click_celda(r, c):
        if app._tablero_usados[r][c]:
            return

        categoria = categorias[c]
        valor = valores[r]

        # ✅ SIN CONSULTA: usamos lo precargado
        q = app._preguntas_tablero[r][c]
        if q is None:
            tb.ToastNotification(
                title="Sin pregunta",
                message=f"No hay pregunta asignada para {categoria} ({valor}).",
                duration=2000,
                position=tb.BOTTOM_RIGHT
            ).show_toast()
            return

        current_q["data"] = q
        current_q["r"] = r
        current_q["c"] = c
        current_q["valor"] = valor

        feedback.configure(text="")
        mostrar_overlay(f"{categoria} • {valor} pts", q["enunciado"])
        construir_respuestas(q)
        iniciar_timer()

    for r in range(5):
        fila = tb.Frame(grid)
        fila.pack(fill=BOTH, expand=True, pady=6)

        for c in range(5):
            usada = app._tablero_usados[r][c]
            texto = "✓" if usada else str(valores[r])

            b = tb.Button(
                fila,
                text=texto,
                style=(f"pastel{c}_used.TButton" if usada else f"pastel{c}.TButton"),
                state=(DISABLED if usada else NORMAL),
                command=lambda rr=r, cc=c: click_celda(rr, cc)
            )
            b.pack(side="left", fill=BOTH, expand=True, padx=6)
            botones[r][c] = b

    # ===== Marcador inferior =====
    scoreboard = tb.Frame(root, padding=10, bootstyle="secondary")
    scoreboard.pack(fill=X)

    tarjetas = []

    def set_equipo_activo(idx):
        app._equipo_activo = idx
        refrescar_equipo_activo()

    def refrescar_equipo_activo():
        for i, (frame, _, __) in enumerate(tarjetas):
            frame.configure(style=("team_active.TFrame" if i == app._equipo_activo else "team_inactive.TFrame"))

    for i, nombre in enumerate(equipos):
        card = tb.Frame(scoreboard, padding=10)
        card.pack(side="left", fill=X, expand=True, padx=6)

        card.configure(cursor="hand2")
        card.bind("<Button-1>", lambda e, idx=i: set_equipo_activo(idx))

        name_lbl = tb.Label(card, text=nombre, font=("Segoe UI", 12, "bold"))
        name_lbl.pack()
        name_lbl.bind("<Button-1>", lambda e, idx=i: set_equipo_activo(idx))

        puntos_lbl = tb.Label(card, text=str(app._puntos[nombre]), font=("Segoe UI", 18, "bold"))
        puntos_lbl.pack(pady=(2, 0))
        puntos_lbl.bind("<Button-1>", lambda e, idx=i: set_equipo_activo(idx))

        tarjetas.append((card, nombre, puntos_lbl))

    refrescar_puntos()
    refrescar_equipo_activo()
