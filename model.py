from candidates_selection.step_constructor import StepsLibrary
from settings import TYPES_OF_STEP
from dataset_forms.dataset_wrapper import DatasetWrapper, POINTS_DATASET_JSON_KEYS
from candidates_selection.multitrack_results import MultitrackResult
from candidates_selection.multitrack import MultiTrack, create_multitrack_from_json

from typing import List, Optional, Dict
import json5 as json


class Model:
    def __init__(self,  multitrack_filename:str, form_dataset_filename:str, left_name:str, right_name:str, target_name:str, indices_in_dataset:Optional[List[int]]=None) :

        print(f"Датасет формы {form_dataset_filename}\n файл с сигнатурой мультитрека {multitrack_filename}\n индексы примеров {indices_in_dataset}")

        self.steps_library = StepsLibrary()  # Инициализируем библиотеку шагов
        self.dataset = DatasetWrapper(form_dataset_filename)  # Инициализируем  датасет


        if indices_in_dataset is None:
            self.indices = list(range(len(self.dataset)))
        else:
            self.indices = indices_in_dataset


        self.multitrack_filename = multitrack_filename # редактируемый файл с мультритреком, ради которого запущена сессия

        self.tracks_names:Optional[List[str]] = None

        # Поля, связанные с текущей записью из датасета формы
        self.points_dict = None
        self.signal = None
        self.time = None
        self.left_coord = None
        self.right_coord = None
        self.target_coord = None

        # имена точек, для которых разрабатывается мультитрек
        self.left_name=left_name
        self.right_name=right_name
        self.target_name= target_name
        self.results:Optional[MultitrackResult] = None




    def get_steps_types_names(self)->List[str]:
        """ Список названий классов в формате тип_шага--имя шага""" #TODO
        #names = []
        #candidates_types = self.steps_library.get_class_names_by_type(TYPES_OF_STEP.candidates)
        return self.steps_library.get_class_names()

    def get_step_dict_by_type_name(self, type_name: str)->Dict:
        return self.steps_library.get_class_parameters(type_name)

    def reset_entry(self, index_in_dataset:int):
        entry = self.dataset.get_ith_entry(index_in_dataset)
        self.points_dict = entry[POINTS_DATASET_JSON_KEYS.points]
        self.signal, self.time = self.dataset.get_signal_for_ith_entry(index_in_dataset)

        self.left_coord = self.points_dict[self.left_name]
        self.right_coord = self.points_dict[self.right_name]
        self.target_coord = self.points_dict[self.target_name]

    def get_left_right_true_coords(self):
        return self.left_coord, self.right_coord, self.target_coord

    def run_multitrack_on_current_entry(self):
        with open(self.multitrack_filename, 'r') as f:
            multitrack_data = json.load(f)

        multitrack = create_multitrack_from_json(step_library=self.steps_library, data=multitrack_data)
        self.results = multitrack.run(signal=self.signal, left=self.left_coord, right=self.right_coord)
        self.tracks_names = list(multitrack_data.keys())

    def get_signals_history_for_track(self, track_name:str):
        signals_history = self.results.get_track_detailed_history(track_name=track_name)
        signals_history = [self.signal] + signals_history
        if len(signals_history)==1:
            old_signals = [self.signal]
            new_signals = []
        else:
            old_signals = signals_history[:-1]
            new_signals = signals_history[1:]
        return old_signals, new_signals

    def get_final_candidates_for_tracks(self):
        candidates_of_tracks = []
        for track_name in self.tracks_names:
            candidates_of_tracks.append(self.results.get_track_candidates(track_name))
        return candidates_of_tracks, self.tracks_names


    def get_final_candidates_for_track(self, track_name):
        return self.results.get_track_candidates(track_name=track_name)



if __name__ == "__main__":
    from paths import PATH_TO_MULTITRACKS, PATH_TO_FORMS_DATASETS

    multitrack_filename = PATH_TO_MULTITRACKS +"\\test_multi.json"
    form_dataset_filename = PATH_TO_FORMS_DATASETS + "\\RS_i.json"

    model = Model(multitrack_filename=multitrack_filename, form_dataset_filename=form_dataset_filename, indices_in_dataset=[0,1,2,3,4])