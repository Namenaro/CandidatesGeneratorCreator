from candidates_selection.step_constructor import StepsLibrary
from settings import TYPES_OF_STEP
from dataset_forms.dataset_wrapper import DatasetWrapper, POINTS_DATASET_JSON_KEYS
from candidates_selection.multitrack_results import MultitrackResult
from candidates_selection.multitrack import MultiTrack, create_multitrack_from_json

from typing import List, Optional, Dict


class Model:
    def __init__(self,  multitrack_filename:str, form_dataset_filename:str, indices_in_dataset:Optional[List[int]]=None) :
        """

        :param form_dataset_filename:
        :param indices_in_dataset:
        :param multitrack_filename:
        """
        print(f"Датасет формы {form_dataset_filename}\n файл с сигнатурой мультитрека {multitrack_filename}\n индексы примеров {indices_in_dataset}")

        self.steps_library = StepsLibrary()  # Инициализируем библиотеку шагов
        self.dataset = DatasetWrapper(form_dataset_filename)  # Инициализируем  датасет


        if indices_in_dataset is None:
            self.indices = list(range(len(self.dataset)))
        else:
            self.indices = indices_in_dataset

        self.current_entry:Optional[Dict] = None

        self.multitrack_filename = multitrack_filename # редактируемый файл с мультритреком, ради которого запущена сессия


    def get_steps_types_names(self)->List[str]:
        """ Список названий классов в формате тип_шага--имя шага""" #TODO
        #names = []
        #candidates_types = self.steps_library.get_class_names_by_type(TYPES_OF_STEP.candidates)
        return self.steps_library.get_class_names()

    def get_step_dict_by_type_name(self, type_name: str)->Dict:
        return self.steps_library.get_class_parameters(type_name)





if __name__ == "__main__":
    from paths import PATH_TO_MULTITRACKS, PATH_TO_FORMS_DATASETS

    multitrack_filename = PATH_TO_MULTITRACKS +"\\test_multi.json"
    form_dataset_filename = PATH_TO_FORMS_DATASETS + "\\RS_i.json"

    model = Model(multitrack_filename=multitrack_filename, form_dataset_filename=form_dataset_filename, indices_in_dataset=[0,1,2,3,4])