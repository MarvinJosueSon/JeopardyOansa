import ttkbootstrap as tb
from ttkbootstrap.constants import *

# Categorías definidas
CATEGORIAS_DEFAULT = ["Historia", "Personajes", "Lugares", "Milagros", "Versículos"]
VALORES_DEFAULT = [100, 200, 300, 400, 500]

# Colores pastel por columna (5 columnas)
PASTELES = [
    {"bg": "#AFC9F5", "fg": "#0D1B2A"},  # azul pastel
    {"bg": "#BFE6C6", "fg": "#0B1F13"},  # verde pastel
    {"bg": "#F7E6A8", "fg": "#2A2200"},  # amarillo pastel
    {"bg": "#F3B7B7", "fg": "#2A0A0A"},  # rojo pastel
    {"bg": "#D7C6F7", "fg": "#1C102A"},  # morado pastel (para 5ta col)
]


def _clear(app: tb.Window):
    for w in app.winfo_children():
        w.destroy()


def _init_styles(app: tb.Window):
    """Crea estilos pastel para botones y encabezados."""
    style = app.style

    for i in range(5):
        bg = PASTELES[i]["bg"]
        fg = PASTELES[i]["fg"]

        # Botón normal
        style.configure(
            f"pastel{i}.TButton",
            font=("Segoe UI", 16, "bold"),
            padding=(8, 18),
            background=bg,
            foreground=fg,
            bordercolor="#2b2b2b",
            focusthickness=0
        )
        # Hover/pressed
        style.map(
            f"pastel{i}.TButton",
            background=[("active", bg), ("pressed", bg)],
            foreground=[("active", fg), ("pressed", fg)],
            relief=[("pressed", "sunken")]
        )

        # Botón usado
        style.configure(
            f"pastel{i}_used.TButton",
            font=("Segoe UI", 16, "bold"),
            padding=(8, 18),
            background="#3f3f3f",
            foreground="#cfcfcf",
            bordercolor="#2b2b2b"
        )

        # Encabezado categoría
        style.configure(
            f"pastel{i}_head.TLabel",
            font=("Segoe UI", 12, "bold"),
            background=bg,
            foreground=fg,
            padding=10
        )


def iniciar_tablero(app: tb.Window, on_back, categorias=None, valores=None):
    _clear(app)
    _init_styles(app)

    categorias = categorias if categorias and len(categorias) == 5 else CATEGORIAS_DEFAULT
    valores = valores if valores and len(valores) == 5 else VALORES_DEFAULT

    # Equipos desde el flujo anterior (team_names)
    equipos = getattr(app, "_equipos", ["Equipo 1", "Equipo 2"])
    equipos = equipos[:4]  # seguridad

    # Puntajes en memoria
    if not hasattr(app, "_puntos"):
        app._puntos = {nombre: 0 for nombre in equipos}
    else:
        # si cambia cantidad de equipos, ajusta el dict
        for nombre in equipos:
            if nombre not in app._puntos:
                app._puntos[nombre] = 0
        for nombre in list(app._puntos.keys()):
            if nombre not in equipos:
                del app._puntos[nombre]

    # Estado: celdas usadas
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
    tb.Label(top, text="TABLERO DE PREGUNTAS", font=("Segoe UI", 18, "bold")).pack(side="left", padx=200)

    # ===== Header categorías (pastel por columna) =====
    header = tb.Frame(root)
    header.pack(fill=X)

    for c in range(5):
        box = tb.Frame(header, bootstyle="secondary")
        box.pack(side="left", fill=X, expand=True, padx=6)
        lbl = tb.Label(box, text=categorias[c], style=f"pastel{c}_head.TLabel", anchor="center")
        lbl.pack(fill=X)

    # ===== Grid 5x5 =====
    grid = tb.Frame(root)
    grid.pack(fill=BOTH, expand=True, pady=(14, 10))

    botones = [[None for _ in range(5)] for _ in range(5)]

    def marcar_usada(r, c):
        app._tablero_usados[r][c] = True
        b = botones[r][c]
        b.configure(text="✓", style=f"pastel{c}_used.TButton", state=DISABLED)

    def click_celda(r, c):
        # Por ahora solo marca la celda como usada (luego aquí abrimos pregunta)
        if app._tablero_usados[r][c]:
            return
        marcar_usada(r, c)

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

    # ===== Marcador inferior (2–4 equipos según selección) =====
    scoreboard = tb.Frame(root, padding=10, bootstyle="secondary")
    scoreboard.pack(fill=X)

    tarjetas = []

    def refrescar_puntos():
        for nombre, lbl in tarjetas:
            lbl.configure(text=str(app._puntos.get(nombre, 0)))

    # Tarjetas de equipos (pasteles suaves alternados)
    for i, nombre in enumerate(equipos):
        col = i % 5
        card = tb.Frame(scoreboard, padding=10, bootstyle="secondary")
        card.pack(side="left", fill=X, expand=True, padx=6)

        # Nombre
        tb.Label(card, text=nombre, font=("Segoe UI", 12, "bold")).pack()

        # Puntaje grande
        puntos_lbl = tb.Label(card, text=str(app._puntos[nombre]), font=("Segoe UI", 18, "bold"))
        puntos_lbl.pack(pady=(2, 0))

        tarjetas.append((nombre, puntos_lbl))

    refrescar_puntos()
