from candidates_selection.step_constructor import StepsLibrary


class Model:
    def __init__(self, multitrack_filename, form_dataset_filename, indices_in_dataset):
        print(f"Датасет формы {form_dataset_filename}\n файл с сигнатурой мультитрека {multitrack_filename}\n индексы примеров {indices_in_dataset}")

        self.steps_library = StepsLibrary()





if __name__ == "__main__":
    from paths import PATH_TO_MULTITRACKS, PATH_TO_FORMS_DATASETS

    multitrack_filename = PATH_TO_MULTITRACKS +"\\test_multi.json"
    form_dataset_filename = PATH_TO_FORMS_DATASETS + "\\RS_i.json"

    model = Model(multitrack_filename=multitrack_filename, form_dataset_filename=form_dataset_filename, indices_in_dataset=[0,1,2,3,4])