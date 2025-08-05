
from views.subviews_multitrack_editor.step_editor_view import StepTextRedactor
from settings import JSON_KEYS
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional, Callable


class TrackEditorView(tk.Frame):
    def __init__(self, master,
                 get_steps_types_names: Callable[[], List[str]],
                 get_step_dict_by_type_name: Callable[[str], Dict],
                 **kwargs):
        super().__init__(master, **kwargs)

        self.get_steps_types_names = get_steps_types_names
        self.get_step_dict_by_type_name = get_step_dict_by_type_name

        # Контейнер для кнопки добавления
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(fill="x", padx=5, pady=5)

        # Кнопка добавления шага
        self.add_button = ttk.Button(
            self.control_frame,
            text="Добавить шаг",
            command=self._show_add_step_dialog
        )
        self.add_button.pack(side="left")

        # Основной контейнер с прокруткой
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Настройка canvas и scrollbar'ов
        self.canvas = tk.Canvas(self.container, borderwidth=0, highlightthickness=0)
        self.h_scrollbar = ttk.Scrollbar(self.container, orient="horizontal", command=self.canvas.xview)
        self.v_scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.pack(fill="both", expand=True)

        # Конфигурация прокрутки
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set
        )

        # Настройка прокрутки колесиком мыши
        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)

        # Размещение элементов
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Хранилище для шагов
        self.step_editors = []
        self.step_labels = []
        self.step_frames = []

    def _show_add_step_dialog(self):
        """Показать диалоговое окно для добавления шага"""
        dialog = tk.Toplevel(self)
        dialog.title("Добавить шаг")
        dialog.geometry("350x200")
        dialog.resizable(False, False)

        # Центрирование диалога
        self._center_dialog(dialog)

        # Метка и поле ввода для позиции
        tk.Label(dialog, text="Позиция нового шага:").pack(pady=(10, 0))

        position_frame = tk.Frame(dialog)
        position_frame.pack()

        self.position_entry = ttk.Entry(position_frame, width=5)
        self.position_entry.pack(side="left", padx=5)
        tk.Label(position_frame, text=f"(1-{len(self.step_editors) or 1})").pack(side="left")

        # Выбор типа шага
        tk.Label(dialog, text="Тип шага:").pack(pady=(10, 0))

        self.step_type_var = tk.StringVar()
        step_types = self.get_steps_types_names()

        if not step_types:
            messagebox.showerror("Ошибка", "Нет доступных типов шагов")
            dialog.destroy()
            return

        self.step_type_combobox = ttk.Combobox(
            dialog,
            textvariable=self.step_type_var,
            values=step_types,
            state="readonly"
        )
        self.step_type_combobox.pack(pady=5)
        self.step_type_combobox.current(0)

        # Кнопки
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Добавить",
            command=lambda: self._add_step_from_dialog(dialog)
        ).pack(side="left", padx=10)

        ttk.Button(
            button_frame,
            text="Отмена",
            command=dialog.destroy
        ).pack(side="left", padx=10)

        # Установка фокуса
        self.position_entry.focus_set()

    def _center_dialog(self, dialog):
        """Центрировать диалоговое окно относительно родителя"""
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')

    def _add_step_from_dialog(self, dialog):
        """Обработчик добавления шага из диалога"""
        try:
            # Получаем позицию
            position = self.position_entry.get()
            if not position:
                position = len(self.step_editors)
            else:
                position = int(position)
                if position < 0 or position > len(self.step_editors):
                    raise ValueError("Некорректная позиция")

            # Получаем тип шага
            step_type = self.step_type_var.get()
            if not step_type:
                raise ValueError("Не выбран тип шага")

            # Получаем словарь для нового шага
            step_params = self.get_step_dict_by_type_name(step_type)
            step_data = {}
            step_data[JSON_KEYS.STEP_CLASS_NAME] = step_type
            step_data[JSON_KEYS.STEP_ARGS] = step_params

            dialog.destroy()
            self.add_new_step(step_data, position)

        except ValueError as e:
            messagebox.showerror(
                "Ошибка",
                f"Ошибка при добавлении шага:\n{str(e)}"
            )
            self.position_entry.focus_set()
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось создать шаг:\n{str(e)}"
            )

    def _bind_mousewheel(self, event):
        """Привязать колесико мыши для прокрутки"""
        self.canvas.bind_all("<MouseWheel>", self._on_vertical_scroll)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_horizontal_scroll)

    def _unbind_mousewheel(self, event):
        """Отвязать колесико мыши"""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Shift-MouseWheel>")

    def _on_vertical_scroll(self, event):
        """Вертикальная прокрутка колесиком мыши"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_horizontal_scroll(self, event):
        """Горизонтальная прокрутка колесиком мыши (с зажатым Shift)"""
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def set_track(self, steps_list_data: List[Dict]):
        """Установить список шагов для редактирования"""
        # Очищаем текущие шаги
        for frame in self.step_frames:
            frame.destroy()

        self.step_editors.clear()
        self.step_labels.clear()
        self.step_frames.clear()

        # Создаем новые шаги
        for i, step_data in enumerate(steps_list_data, 1):
            self._create_step_editor(i, step_data)

    def _create_step_editor(self, step_num: int, step_data: Dict):
        """Создать редактор для одного шага"""
        step_frame = tk.Frame(self.scrollable_frame, bd=2, relief=tk.GROOVE, padx=5, pady=5)
        step_frame.pack(fill="x", expand=True, padx=5, pady=5, ipady=5)

        # Заголовок шага с номером
        header_frame = tk.Frame(step_frame)
        header_frame.pack(fill="x")

        label = tk.Label(
            header_frame,
            text=f"Шаг {step_num}",
            font=("Arial", 10, "bold")
        )
        label.pack(side="left")

        # Кнопка удаления
        delete_btn = ttk.Button(
            header_frame,
            text="Удалить",
            command=lambda: self.delete_step(step_num - 1)
        )
        delete_btn.pack(side="left")

        # Редактор шага
        editor = StepTextRedactor(step_frame)
        editor.pack(fill="both", expand=True)
        editor.set_step_dict(step_data)

        # Сохраняем ссылки
        self.step_frames.append(step_frame)
        self.step_editors.append(editor)
        self.step_labels.append(label)

    def get_track(self) -> List[Dict]:
        """Получить список всех шагов"""
        return [editor.get_step_dict() for editor in self.step_editors]

    def add_new_step(self, step_data: Dict, step_num: Optional[int] = None):
        """Добавить новый шаг после указанного номера"""
        if step_num is None:
            step_num = len(self.step_editors)

        if step_num < 0 or step_num > len(self.step_editors):
            raise ValueError("Некорректный номер шага")

        # Создаем новый редактор
        new_editor_frame = tk.Frame(self.scrollable_frame, bd=2, relief=tk.GROOVE, padx=5, pady=5)

        # Вставляем на нужную позицию
        if step_num < len(self.step_frames):
            new_editor_frame.pack(
                in_=self.scrollable_frame,
                before=self.step_frames[step_num],
                fill="x", padx=5, pady=5, ipady=5, expand=True
            )
        else:
            new_editor_frame.pack(fill="x", padx=5, pady=5, ipady=5, expand=True)

        # Заголовок шага
        header_frame = tk.Frame(new_editor_frame)
        header_frame.pack(fill="x")

        label = tk.Label(
            header_frame,
            text=f"Шаг {step_num + 1}",
            font=("Arial", 10, "bold")
        )
        label.pack(side="left")

        # Кнопка удаления
        delete_btn = ttk.Button(
            header_frame,
            text="Удалить",
            command=lambda: self.delete_step(step_num)
        )
        delete_btn.pack(side="right")

        # Редактор шага
        editor = StepTextRedactor(new_editor_frame)
        editor.pack(fill="both", expand=True)
        editor.set_step_dict(step_data)

        # Обновляем списки
        self.step_frames.insert(step_num, new_editor_frame)
        self.step_editors.insert(step_num, editor)
        self.step_labels.insert(step_num, label)

        # Обновляем номера шагов
        self._update_step_numbers()

        # Прокручиваем к новому шагу
        self.canvas.yview_moveto(1.0)

    def delete_step(self, step_num: int):
        """Удалить шаг с указанным номером"""
        if step_num < 0 or step_num >= len(self.step_editors):
            raise ValueError("Некорректный номер шага")

        # Удаляем виджеты
        self.step_frames[step_num].destroy()

        # Удаляем из списков
        self.step_frames.pop(step_num)
        self.step_editors.pop(step_num)
        self.step_labels.pop(step_num)

        # Обновляем номера шагов
        self._update_step_numbers()

    def _update_step_numbers(self):
        """Обновить номера всех шагов"""
        for i, label in enumerate(self.step_labels, 1):
            label.config(text=f"Шаг {i}")

            # Обновляем команду для кнопки удаления
            for btn in self.step_frames[i - 1].winfo_children():
                if isinstance(btn, tk.Frame):
                    for child in btn.winfo_children():
                        if isinstance(child, ttk.Button) and child["text"] == "Удалить":
                            child.config(command=lambda num=i - 1: self.delete_step(num))


if __name__ == "__main__":
    def demo_get_steps_types_names():
        return ["Старт", "Движение", "Остановка", "Поворот", "Ожидание"]


    def demo_get_step_dict_by_type_name(type_name: str):
        templates = {
            "Старт": {"action": "start", "params": {"speed": 0}},
            "Движение": {"action": "move", "params": {"x": 0, "y": 0}},
            "Остановка": {"action": "stop", "params": {}},
            "Поворот": {"action": "rotate", "params": {"angle": 90}},
            "Ожидание": {"action": "wait", "params": {"duration": 1}}
        }
        return templates.get(type_name, {"action": "unknown", "params": {}})


    root = tk.Tk()
    root.title("Редактор трека с типами шагов")
    root.geometry("800x600")

    # Создаем редактор трека с передачей callback-функций
    editor = TrackEditorView(
        root,
        get_steps_types_names=demo_get_steps_types_names,
        get_step_dict_by_type_name=demo_get_step_dict_by_type_name
    )
    editor.pack(fill="both", expand=True, padx=5, pady=5)

    # Устанавливаем начальные данные
    initial_steps = [
        demo_get_step_dict_by_type_name("Старт"),
        demo_get_step_dict_by_type_name("Движение")
    ]
    editor.set_track(initial_steps)

    # Фрейм для кнопок на главной форме
    control_frame = tk.Frame(root)
    control_frame.pack(fill="x", padx=5, pady=5)


    # Кнопка "Получить трек" на главной форме
    def print_track():
        track = editor.get_track()
        print("Текущий трек:")
        for i, step in enumerate(track, 1):
            print(f"Шаг {i}: {step}")


    ttk.Button(
        control_frame,
        text="Получить трек",
        command=print_track
    ).pack(side="left", padx=5)

    root.mainloop()