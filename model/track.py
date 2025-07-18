from steps_model import StepsLibrary, Step
from settings import TYPES_OF_STEP, JSON_KEYS

from typing import List, Optional, Dict, Any

class StepResult:
    def __init__(self, signal_or_candidates:List[float], is_signal:bool ):
        self.signal_or_candidates = signal_or_candidates # координаты отобранных кандидатов либо измененный этим шагом сигнал
        self.is_signal = is_signal


class Track:
    def __init__(self, steps_list: List[Step]=None, steps_names:List[str]=None):
        self.steps_list = steps_list
        self.steps_names = steps_names

        self._steps_results:Optional[List[StepResult]] = None

    def run(self, signal, left, right)->List[float]:
        self._steps_results = [] # Инициализируем список результатов

        for step in self.steps_list:
            float_list = step.run(signal, left, right)
            is_signal = True if step.type_of_step is TYPES_OF_STEP.signal else False
            step_result = StepResult(float_list, is_signal)
            self._steps_results.append(step_result)

        if len(self.steps_results) == 0:
            self._steps_results = []
            return []

        if self.steps_list[-1].type_of_step is not TYPES_OF_STEP.candidates:
            raise RuntimeError("Последний шаг трека обязан возвращать координаты кандидатов")

        return self._steps_results[-1].signal_or_candidates


    @property
    def steps_results(self)->List[StepResult]:
        if self._steps_results is None:
            raise RuntimeError("Прежде чем запрашивать детали выполнения, нужно запустить выполнение")
        return self._steps_results


def create_track_from_json(data:List[Dict[str, Any]], step_library:StepsLibrary) -> Track:
    steps_list, steps_names=[], []

    for step_description in data:
        # имя шага в треке, если оно есть
        step_name= step_description.get(JSON_KEYS.STEP_ID_IN_TRACK, '')
        steps_names.append(step_name)

        # название класса из библиотеки шагов
        class_name = step_description[JSON_KEYS.STEP_CLASS_NAME]

        # аргументы в конструктор шага
        args = step_description[JSON_KEYS.STEP_ARGS]

        step_obj = step_library.create_instance(class_name=class_name, parameters_json=args)
        steps_list.append(step_obj)

    track = Track(steps_list=steps_list, steps_names=steps_names)
    return track

