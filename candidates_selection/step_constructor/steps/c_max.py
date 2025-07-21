from ..step import Step
from settings import TYPES_OF_STEP

from typing import List

class GlobalMax(Step):
    """Пример реализации шага фильтрации"""
    type_of_step = TYPES_OF_STEP.candidates
    comment = "Максимум сигнала"

    def __init__(self):
        pass

    def run(self, signal, left, right)->List[float]:
        """

        :param signal:
        :param left:
        :param right:
        :return: координата победителя
        """
        return [1/500]