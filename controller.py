import tkinter as tk
import easygui
import json5 as json

from model import Model
from test_multitrack import TestMultitrack
from candidates_selection.multitrack import MultiTrack, create_multitrack_from_json
from views.main_view import MainView

class Controller:
    def __init__(self, model:Model, root):
        self.model = model

        self.main_view = MainView(master=root, json_to_redact=self.model.multitrack_filename,
                                  get_steps_types_names=self.model.get_steps_types_names,
                                get_step_dict_by_type_name=self.model.get_step_dict_by_type_name,
                                  save_and_run=self.save_and_run,
                                  next_entry = self.next_entry,
                                  prev_entry=self.prev_entry,
                                  run_test_multitrack=self.run_test_multitrack)

        self.main_view.pack(fill="both", expand=True)
        self.main_view.reset_multitrack_info(self.model.multitrack_filename)

        self.entry_i = -1
        self.max_i = len(self.model.indices)-1


    def save_and_run(self):
        if self.entry_i<0:
            self.next_entry()
        # сохраняем все содержимое редактора в редактируемый в этой сессии файл
        self.main_view.multitrack_editor.save_multitrack()

        # восстанавливаем мультритрек из этого файла,запускаем его на текущей entry
        self.model.run_multitrack_on_current_entry()


        # отрисовывем историю текущего трека
        current_track_name = self.main_view.multitrack_editor.get_current_track_name()

        old_signals, new_signals = self.model.get_signals_history_for_track(current_track_name)
        final_candidates = self.model.get_final_candidates_for_track(current_track_name)
        left, right, true = self.model.get_left_right_true_coords()
        self.main_view.track_view.plot(left, right, true,
                                       time=self.model.time,
                                       old_signals=old_signals,
                                       new_signals=new_signals,
                                       final_candidates=final_candidates,
                                       description=None)

        # отрисовываем сводный результат мультитрека
        candidates_of_tracks, tracks_names = self.model.get_final_candidates_for_tracks()
        self.main_view.multitrack_result.plot(signal=self.model.signal,
                                              time=self.model.time,
                                              left=left,
                                              right=right,
                                              true=true,
                                              candidates_of_tracks=candidates_of_tracks,
                                            tracks_names=tracks_names)

        self.main_view.track_view.text_field.delete(0, tk.END)  # Очистка всего текста
        self.main_view.track_view.text_field.insert(0, "Трек: " + current_track_name)





    def next_entry(self):
        if self.entry_i >= self.max_i:
            return

        self.entry_i +=1
        index_in_dataset = self.model.indices[self.entry_i]
        self.model.reset_entry(index_in_dataset)
        self.main_view.reset_example_info(f"номер записи {index_in_dataset}")


    def prev_entry(self):
        if self.entry_i <= 0:
            return

        self.entry_i -=1
        index_in_dataset = self.model.indices[self.entry_i]
        self.model.reset_entry(index_in_dataset)
        self.main_view.reset_example_info(f"номер записи {index_in_dataset}")

    def run_test_multitrack(self):
        print("Тестирование мультитрека")
        with open(self.model.multitrack_filename, 'r') as f:
            multitrack_data = json.load(f)

        multitrack = create_multitrack_from_json(step_library=self.model.steps_library,
                                                 data=multitrack_data)

        test = TestMultitrack(multitrack=multitrack,
                              dataset=self.model.dataset,
                              left_name=self.model.left_name,
                              right_name=self.model.right_name,
                              target_name=self.model.target_name)

        mean_err, mean_num_candidates, indices_of_worst, errors_of_worst = test.run()
        easygui.msgbox(f"средняя ошибка {mean_err}, среднее кол-во кандидатов {mean_num_candidates}, \n Индексы худших {indices_of_worst}, \n их ошибки {errors_of_worst} ", title="Результат теста")









