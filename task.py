import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Task:
    multitrack_filename: Optional[str] = None
    form_dataset_filename: Optional[str] = None
    indices_in_dataset: Optional[List[int]] = None
    left_name: Optional[str] = None
    right_name: Optional[str] = None
    target_name: Optional[str] = None


def fill_task_manually() -> Optional[Task]:
    def on_ok():
        # Проверка обязательных полей
        if not left_name_entry.get():
            messagebox.showerror("Ошибка", "Не заполнено поле left_name")
            return
        if not right_name_entry.get():
            messagebox.showerror("Ошибка", "Не заполнено поле right_name")
            return
        if not target_name_entry.get():
            messagebox.showerror("Ошибка", "Не заполнено поле target_name")
            return
        if not multitrack_filename_var.get():
            messagebox.showerror("Ошибка", "Не выбран файл мультитрека")
            return
        if not dataset_filename_var.get():
            messagebox.showerror("Ошибка", "Не выбран файл датасета")
            return

        # Парсинг индексов
        indices_text = indices_entry.get()
        indices = None
        if indices_text:
            try:
                indices = [int(idx.strip()) for idx in indices_text.split(",")]
            except ValueError:
                messagebox.showerror("Ошибка", "Индексы должны быть числами, разделенными запятыми")
                return

        # Создание и заполнение объекта Task
        task = Task(
            left_name=left_name_entry.get(),
            right_name=right_name_entry.get(),
            target_name=target_name_entry.get(),
            multitrack_filename=multitrack_filename_var.get(),
            form_dataset_filename=dataset_filename_var.get(),
            indices_in_dataset=indices
        )

        root.destroy()
        nonlocal result
        result = task

    def on_cancel():
        root.destroy()
        nonlocal result
        result = None

    def select_multitrack_file():
        filename = filedialog.askopenfilename(title="Выберите файл мультитрека")
        if filename:
            multitrack_filename_var.set(filename)

    def select_dataset_file():
        filename = filedialog.askopenfilename(title="Выберите файл датасета")
        if filename:
            dataset_filename_var.set(filename)

    result = None

    root = tk.Tk()
    root.title("Создание задачи")

    # Поля для имен
    tk.Label(root, text="left_name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    left_name_entry = tk.Entry(root, width=40)
    left_name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

    tk.Label(root, text="right_name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    right_name_entry = tk.Entry(root, width=40)
    right_name_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

    tk.Label(root, text="target_name:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    target_name_entry = tk.Entry(root, width=40)
    target_name_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

    # Поля для выбора файлов
    multitrack_filename_var = tk.StringVar()
    tk.Label(root, text="Файл мультитрека:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(root, textvariable=multitrack_filename_var, width=30, state='readonly').grid(row=3, column=1, padx=5,
                                                                                          pady=5)
    tk.Button(root, text="Выбрать", command=select_multitrack_file).grid(row=3, column=2, padx=5, pady=5)

    dataset_filename_var = tk.StringVar()
    tk.Label(root, text="Файл датасета:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(root, textvariable=dataset_filename_var, width=30, state='readonly').grid(row=4, column=1, padx=5, pady=5)
    tk.Button(root, text="Выбрать", command=select_dataset_file).grid(row=4, column=2, padx=5, pady=5)

    # Поле для индексов
    tk.Label(root, text="Индексы (через запятую):").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    indices_entry = tk.Entry(root, width=40)
    indices_entry.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

    # Кнопки OK и Отмена
    button_frame = tk.Frame(root)
    button_frame.grid(row=6, column=0, columnspan=3, pady=10)

    tk.Button(button_frame, text="OK", width=10, command=on_ok).pack(side="left", padx=10)
    tk.Button(button_frame, text="Отмена", width=10, command=on_cancel).pack(side="right", padx=10)

    root.mainloop()
    return result