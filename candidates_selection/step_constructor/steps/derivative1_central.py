import numpy as np

from candidates_selection.step_constructor import Step
from settings import TYPES_OF_STEP


class Derivative1_central(Step):
    type_of_step = TYPES_OF_STEP.signal
    comment = ""

    def __init__(self):
        pass

    def run(self, signal, left: float, right: float):
        if len(signal) <= 1:
            return []

        signal = np.asarray(signal, dtype=float)
        derivative = np.zeros_like(signal)

        # Берет f'(x) ≈ (f(x+h) - f(x-h)) / (2h)    при h = 1
        derivative[1:-1] = (signal[2:] - signal[:-2]) / 2
        derivative[0] = signal[1] - signal[0]  # прямая разность для первого элемента
        derivative[-1] = signal[-1] - signal[-2]  # обратная для последнего

        return list(derivative)
