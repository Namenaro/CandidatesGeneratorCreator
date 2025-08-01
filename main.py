import tkinter as tk
from tkinter import ttk

from model import Model
from controller import Controller



if __name__ == "__main__":
    from paths import PATH_TO_MULTITRACKS, PATH_TO_FORMS_DATASETS

    # запрашиваем пути к файлу мультитрека и датасета формы multitrack_filename, form_dataset_filename, indices_in_dataset
    multitrack_filename = PATH_TO_MULTITRACKS +"\\test_multi.json"
    form_dataset_filename = PATH_TO_FORMS_DATASETS + "\\RS_i.json"
    indices_in_dataset = [0, 1, 2, 3, 4]

    model = Model(multitrack_filename=multitrack_filename, form_dataset_filename=form_dataset_filename, indices_in_dataset=indices_in_dataset)

    root = tk.Tk()
    root.title("Анализ мультитреков")

    # Устанавливаем окно в максимальный размер
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width - 100}x{screen_height - 100}+0+0")
    root.state('zoomed')


    controller = Controller(model, root)
    root.mainloop()
