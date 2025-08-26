from settings import FREQUENCY
from typing import Any, List

class Step:
    """Базовый класс для всех шагов обработки"""
    type_of_step: str = "base"
    comment: str = "Базовый шаг обработки"


    def run(self, signal: List[float] ,left:float, right:float) -> List[float]:
        """Основной метод обработки сигнала"""
        raise NotImplementedError("Each step must implement run() method")

    @staticmethod
    def get_borders_as_ints(left:float, right:float, signal):
        """
        Получить границы интервала поиска не в секундах, а как индексы массива сигнала
        :param left: левая временнАя граница, в секундах
        :param right:  правая временнАя граница, в секундах
        :param signal: сигнал, неважно в чем
        :return:
        """
        int_coord_left = int(left * FREQUENCY)
        int_coord_right = int(right * FREQUENCY)

        # Корректируем left, если он меньше 0
        if int_coord_left < 0:
            int_coord_left = 0

        # Корректируем right, если он выходит за границу списка
        if int_coord_right >= len(signal):
            int_coord_right = len(signal) - 1

        # Если после корректировки left > right, значит диапазон невалиден
        if int_coord_left > int_coord_right:
            int_coord_right = None
            int_coord_left = None

        return int_coord_left, int_coord_right