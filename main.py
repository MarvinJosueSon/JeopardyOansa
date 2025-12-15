import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from juego import select_teams

# =========================
# CONTROLES FINOS DEL PANEL
# =========================
PANEL_POS = "bottom"

PANEL_Y_RATIO = 0.744
PANEL_Y_OFFSET_PX = 0

PANEL_W_RATIO_BY_WIDTH  = 0.20
PANEL_W_RATIO_BY_HEIGHT = 0.25
PANEL_MIN_W = 295

PANEL_PADDING = 16
BTN_PADY = 4

PANEL_X_OFFSET_PX = 5   # 👉 ajuste horizontal a la derecha


def clear(app):
    for w in app.winfo_children():
        w.destroy()


def main_menu(app: tb.Window):
    clear(app)

    app.title("Jeopardy Bíblico")
    app.minsize(800, 500)

    canvas = tb.Canvas(app, highlightthickness=0, borderwidth=0)
    canvas.pack(fill="both", expand=True)

    app._bg_original = Image.open("assets/Fondo 1.jpg")
    app._bg_photo = ImageTk.PhotoImage(
        app._bg_original.resize((800, 500), Image.LANCZOS)
    )
    bg_item = canvas.create_image(0, 0, image=app._bg_photo, anchor="nw")

    panel = tb.Frame(canvas, padding=PANEL_PADDING, bootstyle="secondary")
    panel_item = canvas.create_window(0, 0, window=panel, anchor="n")

    tb.Button(
        panel, text="Comenzar juego",
        bootstyle="primary-outline",
        command=lambda: select_teams(app, on_back=lambda: main_menu(app))
    ).pack(fill=X, pady=BTN_PADY)

    tb.Button(
        panel, text="Configuraciones",
        bootstyle="secondary-outline",
        command=lambda: print("Configuraciones (pendiente)")
    ).pack(fill=X, pady=BTN_PADY)

    tb.Button(
        panel, text="Salir",
        bootstyle="danger-outline",
        command=app.destroy
    ).pack(fill=X, pady=(BTN_PADY, 0))

    def panel_y(h: int) -> int:
        return int(h * PANEL_Y_RATIO) + PANEL_Y_OFFSET_PX

    def on_resize(event):
        w, h = event.width, event.height
        if w < 1 or h < 1:
            return

        resized = app._bg_original.resize((w, h), Image.LANCZOS)
        app._bg_photo = ImageTk.PhotoImage(resized)
        canvas.itemconfig(bg_item, image=app._bg_photo)

        panel_w = max(
            PANEL_MIN_W,
            min(int(w * PANEL_W_RATIO_BY_WIDTH), int(h * PANEL_W_RATIO_BY_HEIGHT))
        )

        canvas.itemconfig(panel_item, width=panel_w)
        canvas.coords(panel_item, (w // 2) + PANEL_X_OFFSET_PX, panel_y(h))

    canvas.bind("<Configure>", on_resize)

    app.bind("<F11>", lambda e: app.attributes("-fullscreen", True))
    app.bind("<Escape>", lambda e: app.attributes("-fullscreen", False))


if __name__ == "__main__":
    app = tb.Window(themename="darkly")
    main_menu(app)
    app.mainloop()
