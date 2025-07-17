from ..step import Step


class GlobalMax(Step):
    """Пример реализации шага фильтрации"""
    type_of_step = "candidates"
    comment = "Максимум сигнала"

    def __init__(self):
        pass

    def run(self, signal):
        return max(signal)