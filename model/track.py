from steps_model import StepsLibrary, Step
from settings import TYPES_OF_STEP, JSON_KEYS

from typing import List, Dict, Any



class Track:
    def __init__(self, steps_list: List[Step]=None, steps_names:List[str]=None):
        """
        Трек это несколько шагов преобразования сигнала и в конце один щаг взятия кандидатов
         как "особенных" точек полученного после преобразований сигнала
        :param steps_list: объекты, осуществляющие шаг, порядок важен
        :param steps_names: id шагов в данном треке, если есть
        """
        self.steps_list = steps_list
        self.steps_names = steps_names

        # сигнал после каждого шага его изменения, например, steps_signals[i] это сигнал в мВ после применения i-того шага
        self.steps_signals: List[List[float]]= []
        self.candidates_coords: List[float] = [] # координаты кандидатов после последнего шага

    def fill_results(self, signal, left, right):
        # Очищаем результаты предыдущего запуска
        self.steps_signals = []
        self.candidates_coords = []

        # Если шагов более одного, то все кроме последнего - шаги модицикации сигнала
        if len(self.steps_list) > 1:
            prev_signal = signal
            for step in self.steps_list[0:-2]:
                new_signal = step.run(prev_signal, left, right)
                self.steps_signals.append(new_signal)
                prev_signal = new_signal


        # Последний шаг трека всегда селектор кандидатов
        if self.steps_list[-1].type_of_step is not TYPES_OF_STEP.candidates:
            raise RuntimeError("Последний шаг трека обязан возвращать координаты кандидатов")

        self.candidates_coords = self.steps_list[-1].run(signal, left, right)



    def get_candidates_coords(self)->List[float]:
        return self.candidates_coords

    def get_history_signal_changes(self)->List[List[float]]:
        return self.steps_signals


def create_track_from_json(data:List[Dict[str, Any]], step_library:StepsLibrary) -> Track:
    """
    Конструирует объект Трека по фрагменту json-описания, структуру json см в settings.JSON_KEYS
    :param data: данные после десериализации json-а с треком
    :param step_library: конкструирует объект шага по словарю аргументов
    :return:
    """
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

