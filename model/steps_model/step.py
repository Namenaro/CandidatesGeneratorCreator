from typing import Any, List

class Step:
    """Базовый класс для всех шагов обработки"""
    type_of_step: str = "base"
    comment: str = "Базовый шаг обработки"


    def run(self, signal: List[float] ,left:float, right:float) -> List[float]:
        """Основной метод обработки сигнала"""
        raise NotImplementedError("Each step must implement run() method")