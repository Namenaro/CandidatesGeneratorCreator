from step_constructor import StepsLibrary
from track import Track, create_track_from_json


from typing import List, Dict, Any

class MultitrackResult:
    """
     Контейнер, хранящий результаты запуска мультитрека на данном сигнале.
     Хранит краткие и детализированные результаты выполнения по каждому треку.
     Краткие участвуют в работе итоговой системы разметки, а детализированные
     нужны для визуальной отладки при разработке новых мультитреков в редакторе.
    """
    def __init__(self):
        # Какой трек каких координат-канждидатов вернул (порядок треков не важен, они все выполняются параллельно)
        self.tracks_names_to_candidates: Dict[str: List[float]] = {}

        # Для каждого трека подробная история пошаговой маодификации сигнала
        # в треке перед последним шагом взятия кандидатов. Каждому треку соотв.
        # список сигналов в мВ, порядок соотв. порядку шагов
        self.tracks_names_to_lists_of_steps_results: Dict[str: List[List[float]]] = {}

    def add_track_candidates(self, track_name:str, track_candidates:List[float]):
        """
        Добавить  краткий результат выполнения данного трека.
        :param track_name: имя трека в мультитреке
        :param track_candidates: координаты кандидатов, отобранных треком
        :return:
        """
        self.tracks_names_to_candidates[track_name] = track_candidates

    def add_track_detailed_history(self, track_name:str, steps_results:List[List[float]]):
        """
        Для визуальной отладки: пошаговая история выполнения трека на этом сигнале
        :param track_name: id трека в мультитреке
        :param steps_results: список модифицированных сигналов в мВ, нумерация в котором
                совпадает с нумерацией имен шагов в Track
        """
        self.tracks_names_to_lists_of_steps_results[track_name] = steps_results

    def get_track_detailed_history(self, track_name:str)->List[List[float]]:
        """ Получить для данного трека результаты каждого шага выполнения
         этого трека, нумерация совпадает с нумерацией имен шагов в треке

         :param track_name: id трека в мультитреке
         """
        return self.tracks_names_to_lists_of_steps_results[track_name]

    def get_track_candidates(self, track_name:str)->List[float]:
        """
        Для трека получить список координат кандидатов, которые являются результатом выполнения трека
        :param track_name: id трека в мультитреке
        :return: список координат
        """
        return self.tracks_names_to_candidates[track_name]

    def get_all_candidates(self, epsilon=0.0001)->List[float]:
        """
        Получить кандидатов, получившихся выполнением всего мультитрека.
        Производится удаление дублей (т.е. очень близких точек с точностью до эпсилон)
        :param epsilon: расстояние в секундах, если точки на таком расстоянии, то считаются одной и той же точкой.
        :return: список координат
        """
        # Собираем все элементы из всех списков в один
        all_values = []
        for candidates in self.tracks_names_to_candidates.values():
            all_values.extend(candidates)

        if not all_values:
            return []

        # удалим дубли (значения, который близки с точностью до epsilon)
        # Сортируем все значения по возрастанию
        all_values_sorted = sorted(all_values)

        # Проходим по отсортированному списку и объединяем близкие значения
        result = self.remove_duplicates(all_values_sorted, tolerance=epsilon)
        return result

    @staticmethod
    def remove_duplicates(arr_sorted, tolerance):
        result = [arr_sorted[0]]
        for num in arr_sorted[1:]:
            if abs(num - result[-1]) > tolerance:
                result.append(num)
        return result