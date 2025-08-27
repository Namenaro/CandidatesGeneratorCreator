import numpy as np

from candidates_selection.step_constructor import Step
from settings import TYPES_OF_STEP


class SmoothPreserveBordersMean(Step):
    """
    Сглаживание с сохранением граничных значений
    """
    type_of_step = TYPES_OF_STEP.signal
    comment = "скользящим средним сглаживаем сигнал внутри области поиска (а за ней сигнал не трогаем)"

    def __init__(self, window_size_int: int = 5):
        self.window_size_int = window_size_int

        if self.window_size_int % 2 == 0:
            self.window_size_int += 1

    def smooth_gradual(self, data):
        """
        Постепенное сглаживание с уменьшением влияния к границам
        """

        half_window = self.window_size_int // 2
        result = np.copy(data)
        n = len(data)

        # Обрабатываем каждую точку с учетом ее положения
        for i in range(n):
            if i < half_window or i >= n - half_window:
                # Близко к границе - меньшее сглаживание
                effective_window = min(i + 1, n - i, half_window + 1)
                if effective_window % 2 == 0:
                    effective_window -= 1

                start = max(0, i - effective_window // 2)
                end = min(n, i + effective_window // 2 + 1)

                result[i] = np.mean(data[start:end])
            else:
                # Центральная часть - полное сглаживание
                start = i - half_window
                end = i + half_window + 1
                result[i] = np.mean(data[start:end])

        return result

    def run(self, signal, left: float, right: float):
        if len(signal) <= 1:
            return []

        int_coord_left, int_coord_right = Step.get_borders_as_ints(left, right=right, signal=signal)
        if int_coord_left is None:
            return signal  # ничего не сглаживаем, потому что какая-то проблема с интервалом рассмотрения

        # Создаем копию сигнала
        result = np.copy(signal)

        # Извлекаем фрагмент для сглаживания
        fragment = signal[int_coord_left:int_coord_right + 1]

        if len(fragment) > self.window_size_int:
            self.window_size_int = len(fragment)

        # Сглаживаем фрагмент
        smoothed_fragment = self.smooth_gradual(fragment)

        # Заменяем фрагмент в результате
        result[int_coord_left:int_coord_right + 1] = smoothed_fragment

        return list(result)
