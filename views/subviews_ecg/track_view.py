import tkinter as tk

from step_signal_view import StepSignalView
from candidates_view import CandidatesView

from typing import List, Optional

class TrackView(tk.Frame):
    """ Визуализирует историю трека: первые несколько шагов это шаги типа "сигнал", последний шаг это шаг типа "кандидаты" """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.steps_views = []

        # Добавлено: Верхний фрейм с текстовым полем
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(fill=tk.X, padx=5, pady=5)

        self.text_label = tk.Label(self.top_frame, text="имя трека:")
        self.text_label.pack(side=tk.LEFT)

        self.text_field = tk.Entry(self.top_frame)
        self.text_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Создаем контейнер с прокруткой
        self.canvas = tk.Canvas(self)
        self.scrollbar_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        # Размещаем элементы
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Фрейм для графиков внутри canvas
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw", tags="inner_frame")

        # Настройка прокрутки
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig("inner_frame", width=event.width)


    def plot(self, left:float, right:float, true:float, time:List[float], old_signals:List[List[float]], new_signals:List[List[float]], final_candidates:List[float], description: Optional[str] = None):
        """

        :param left: координата левой границы интервала поиска, в секундах
        :param right: координата правой границы интервала поиска, в секундах
        :param true: координата верного ответа, в секундах
        :param time: моменты времени , их кол-во равно длине массивов old_signals[i], new_signals[i]
        :param old_signals: если new_signals пустой, то old_signals содержит один элемент - исзодный
            сигнал ЭКГ. Иначе  пара old_signals[i], new_signals[i] это входной и выходной сигнал для i-того шага типа "сигнал"
        :param new_signals:  пара old_signals[i], new_signals[i] это входной и выходной сигнал для i-того шага типа "сигнал"
        :param final_candidates: координаты кандидатов на последнем шаге трека
        :param description: имя трека внутри мультитрека
        :return:
        """

        # Установка текста описания
        self.text_field.delete(0, tk.END)
        if description:
            self.text_field.insert(0, description)

        # Очищаем предыдущие графики
        for view in self.steps_views:
            view.destroy()
        self.steps_views.clear()

        # Создаем новые графики для шагов типа "сигнал"
        for i in range(len(new_signals)):
            old_signal = old_signals[i]
            new_signal = new_signals[i]
            view = StepSignalView(self.inner_frame)
            view.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=5)#view.pack(fill=tk.X, expand=True, pady=5)

            view.plot(old_signal=old_signal, new_signal=new_signal,time=time, left=left, right=right, true=true)

            self.steps_views.append(view)

        # созданием новый график для шага типа "кандидаты" -  поверх того сигнала,
        # по которому они искались (не оригиналльный, в общем случае)
        if len(new_signals) == 0:
            last_signal = old_signals[0] # случай, когда изменяющих сигнал шагов не было - тогда кандидаты считаются по сырому ЭКГ
        else:
            last_signal = new_signals[-1]
        view = CandidatesView(self.inner_frame)
        view.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=5)#view.pack(fill=tk.X, expand=True, pady=5)

        view.plot(signal=last_signal, time=time, left=left, right=right, true=true, candidates=final_candidates)

        self.steps_views.append(view)

        self.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    from tkinter import filedialog
    from dataset_forms import DatasetWrapper, POINTS_DATASET_JSON_KEYS

    file_path = filedialog.askopenfilename(
        title="Выберите файл",
        filetypes=(("Все файлы", "*.*"), ("json файлы", "*.json"))
    )

    if file_path:
        dataset = DatasetWrapper(file_path)

        index = 0
        entry = dataset.get_ith_entry(index)

        points_dict = entry[POINTS_DATASET_JSON_KEYS.points]
        signal, time = dataset.get_signal_for_ith_entry(index)
        left = points_dict["p1"]
        right = points_dict["p3"]
        true = points_dict["p2"]

        new_signal1 = [x * 1.5 for x in signal]
        new_signal2 = [x * 0.4-0.2 for x in signal]

        candidates = [left + 0.1 * (right - left), left + 0.2 * (right - left), left + 0.7 * (right - left)]

        # Создаем корневое окно
        root = tk.Tk()
        view = TrackView(root)
        view.pack(fill=tk.BOTH, expand=True, pady=10)
        view.plot(left, right, true=true, time=time, old_signals=[signal, new_signal1], new_signals=[new_signal1, new_signal2], final_candidates=candidates, description="имя трека" )

        root.mainloop()