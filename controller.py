from model import Model
from views.main_view import MainView

class Controller:
    def __init__(self, model:Model, root):
        self.model = model

        self.main_view = MainView(master=root,
                                  get_steps_types_names=self.model.get_steps_types_names,
                         get_step_dict_by_type_name=self.model.get_step_dict_by_type_name)
        self.main_view.pack(fill="both", expand=True)
        self.main_view.reset_multitrack_info(self.model.multitrack_filename)


