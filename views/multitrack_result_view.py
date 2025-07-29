from sympy.printing.pretty.pretty_symbology import line_width

from utils import plot_lead_signal_to_ax

import tkinter as tk

from views.subviews_ecg.plot_popup_manager import PlotPopupManager

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import List
import matplotlib.pyplot as plt
import numpy as np



class MultitrackResultView(tk.Frame):
    """ Визуализирует кандатов от всех треков одной картинкой
    График интерактивен: есть зум колесиком мыши, перетаскивание, возфращение масщтаба при клике на правую кнопку мыши"""
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg='white', padx=5, pady=5)

        # Создаем фигуру и оси
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)



        # Создаем холст для графика
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Менеджер всплывающих окон
        self.popup_manager = PlotPopupManager()

        # Привязка обработчика кликов
        self.canvas.mpl_connect('button_press_event', self._on_click)


    def plot(self, signal:List[float], time:List[float], left:float, right:float, true:float, candidates_of_tracks:List[List[float]], tracks_names:List[str]):
        self.ax.clear()

        # рисуем сигнал
        max_y = max(signal)*1.1
        min_y = min(signal)
        min_y = min_y - 0.1 * abs(min_y)
        plot_lead_signal_to_ax(signal_mV=signal, ax=self.ax, time=time, Y_max=max_y,
                               Y_min=min_y, color='gray', alpha=0.4, linestyle='--')

        # рисуем допустимую область
        self.ax.axvline(left, color='r', linestyle='-', alpha=0.7,  linewidth=0.3)
        self.ax.axvline(right, color='r', linestyle='-', alpha=0.7, linewidth=0.3)

        self.ax.axvspan(left, right,
                   facecolor='r', alpha=0.1,
                   ymin=0, ymax=1)

        # рисуем правильный ответ (где должна реально стоять целевая точка этого мультитрека)
        self.ax.axvline(true, color='g', linestyle='--', alpha=0.5)

        self.plot_candidates(candidates_of_tracks=candidates_of_tracks, tracks_names=tracks_names)

        # Перерисовываем холст
        self.canvas.draw()

    def plot_candidates(self, candidates_of_tracks: List[List[float]], tracks_names: List[str]):
        if len(candidates_of_tracks) != len(tracks_names):
            raise ValueError("Length of candidates_of_tracks and tracks_names must be equal")

        # Generate distinct colors for each track
        colormap = plt.colormaps['tab20']
        colors = colormap(np.linspace(0, 1, len(candidates_of_tracks)))


        for i, (candidates, name) in enumerate(zip(candidates_of_tracks, tracks_names)):
            if not candidates:
                continue

            first_line = True
            for candidate in candidates:

                self.ax.axvline(
                    x=candidate,
                        color=colors[i],
                        alpha=0.5,
                        linestyle='-',
                        linewidth=1,
                    label=name if first_line else None
                    )
                first_line = False

        # Add legend (only show one entry per track)
        self.ax.legend()

        # Optional: improve layout
        self.ax.grid(True, alpha=0.3)


    def _on_click(self, event):
        """Обработчик клика по графику"""
        self.popup_manager.create_popup(self.master, self.ax)



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
        entry_view = MultitrackResultView(root)
        entry_view.pack(fill=tk.BOTH, expand=True, pady=10)
        left = points_dict["p1"]
        right = points_dict["p3"]
        true = points_dict["p2"]

        candidates1 = [left+ 0.1*(right-left), left+ 0.2*(right-left), left+ 0.7*(right-left)]
        candidates2 = [left + 0.3 * (right - left), left + 0.4 * (right - left)]
        candidates3 = [left + 0.5 * (right - left), left + 0.6 * (right - left)]

        entry_view.plot(signal=signal, time=time, left=left, right=right, true=true, candidates_of_tracks=[candidates1, candidates2, candidates3], tracks_names=["1", "2", "3"])

        root.mainloop()






