from ..step import Step


class Step1(Step):
    """Пример реализации шага фильтрации"""
    type_of_step = "filter"
    comment = "Фильтрация значений выше порога"

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    def run(self, signal):
        return [x for x in signal if x > self.threshold]