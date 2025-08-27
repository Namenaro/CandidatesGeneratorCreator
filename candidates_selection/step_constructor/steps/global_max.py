from typing import List

import numpy as np

from candidates_selection.step_constructor import Step
from settings import TYPES_OF_STEP, FREQUENCY


class GlobalMax(Step):
    """Берется максимум сигнала внутри интервала, включающего обе границы.  если глобальных максисмумов много, берется самый левый"""
    type_of_step = TYPES_OF_STEP.candidates
    comment = "Максимум сигнала"

    def __init__(self):
        pass

    def run(self, signal, left, right) -> List[float]:
        """
        Берется максимум сигнала внтри интервала, включающего обе границы
        :param signal:
        :param left:
        :param right:
        :return: координата победителя, [float]
        """
        int_coord_left, int_coord_right = Step.get_borders_as_ints(left, right=right, signal=signal)
        if int_coord_left is None:
            return []  # нкакая-то проблема с интервалом рассмотрения

        segment = signal[int_coord_left:int_coord_right + 1]
        max_val = max(segment)
        max_index = int_coord_left + segment.index(max_val)

        return [max_index / FREQUENCY]


if __name__ == "__main__":
    step = GlobalMax()
    signal = [np.float64(-0.0106342953031646), np.float64(-0.011027101022679776), np.float64(-0.011723689300601511),
              np.float64(-0.012566799856055246), np.float64(-0.013371400718072224), np.float64(-0.013978960305321184),
              np.float64(-0.014305822965119532), np.float64(-0.014360739766249912), np.float64(-0.014220073672175159),
              np.float64(-0.013975389895095069), np.float64(-0.013681088771199364), np.float64(-0.013320567854320184),
              np.float64(-0.012798633885763033), np.float64(-0.01197280266370884), np.float64(-0.010729987901895324),
              np.float64(-0.009080803290354714), np.float64(-0.007208839428620132), np.float64(-0.005421874796244399),
              np.float64(-0.004017662109653107), np.float64(-0.003146493638477383), np.float64(-0.0027606147233676936),
              np.float64(-0.0026804769721745663), np.float64(-0.002724931823827944), np.float64(-0.0028130837112475804),
              np.float64(-0.0029796481026040664), np.float64(-0.0033139592785465183),
              np.float64(-0.0038790304396214975), np.float64(-0.004661720250517456), np.float64(-0.005568923122640443),
              np.float64(-0.006457916233885905), np.float64(-0.007183835587605394), np.float64(-0.00764977196020223),
              np.float64(-0.007842789983398662), np.float64(-0.007837509680207543), np.float64(-0.00775928043060309),
              np.float64(-0.0077223688738730315), np.float64(-0.007776572778240709), np.float64(-0.00789377387290024),
              np.float64(-0.008004648605477727), np.float64(-0.008064244126384637), np.float64(-0.008101004053383268),
              np.float64(-0.008211249542180478), np.float64(-0.0084990294310782), np.float64(-0.009004324067534484),
              np.float64(-0.009671562166440054), np.float64(-0.010377748669276213), np.float64(-0.010997307424869195)]
    left = 0
    right = len(signal) / FREQUENCY
    coord = step.run(signal, left, right=right)
    int_coord = int(coord[0] * FREQUENCY)
    print(f" коорд максимума {int_coord}, значение {signal[int_coord]}")
