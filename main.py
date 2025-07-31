import tkinter as tk
from tkinter import ttk

from views.main_view import MainView

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Редактор мультирека")
    root.geometry("800x600")

    main_view = MainView(root)
    main_view.pack(fill="both", expand=True)

    root.mainloop()