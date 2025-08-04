import tkinter as tk

from model import Model
from controller import Controller

from paths import PATH_TO_MULTITRACKS, PATH_TO_FORMS_DATASETS

class Task:
    def __init__(self, left_name:str, right_name:str, target_name:str):
        self.multitrack_filename=None
        self.form_dataset_filename = None

        self.indices_in_dataset = None

        self.left_name = left_name
        self.right_name = right_name
        self.target_name = target_name


def create_dammy_task():
    task = Task(left_name = 'p1', right_name = 'p3', target_name = 'p2')
    task.indices_in_dataset = [0, 1, 2, 3, 4]
    task.form_dataset_filename = PATH_TO_FORMS_DATASETS + "\\RS_i.json"
    task.multitrack_filename = PATH_TO_MULTITRACKS +"\\цц.json"
    return task

if __name__ == "__main__":
    task = create_dammy_task()

    model = Model(multitrack_filename=task.multitrack_filename,
                  form_dataset_filename=task.form_dataset_filename,
                  indices_in_dataset=task.indices_in_dataset,
                  left_name=task.left_name,
                  right_name = task.right_name,
                  target_name=task.target_name
                  )

    root = tk.Tk()
    root.title("Анализ мультитреков")

    # Устанавливаем окно в максимальный размер
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width - 100}x{screen_height - 100}+0+0")
    root.state('zoomed')



    controller = Controller(model, root)
    root.mainloop()
