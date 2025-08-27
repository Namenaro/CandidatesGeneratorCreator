from candidates_selection.step_constructor import Step
from settings import TYPES_OF_STEP

import numpy as np
from scipy.signal import savgol_filter


class SmoothSavitzkyGolay(Step):
    """Сглаживает методом Савицкого-Голея весь сигнал"""
    type_of_step = TYPES_OF_STEP.signal
    comment = "Сглаживает методом Савицкого-Голея весь сигнал"

    def __init__(self, kernel_size_int:int = 11,  poly_order=2):
        self.poly_order = poly_order
        self.kernel_size_int = kernel_size_int

        if self.kernel_size_int % 2 == 0:
            self.kernel_size_int += 1

    def run(self, signal, left:float, right:float):
        if len(signal) <=1:
            return []

        if len(signal) < self.kernel_size_int:
            self.kernel_size_int = len(signal)
        # Применяем фильтр Савицкого-Голея
        smoothed_signal = savgol_filter(signal,
                                        window_length=self.kernel_size_int,  # размер окна
                                        polyorder=self.poly_order,  # степень полинома
                                        deriv=0,  # производная
                                        delta=1.0,  # шаг по времени
                                        mode='interp')  # режим обработки границ
        return list(smoothed_signal)



