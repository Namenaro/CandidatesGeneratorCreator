import tkinter as tk

from model import Model
from controller import Controller

from paths import PATH_TO_MULTITRACKS, PATH_TO_FORMS_DATASETS
from task import Task, fill_task_manually


def create_dammy_task():
    indices_in_dataset = [1,2,3]
    form_dataset_filename = PATH_TO_FORMS_DATASETS + "\\p_simpmle_i.json"
    multitrack_filename = PATH_TO_MULTITRACKS +"\\for_form_T.json"

    task = Task(left_name='p1',
                right_name='p3',
                target_name='p2',
                indices_in_dataset=indices_in_dataset,
                form_dataset_filename=form_dataset_filename,
                multitrack_filename=multitrack_filename)
    return task

if __name__ == "__main__":
    #task = create_dammy_task()
    task = fill_task_manually()
    if task is None:
        exit(1)

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
