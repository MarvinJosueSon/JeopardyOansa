import ttkbootstrap as tb
from ttkbootstrap.constants import *

# Intentar importar el Switch nativo (ttkbootstrap >= 1.10 aprox.)
try:
    from ttkbootstrap.widgets import Switch as TBSwitch
except Exception:
    TBSwitch = None  # usaremos fallback

# Estado simple en memoria (luego lo pasamos a SQLite)
DEFAULTS = {"sound_on": True, "time_seconds": 15}


def _ensure_settings(app):
    if not hasattr(app, "_settings"):
        app._settings = DEFAULTS.copy()


def _clear(app):
    for w in app.winfo_children():
        w.destroy()


def open_settings(app: tb.Window, on_back):
    _ensure_settings(app)
    _clear(app)

    app.title("Configuraciones")

    frame = tb.Frame(app, padding=30)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6)

    tb.Label(frame, text="Configuraciones", font=("Segoe UI", 20, "bold")).pack(pady=(0, 16))

    # --- Sonido ON/OFF ---
    sound_row = tb.Frame(frame)
    sound_row.pack(fill=X, pady=10)

    tb.Label(sound_row, text="Sonido").pack(side="left")
    sound_var = tb.BooleanVar(value=app._settings.get("sound_on", True))

    if TBSwitch:
        # Switch nativo
        TBSwitch(sound_row, variable=sound_var, bootstyle="success").pack(side="right")
    else:
        # Fallback para versiones antiguas: Checkbutton con estilo "round-toggle"
        tb.Checkbutton(
            sound_row,
            variable=sound_var,
            bootstyle="success-round-toggle",
            text=""  # sin texto, solo el toggle
        ).pack(side="right")

    # --- Tiempo por pregunta (5–30 s) ---
    time_row = tb.Frame(frame)
    time_row.pack(fill=X, pady=10)
    tb.Label(time_row, text="Tiempo por pregunta (segundos)").pack(anchor="w", pady=(0, 6))

    time_var = tb.IntVar(value=int(app._settings.get("time_seconds", 15)))
    spin = tb.Spinbox(
        time_row, from_=5, to=30, increment=1,
        textvariable=time_var, width=6, bootstyle="primary"
    )
    spin.pack(side="left")

    presets = tb.Frame(time_row)
    presets.pack(side="left", padx=10)
    for v in (5, 10, 15, 20, 30):
        tb.Button(
            presets, text=f"{v}s", bootstyle="secondary",
            command=lambda x=v: time_var.set(x)
        ).pack(side="left", padx=3)

    # --- Acciones ---
    actions = tb.Frame(frame)
    actions.pack(fill=X, pady=(20, 0))

    def _save():
        v = max(5, min(30, int(time_var.get())))
        app._settings["sound_on"] = bool(sound_var.get())
        app._settings["time_seconds"] = v

        tb.ToastNotification(
            title="Guardado",
            message=f"Sonido: {'ON' if app._settings['sound_on'] else 'OFF'} • Tiempo: {v}s",
            duration=2000, position=tb.BOTTOM_RIGHT
        ).show_toast()
        on_back()

    tb.Button(actions, text="Guardar", bootstyle=SUCCESS, command=_save)\
      .pack(side="left", fill=X, expand=True, padx=(0, 6))
    tb.Button(actions, text="Volver", bootstyle=SECONDARY, command=on_back)\
      .pack(side="left", fill=X, expand=True, padx=(6, 0))
