from candidates_selection.step_constructor import Step
from settings import TYPES_OF_STEP

import numpy as np
from scipy.ndimage import gaussian_filter1d


class GaussianSmooth(Step):
    """Сглаживает гауссовым ядром весь сигнал"""
    type_of_step = TYPES_OF_STEP.signal
    comment = "Сглаживает гауссовым ядром весь сигнал"

    def __init__(self, sigma: float = 2.5, kernel_size_int:int = 21 ):
        """

        :param sigma: Стандартное отклонение гауссова ядра.
        :param kernel_size_int:  Размер ядра фильтра (должен быть нечетным). Измеряется в кол-ве дискретов (т.е. не переводили в секунды)
        """
        self.sigma = sigma
        self.kernel_size_int = kernel_size_int

    def run(self, signal, left:float, right:float):
        """
            Сглаживание одномерного сигнала гауссовым фильтром. Сглажывается весь, так что левая и правая границы не учитывются
            """
        if self.kernel_size_int % 2 == 0:
            self.kernel_size_int += 1

        truncate_value = (self.kernel_size_int - 1) / (2 * self.sigma)
        return gaussian_filter1d(signal, sigma=self.sigma, truncate=truncate_value)
