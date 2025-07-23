from ..step import Step
from settings import TYPES_OF_STEP, FREQUENCY

from typing import List

class GlobalMax(Step):
    """Берется максимум сигнала внутри интервала, включающего обе границы"""
    type_of_step = TYPES_OF_STEP.candidates
    comment = "Максимум сигнала"

    def __init__(self):
        pass

    def run(self, signal, left, right)->List[float]:
        """
        Берется максимум сигнала внтри интервала, включающего обе границы
        :param signal:
        :param left:
        :param right:
        :return: координата победителя, [float]
        """
        int_coord_left = int(left*FREQUENCY)
        int_coord_right = int(right*FREQUENCY)

        # Корректируем left, если он меньше 0
        if int_coord_left < 0:
            int_coord_left = 0

        # Корректируем right, если он выходит за границу списка
        if int_coord_right >= len(signal):
            int_coord_right = len(signal) - 1

        # Если после корректировки left > right, значит диапазон невалиден
        if int_coord_left > int_coord_right:
            return []

        max_index = int_coord_left
        for i in range(int_coord_left + 1, int_coord_right + 1):
            if signal[i] > signal[max_index]:
                max_index = i

        return [max_index/FREQUENCY]

if __name__ == "__main__":
    step = GlobalMax()
    signal = [0,2,1,1,1,4,5,3,-1]
    left = 0
    right = 4/FREQUENCY
    coord = step.run(signal, left, right=right)
    int_coord = int(coord[0]*FREQUENCY)
    print (f" коорд максимума {int_coord}, значение {signal[int_coord]}")