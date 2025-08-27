from candidates_selection.step_constructor import Step
from settings import TYPES_OF_STEP

import numpy as np


class Derivative1_splines(Step):
    type_of_step = TYPES_OF_STEP.signal
    comment = ""

    def __init__(self):
        pass

    def run(self, signal, left:float, right:float):
        if len(signal) <= 1:
            return []

        n = len(signal)
        x = np.arange(n)



        from scipy.interpolate import CubicSpline
        cs = CubicSpline(x, signal)
        result = cs(x, 1)  # первая производная

        return list(result)


