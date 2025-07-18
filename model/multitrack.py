from steps_model import StepsLibrary, Step
from track import Track, StepResult
from settings import TYPES_OF_STEP, JSON_KEYS

from typing import List, Optional, Dict, Any

class MultitrackResult:
    """
     Контейнер, хранящий результаты запуска мультитрека на данном сигнале.
     Хранит краткие и детализированные результаты выполнения по каждому треку.
     Краткие участвуют в работе итоговой системы разметки, а детализированные
     нужны для визуальной отладки при разработке новых мультитреков в редакторе.
    """
    def __init__(self):
        self.tracks_names_to_candidates: Dict[str: List[float]] = {}
        self.tracks_names_to_lists_of_steps_results: Dict[str: List[StepResult]] = {}

    def add_track_candidates(self, track_name:str, track_candidates:List[float]):
        """
        Добавить  краткий результат выполнения данного трека.
        :param track_name: имя трека в мультитреке
        :param track_candidates: координаты кандидатов, отобранных треком
        :return:
        """
        self.tracks_names_to_candidates[track_name] = track_candidates

    def add_track_detailed_history(self, track_name:str, steps_names_to_results: Dict[str, List[StepResult]]):
        """
        Для визуальной отладки: пошаговая история выполнения трека на этом сигнале
        :param track_name: id трека в мультитреке
        :param steps_names_to_results: соответствие между именем шага в треке и результатов этого шага. Ключ - имя шага.
        """
        self.tracks_names_to_lists_of_steps_results[track_name] = steps_names_to_results

    def get_track_detailed_history(self, track_name:str)->Dict[str: List[StepResult]]:
        return self.tracks_names_to_lists_of_steps_results[track_name]

    def get_track_candidates(self, track_name:str)->List[float]:
        return self.tracks_names_to_candidates[track_name]

    def get_all_candidates(self, epsilon=0.0001):
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



class MultiTrack:
    def __init__(self, tracks_names:List[str]=None, tracks:List[Track]=None):
        self.tracks_names = tracks_names
        self.tracks = tracks

    def run(self, signal, left, right)->MultitrackResult:
        result = MultitrackResult()
        for i in range(len(self.tracks)):
            track = self.tracks[i]
            track_name = self.tracks_names[i]





