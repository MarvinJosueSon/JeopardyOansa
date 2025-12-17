#juego.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tablero import iniciar_tablero


def _clear(app: tb.Window):
    for w in app.winfo_children():
        w.destroy()


# =========================================================
# PANTALLA 1: SELECCIONAR CANTIDAD DE EQUIPOS (2–4)
# =========================================================
def select_teams(app: tb.Window, on_back):
    _clear(app)

    root = tb.Frame(app, padding=30)
    root.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.82)

    tb.Label(root, text="Cantidad de equipos", font=("Segoe UI", 20, "bold")).pack(pady=(0, 6))
    tb.Label(root, text="Toca una tarjeta para elegir", bootstyle="secondary").pack(pady=(0, 20))

    selected = tb.IntVar(value=2)

    class SelectCard(tb.Frame):
        def __init__(self, parent, value: int):
            super().__init__(parent, padding=26, bootstyle="secondary")
            self.value = value

            self.font_normal = ("Segoe UI", 36, "bold")
            self.font_hover = ("Segoe UI", 44, "bold")

            self.num = tb.Label(self, text=str(value), font=self.font_normal, anchor="center")
            self.num.pack(expand=True)

            self.configure(cursor="hand2")

            self.bind("<Button-1>", self.on_click)
            self.num.bind("<Button-1>", self.on_click)

            self.bind("<Enter>", self.on_enter)
            self.bind("<Leave>", self.on_leave)
            self.num.bind("<Enter>", self.on_enter)
            self.num.bind("<Leave>", self.on_leave)

            self._refresh()

        def on_click(self, _=None):
            selected.set(self.value)
            self.master.event_generate("<<card-changed>>")

        def on_enter(self, _=None):
            if selected.get() != self.value:
                self.num.configure(font=self.font_hover)

        def on_leave(self, _=None):
            self.num.configure(font=self.font_normal)
            self._refresh()

        def _refresh(self):
            if selected.get() == self.value:
                self.configure(bootstyle="primary")
                self.num.configure(font=self.font_hover)
            else:
                self.configure(bootstyle="secondary")
                self.num.configure(font=self.font_normal)

    grid = tb.Frame(root)
    grid.pack(fill=X)

    c2 = SelectCard(grid, 2)
    c3 = SelectCard(grid, 3)
    c4 = SelectCard(grid, 4)

    c2.pack(side="left", fill=X, expand=True, padx=(0, 12))
    c3.pack(side="left", fill=X, expand=True, padx=12)
    c4.pack(side="left", fill=X, expand=True, padx=(12, 0))

    def refresh_all(_=None):
        for card in (c2, c3, c4):
            card._refresh()
    grid.bind("<<card-changed>>", refresh_all)

    actions = tb.Frame(root)
    actions.pack(fill=X, pady=(20, 0))

    tb.Button(
        actions,
        text="Continuar",
        bootstyle=SUCCESS,
        command=lambda: team_names(app, selected.get(), on_back)
    ).pack(side="left", fill=X, expand=True, padx=(0, 6))

    tb.Button(
        actions,
        text="Volver",
        bootstyle=SECONDARY,
        command=on_back
    ).pack(side="left", fill=X, expand=True, padx=(6, 0))


# =========================================================
# PANTALLA 2: NOMBRES DE EQUIPOS
# =========================================================
def team_names(app: tb.Window, team_count: int, on_back):
    _clear(app)

    root = tb.Frame(app, padding=30)
    root.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.70)

    tb.Label(root, text="Nombres de equipos", font=("Segoe UI", 20, "bold")).pack(pady=(0, 6))
    tb.Label(root, text=f"Ingresa los nombres ({team_count})", bootstyle="secondary").pack(pady=(0, 18))

    form = tb.Frame(root)
    form.pack(fill=X)

    entradas = []
    for i in range(team_count):
        row = tb.Frame(form)
        row.pack(fill=X, pady=8)

        tb.Label(row, text=f"Equipo {i+1}", width=12, anchor="w").pack(side="left")
        e = tb.Entry(row, font=("Segoe UI", 12))
        e.pack(side="left", fill=X, expand=True)
        e.insert(0, f"Equipo {i+1}")
        entradas.append(e)

    def continuar():
        nombres = [e.get().strip() for e in entradas]

        # Validación simple
        if any(n == "" for n in nombres):
            tb.ToastNotification(
                title="Faltan nombres",
                message="Completa el nombre de todos los equipos.",
                duration=2000,
                position=tb.BOTTOM_RIGHT
            ).show_toast()
            return

        # Guardamos en memoria por si luego usamos marcador/turnos
        app._equipos = nombres

        # Ir al tablero
        iniciar_tablero(app, on_back=lambda: team_names(app, team_count, on_back))

    actions = tb.Frame(root)
    actions.pack(fill=X, pady=(22, 0))

    tb.Button(
        actions,
        text="Continuar",
        bootstyle=SUCCESS,
        command=continuar
    ).pack(side="left", fill=X, expand=True, padx=(0, 6))

    tb.Button(
        actions,
        text="Volver",
        bootstyle=SECONDARY,
        command=lambda: select_teams(app, on_back)
    ).pack(side="left", fill=X, expand=True, padx=(6, 0))

    tb.Button(
        actions,
        text="Cancelar",
        bootstyle=DANGER,
        command=on_back
    ).pack(side="left", fill=X, expand=True, padx=(6, 0))
