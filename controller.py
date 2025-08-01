from model import Model
from views.main_view import MainView

class Controller:
    def __init__(self, model:Model, root):
        self.model = model

        self.main_view = MainView(master=root, json_to_redact=self.model.multitrack_filename,
                                  get_steps_types_names=self.model.get_steps_types_names,
                                get_step_dict_by_type_name=self.model.get_step_dict_by_type_name,
                                  save_and_run=self.save_and_run,
                                  next_entry = self.next_entry)

        self.main_view.pack(fill="both", expand=True)
        self.main_view.reset_multitrack_info(self.model.multitrack_filename)

        self.entry_i = 0
        self.max_i = len(self.model.indices)-1


    def save_and_run(self):
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



    def next_entry(self):
        if self.entry_i >= self.max_i:
            return

        self.entry_i +=1
        index_in_dataset = self.model.indices[self.entry_i]
        self.model.reset_entry(index_in_dataset)
        self.main_view.reset_example_info(f"номер запаси {index_in_dataset}")







