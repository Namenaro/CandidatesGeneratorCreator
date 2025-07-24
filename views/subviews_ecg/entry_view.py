from utils import plot_lead_signal_to_ax
from interactive_manager import InteractiveManager

import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



class EntryView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg='white', padx=5, pady=5)

        # Создаем фигуру и оси
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.interactive = InteractiveManager(self.ax)  # Внедрение интерактивности

        # Создаем холст для графика
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)


    def plot(self, entry_signal, time, entry_points_pict):
        self.ax.clear()
        #self.ax.plot(time, entry_signal)
        self.plot_signal( entry_signal, time)
        self.plot_points(entry_points_pict)

        # Обновляем начальные границы после создания графика
        self.interactive.initial_xlim = self.ax.get_xlim()
        self.interactive.initial_ylim = self.ax.get_ylim()
        self.interactive.initial_center = (
            (self.interactive.initial_xlim[0] + self.interactive.initial_xlim[1]) / 2,
            (self.interactive.initial_ylim[0] + self.interactive.initial_ylim[1]) / 2
        )

        # Перерисовываем холст
        self.canvas.draw()

    def plot_signal(self, signal, time):
        plot_lead_signal_to_ax(signal_mV=signal, ax=self.ax, time=time, Y_max=max(signal),
                               Y_min=min(signal))

    def plot_points(self, points_dict):
        for  name, pos in points_dict.items():
            self.ax.axvline(pos, color='r', linestyle='--', alpha=0.7, picker=5)
            self.ax.text(
                pos, self.ax.get_ylim()[1] * 0.95, name,
                ha='center', va='top', color='r',
                bbox=dict(facecolor='white', alpha=0.7)
            )

if __name__ == "__main__":
    from tkinter import filedialog
    from dataset_forms import DatasetWrapper, POINTS_DATASET_JSON_KEYS

    file_path = filedialog.askopenfilename(
        title="Выберите файл",
        filetypes=(("Все файлы", "*.*"), ("Текстовые файлы", "*.txt"))
    )

    if file_path:
        dataset = DatasetWrapper(file_path)

        index = 0
        entry = dataset.get_ith_entry(index)

        points_dict = entry[POINTS_DATASET_JSON_KEYS.points]
        signal, time = dataset.get_signal_for_ith_entry(index)

        # Создаем корневое окно
        root = tk.Tk()
        entry_view = EntryView(root)
        entry_view.pack(fill=tk.BOTH, expand=True, pady=10)
        entry_view.plot(signal, time, points_dict)

        root.mainloop()






