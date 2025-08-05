import numpy as np
from typing import List

from dataset_forms.dataset_wrapper import DatasetWrapper, POINTS_DATASET_JSON_KEYS
from candidates_selection.multitrack import MultiTrack
from candidates_selection.multitrack_results import MultitrackResult
from settings import FREQUENCY

class TestMultitrack:
    def __init__(self, multitrack, dataset, left_name:str, right_name:str, target_name:str):
        self.errs_list:List[float] = []
        self.num_candidates:List[float] = []

        self.multitrack:MultiTrack = multitrack
        self.dataset:DatasetWrapper = dataset

        self.left_name = left_name
        self.right_name = right_name
        self.target_name =target_name

    def _fill_stat(self):

        for index_in_dataset in range(len(self.dataset)):
            entry = self.dataset.get_ith_entry(index_in_dataset)
            points_dict = entry[POINTS_DATASET_JSON_KEYS.points]
            signal, time_global = self.dataset.get_signal_for_ith_entry(index_in_dataset)

            # координаты важных точек в полнораземрном сигнале:
            left_coord_global = points_dict[self.left_name]
            right_coord_global = points_dict[self.right_name]
            target_coord_global = points_dict[self.target_name]

            # координаты важных точек в отрезке сигнала:
            start = time_global[0]
            left_coord = left_coord_global - start
            right_coord = right_coord_global - start
            target_coord = target_coord_global - start

            time = [t - start for t in time_global]

            self._handle_entry(time=time,
                               signal=signal,
                               left_coord=left_coord,
                               right_coord=right_coord,
                               target_coord=target_coord)

    def _handle_entry(self, time, signal, left_coord, right_coord, target_coord):
        results:MultitrackResult = self.multitrack.run(signal=signal,
                                      left=left_coord,
                                      right=right_coord)

        final_candidates = results.get_all_candidates(epsilon=0.1/FREQUENCY)
        self.num_candidates.append(len(final_candidates))

        dist_to_best_candidate = self._find_min_distance(final_candidates=final_candidates, target=target_coord)
        self.errs_list.append(dist_to_best_candidate)
        print(dist_to_best_candidate)


    def _find_min_distance(self, final_candidates: List[float], target: float) -> float:
        if not final_candidates:
            raise ValueError("Список кандидатов от мультитрека не должен быть пустым")

        min_distance = abs(final_candidates[0] - target)
        for num in final_candidates[1:]:
            current_distance = abs(num - target)
            if current_distance < min_distance:
                min_distance = current_distance




        return min_distance




    def run(self):
        self._fill_stat()
        # вернуть среднюю ошибку лучшего кандидата, среднее количество кандидатов
        mean_err = np.mean(self.errs_list)
        mean_num_of_candidates = np.mean(self.num_candidates)

        n = 5  #  получить индексы n наибольших элементов (т.е. наибольшая ошибка мультритерка)
        indices_of_worst = sorted(range(len(self.errs_list)), key=lambda i: self.errs_list[i], reverse=True)[:n]
        errors_of_worst = [self.errs_list[i] for i in indices_of_worst]

        return mean_err, mean_num_of_candidates, indices_of_worst, errors_of_worst