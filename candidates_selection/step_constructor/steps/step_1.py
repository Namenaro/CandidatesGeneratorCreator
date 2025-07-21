from ..step import Step
from settings import TYPES_OF_STEP


class TestStepSignal(Step):
    """Пример реализации шага фильтрации"""
    type_of_step = TYPES_OF_STEP.signal
    comment = "Фильтрация значений выше порога"

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    def run(self, signal, left, right):
        return [-x for x in signal ]