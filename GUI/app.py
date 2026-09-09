"""Application entry point for the traffic signal simulation."""

import tkinter as tk
from GUI.intersection import Intersection

WINDOW_TITLE = "AI Traffic Signal Optimization"
WINDOW_SIZE = "1360x900"


def main() -> None:
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(WINDOW_SIZE)
    root.configure(bg="#0B1020")
    app = Intersection(root)

    def on_close():
        app.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
