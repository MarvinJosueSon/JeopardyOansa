import ttkbootstrap as tb
from ttkbootstrap.constants import *

def _clear(app: tb.Window):
    for w in app.winfo_children():
        w.destroy()

def select_teams(app: tb.Window, on_back):
    """Paso 1: Seleccionar cantidad de equipos (2–4) con tarjetas grandes y elegantes."""
    _clear(app)

    # ----- contenedor -----
    root = tb.Frame(app, padding=30)
    root.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.82)

    tb.Label(root, text="Cantidad de equipos", font=("Segoe UI", 20, "bold")).pack(pady=(0, 6))
    tb.Label(root, text="Toca una tarjeta para elegir", bootstyle="secondary").pack(pady=(0, 16))

    selected = tb.IntVar(value=2)

    # ----- helper: tarjeta seleccionable -----
    class SelectCard(tb.Frame):
        def __init__(self, parent, value: int, text: str):
            super().__init__(parent, padding=18, bootstyle="secondary")
            self.value = value

            # número grande
            self.num = tb.Label(self, text=str(value), font=("Segoe UI", 28, "bold"))
            self.num.pack()

            # ícono y texto
            info = tb.Frame(self)
            info.pack(pady=(8, 0))
            tb.Label(info, text="👥", font=("Segoe UI Emoji", 18)).pack(side="left", padx=(0, 6))
            tb.Label(info, text=text, bootstyle="secondary").pack(side="left")

            # comportamiento
            self.configure(cursor="hand2")
            self.bind("<Button-1>", self.on_click)
            for child in self.winfo_children():
                child.bind("<Button-1>", self.on_click)

            # hover
            self.bind("<Enter>", lambda e: self.configure(bootstyle="secondary"))
            self.bind("<Leave>", lambda e: self._refresh())

            self._refresh()

        def on_click(self, _=None):
            selected.set(self.value)
            self.master.event_generate("<<card-changed>>")

        def _refresh(self):
            # tarjeta activa resaltada
            if selected.get() == self.value:
                # fondo suave + borde primary
                self.configure(bootstyle="primary")
            else:
                # borde sutil
                self.configure(bootstyle="secondary")

    # ----- grilla de tarjetas -----
    grid = tb.Frame(root)
    grid.pack(fill=X)

    c2 = SelectCard(grid, 2, "2 equipos")
    c3 = SelectCard(grid, 3, "3 equipos")
    c4 = SelectCard(grid, 4, "4 equipos")

    # distribución responsiva
    c2.pack(side="left", fill=X, expand=True, padx=(0, 8))
    c3.pack(side="left", fill=X, expand=True, padx=8)
    c4.pack(side="left", fill=X, expand=True, padx=(8, 0))

    # cuando cambia la selección, refresca todas
    def refresh_all(_=None):
        for card in (c2, c3, c4):
            card._refresh()
    grid.bind("<<card-changed>>", refresh_all)

    # ----- acciones -----
    tb.Label(root, text="Podrás cambiarlo antes de iniciar el tablero.", bootstyle="secondary").pack(pady=(10, 0))

    actions = tb.Frame(root)
    actions.pack(fill=X, pady=(16, 0))

    tb.Button(
        actions, text="Continuar", bootstyle=SUCCESS,
        command=lambda: enter_team_names(app, selected.get(), on_back)
    ).pack(side="left", fill=X, expand=True, padx=(0, 6))

    tb.Button(
        actions, text="Volver", bootstyle=SECONDARY, command=on_back
    ).pack(side="left", fill=X, expand=True, padx=(6, 0))
