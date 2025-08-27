import tkinter as tk
from typing import List
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class PlotPopupManager:
    """Класс для управления всплывающими окнами с графиками"""

    def __init__(self):
        self.popup_window = None

    def create_popup(self, parent, ax_data):
        """Создает всплывающее окно с графиком и панелью инструментов"""
        if self.popup_window is not None:
            self.popup_window.lift()
            return

        self.popup_window = tk.Toplevel(parent)
        self.popup_window.title("Matplotlib Navigation")
        self.popup_window.protocol("WM_DELETE_WINDOW", self.close_popup)

        popup_fig = plt.figure(figsize=(8, 6))
        new_ax = popup_fig.add_subplot(111)

        # Копируем данные из исходного графика
        self._copy_ax_content(ax_data, new_ax)

        popup_canvas = FigureCanvasTkAgg(popup_fig, master=self.popup_window)
        popup_canvas.draw()
        popup_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(popup_canvas, self.popup_window)
        toolbar.update()

    def _copy_ax_content(self, source_ax, target_ax):
        """Копирует содержимое осей из source_ax в target_ax"""
        target_ax.set_ylim(source_ax.get_ylim())  # Важно: одинаковые lim'ы!
        # 1. Копируем линии (включая axvline)
        # Для обычных линий (plot):
        for line in source_ax.get_lines():
            # Проверяем, является ли линия axvline/axhline
            xdata = line.get_xdata()
            ydata = line.get_ydata()

            # axvline имеет одинаковые x-координаты
            is_axvline = len(xdata) == 2 and xdata[0] == xdata[1]

            # axhline имеет одинаковые y-координаты
            is_axhline = len(ydata) == 2 and ydata[0] == ydata[1]

            if not (is_axvline or is_axhline):  # Только обычные линии
                target_ax.plot(xdata, ydata,
                               alpha=line.get_alpha(),
                               color=line.get_color(),
                               linestyle=line.get_linestyle(),
                               linewidth=line.get_linewidth(),
                               label=line.get_label(),
                               marker=line.get_marker(),
                               markersize = line.get_markersize())

        # Для вертикальных/горизонтальных линий (axvline/axhline):
        for line in source_ax.lines:
            if len(line.get_xdata()) == 2 and line.get_xdata()[0] == line.get_xdata()[1]:  # axvline
                target_ax.axvline(x=line.get_xdata()[0],
                                  alpha=line.get_alpha(),  # Добавляем прозрачность
                                  color=line.get_color(),
                                  linestyle=line.get_linestyle(),
                                  linewidth=line.get_linewidth())
            elif len(line.get_ydata()) == 2 and line.get_ydata()[0] == line.get_ydata()[1]:  # axhline
                target_ax.axhline(y=line.get_ydata()[0],
                                  alpha=line.get_alpha(),  # Добавляем прозрачность
                                  color=line.get_color(),
                                  linestyle=line.get_linestyle(),
                                  linewidth=line.get_linewidth())

        # Применяем функцию копирования
        copy_vertical_elements(source_ax, target_ax)


        # Копируем ОСНОВНУЮ сетку (major)
        major_grid_lines = source_ax.xaxis.get_gridlines()
        if major_grid_lines and major_grid_lines[0].get_visible():
            target_ax.grid(True, which='major',
                           linestyle=major_grid_lines[0].get_linestyle(),
                           linewidth=major_grid_lines[0].get_linewidth(),
                           alpha=major_grid_lines[0].get_alpha(),
                           color=major_grid_lines[0].get_color())

        # Копируем МИНОРНУЮ сетку (minor)
        minor_grid_lines = source_ax.xaxis.get_minorticklocs()  # Получаем позиции минорных линий
        if len(minor_grid_lines) > 0:  # Если есть минорные линии
            target_ax.grid(True, which='minor',
                           linestyle=':',  # Стандартный стиль минорной сетки
                           linewidth=0.5,
                           alpha=0.5,
                           color='gray')
            target_ax.minorticks_on()

        # 2. Копируем коллекции (scatter, bar и т.д.)
        for collection in source_ax.collections:
            offsets = collection.get_offsets()
            target_ax.scatter(offsets[:, 0], offsets[:, 1],
                              label=collection.get_label(),
                              color=collection.get_facecolor(),
                              s=collection.get_sizes()[0] if collection.get_sizes().size > 0 else 20)



        target_ax.set_title(source_ax.get_title())
        target_ax.set_xlabel(source_ax.get_xlabel())
        target_ax.set_ylabel(source_ax.get_ylabel())
        if source_ax.get_legend() is not None:
            target_ax.legend()




    def close_popup(self):
        """Закрывает всплывающее окно"""
        if self.popup_window is not None:
            self.popup_window.destroy()
            self.popup_window = None


# Функция для точного копирования вертикальных линий и областей
def copy_vertical_elements(src_ax, dst_ax):

    # Копируем axvspan (хранятся в patches)
    for patch in src_ax.patches:
        if isinstance(patch, plt.Rectangle):
            width = patch.get_width()
            if width > 0:  # Это axvspan, а не линия
                x = patch.get_x()
                dst_ax.axvspan(x, x + width,
                               ymin=0,
                               ymax=1,
                               alpha=patch.get_alpha(),
                               color=patch.get_facecolor(),
                               label=patch.get_label())


