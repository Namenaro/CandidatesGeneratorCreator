from sympy.printing.pretty.pretty_symbology import line_width

from utils import plot_lead_signal_to_ax

import tkinter as tk

from interactive_manager import InteractiveManager

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import List



class StepSignalView(tk.Frame):
    """ Визуализирует результат шага, относящегося к типу шагов, изменяющих сигнал.
    График интерактивен: есть зум колесиком мыши, перетаскивание, возфращение масщтаба при клике на правую кнопку мыши"""
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg='white', padx=5, pady=5)

        # Создаем фигуру и оси
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.interactive = InteractiveManager(self.ax)


        # Создаем холст для графика
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)


    def plot(self, old_signal:List[float], new_signal:List[float],time:List[float], left:float, right:float, true:float):
        """

        :param old_signal: сигнал до изменения, мВ
        :param new_signal: сигнал после изменения, мВ
        :param time: в секундах, оно одинаковое для обоих сигналов
        :param left: левая граница временного интервала, в котором мультитрек будет искать кандидатов
        :param right: левая граница временного интервала, в котором мультитрек будет искать кандидатов
        :param true: правильный ответ, где находится точка, которую мы пытаемся поставить этим мультитреком, берется из датасета формы
        :return:
        """
        self.ax.clear()

        # рисуем старый и новый сигналы
        max_y = max(max(old_signal), max(new_signal))*1.1
        min_y = min(min(old_signal), min(new_signal))
        min_y = min_y - 0.1 * abs(min_y)
        plot_lead_signal_to_ax(signal_mV=old_signal, ax=self.ax, time=time, Y_max=max_y,
                               Y_min=min_y, color='gray', alpha=0.4, linestyle='--')

        plot_lead_signal_to_ax(signal_mV=new_signal, ax=self.ax, time=time, Y_max=max_y,
                               Y_min=min_y, color='green', alpha=0.6)

        # рисуем допустимую область
        self.ax.axvline(left, color='r', linestyle='-', alpha=0.7,  linewidth=0.3)
        self.ax.axvline(right, color='r', linestyle='-', alpha=0.7, linewidth=0.3)

        self.ax.axvspan(left, right,
                   facecolor='r', alpha=0.1,
                   ymin=0, ymax=1)

        # рисуем правильный ответ (где должна реально стоять целевая точка этого мультитрека)
        self.ax.axvline(true, color='g', linestyle='--', alpha=0.5, picker=5)

        # Обновляем начальные границы после создания графика
        self.interactive.initial_xlim = self.ax.get_xlim()
        self.interactive.initial_ylim = self.ax.get_ylim()
        self.interactive.initial_center = (
            (self.interactive.initial_xlim[0] + self.interactive.initial_xlim[1]) / 2,
            (self.interactive.initial_ylim[0] + self.interactive.initial_ylim[1]) / 2
        )

        # Перерисовываем холст
        self.canvas.draw()



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
        entry_view = StepSignalView(root)
        entry_view.pack(fill=tk.BOTH, expand=True, pady=10)
        left = points_dict["p1"]
        right = points_dict["p3"]
        true = points_dict["p2"]
        new_signal = [x * 2 for x in signal]
        entry_view.plot(old_signal=signal, new_signal=new_signal,time=time, left=left, right=right, true=true)

        root.mainloop()






