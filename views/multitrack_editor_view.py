from views.subviews_multitrack_editor.track_editor_view import TrackEditorView

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from typing import List, Dict, Callable, Optional


class MultitrackEditorView(tk.Frame):
    def __init__(self, master,
                 get_steps_types_names: Callable[[], List[str]],
                 get_step_dict_by_type_name: Callable[[str], Dict],
                 **kwargs):
        super().__init__(master, **kwargs)

        self.get_steps_types_names = get_steps_types_names
        self.get_step_dict_by_type_name = get_step_dict_by_type_name
        self.json_to_redact = None

        # Основные элементы интерфейса
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # Панель управления
        self.control_panel = tk.Frame(self)
        self.control_panel.pack(fill="x", padx=5, pady=5)

        # Кнопки управления
        self.add_track_btn = ttk.Button(
            self.control_panel,
            text="Добавить трек",
            command=self.add_new_track
        )
        self.add_track_btn.pack(side="left", padx=2)

        self.remove_track_btn = ttk.Button(
            self.control_panel,
            text="Удалить трек",
            command=self.remove_current_track
        )
        self.remove_track_btn.pack(side="left", padx=2)

        self.rename_track_btn = ttk.Button(
            self.control_panel,
            text="Переименовать трек",
            command=self.rename_current_track
        )
        self.rename_track_btn.pack(side="left", padx=2)

        self.save_btn = ttk.Button(
            self.control_panel,
            text="Сохранить мультитрек",
            command=self.save_multitrack
        )
        self.save_btn.pack(side="right", padx=2)

    def add_new_track(self, track_name: str = "Новый трек", steps: Optional[List[Dict]] = None):
        """Добавить новый трек с заданным именем и шагами"""
        if steps is None:
            steps = []

        # Создаем фрейм для новой вкладки
        tab_frame = tk.Frame(self.notebook)
        tab_frame.pack(fill="both", expand=True)

        # Создаем редактор трека
        editor = TrackEditorView(
            tab_frame,
            get_steps_types_names=self.get_steps_types_names,
            get_step_dict_by_type_name=self.get_step_dict_by_type_name
        )
        editor.pack(fill="both", expand=True)
        editor.set_track(steps)

        # Добавляем вкладку
        self.notebook.add(tab_frame, text=track_name)
        self.notebook.select(tab_frame)  # Делаем новой вкладкой текущей

    def remove_current_track(self):
        """Удалить текущий трек"""
        if self.notebook.index("end") == 0:
            return  # Нет вкладок для удаления

        current_tab = self.notebook.select()
        if not current_tab:
            return

        if not messagebox.askyesno(
                "Подтверждение",
                "Вы уверены, что хотите удалить текущий трек?"
        ):
            return

        self.notebook.forget(current_tab)

    def rename_current_track(self):
        """Переименовать текущий трек"""
        current_tab = self.notebook.select()
        if not current_tab:
            return

        current_name = self.notebook.tab(current_tab, "text")

        dialog = tk.Toplevel(self)
        dialog.title("Переименовать трек")
        dialog.geometry("300x120")
        dialog.resizable(False, False)

        # Центрирование диалога
        self._center_dialog(dialog)

        tk.Label(dialog, text="Введите новое имя трека:").pack(pady=(10, 5))

        self.new_name_entry = ttk.Entry(dialog)
        self.new_name_entry.pack(pady=5, padx=10, fill="x")
        self.new_name_entry.insert(0, current_name)
        self.new_name_entry.focus_set()

        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=5)

        ttk.Button(
            button_frame,
            text="Применить",
            command=lambda: self._apply_rename(dialog, current_tab)
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Отмена",
            command=dialog.destroy
        ).pack(side="left", padx=5)

    def _apply_rename(self, dialog, tab_id):
        """Применить переименование трека"""
        new_name = self.new_name_entry.get().strip()
        if not new_name:
            messagebox.showerror("Ошибка", "Имя трека не может быть пустым")
            return

        self.notebook.tab(tab_id, text=new_name)
        dialog.destroy()

    def save_multitrack(self):
        """Сохранить мультитрек в файл"""

        # Проверяем уникальность имён треков
        track_names = []
        for i in range(self.notebook.index("end")):
            tab_id = self.notebook.tabs()[i]
            track_name = self.notebook.tab(tab_id, "text")
            if track_name in track_names:
                messagebox.showerror(
                    "Ошибка сохранения",
                    f"Найдены треки с одинаковыми именами: '{track_name}'\n"
                    "Пожалуйста, переименуйте треки перед сохранением."
                )
                return
            track_names.append(track_name)

        if not self.json_to_redact:
            self._save_as()
            return

        try:
            data = self._get_multitrack_data()
            with open(self.json_to_redact, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Сохранение", "Мультитрек успешно сохранён")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def _save_as(self):
        """Сохранить как новый файл"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if not filename:
            return

        self.json_to_redact = filename
        self.save_multitrack()

    def load_json_multitrack(self, filename: str):
        """Загрузить мультитрек из JSON файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Очищаем текущие вкладки
            while self.notebook.index("end") > 0:
                self.notebook.forget(0)

            # Создаем вкладки для каждого трека
            for track_name, steps in data.items():
                self.add_new_track(track_name, steps)

            self.json_to_redact = filename
            return True

        except Exception as e:
            messagebox.showerror(
                "Ошибка загрузки",
                f"Не удалось загрузить файл {filename}:\n{str(e)}"
            )
            return False

    def _get_multitrack_data(self) -> Dict[str, List[Dict]]:
        """Получить данные всех треков в виде словаря"""
        data = {}
        for i in range(self.notebook.index("end")):
            tab_id = self.notebook.tabs()[i]
            track_name = self.notebook.tab(tab_id, "text")

            # Получаем редактор трека из вкладки
            tab_frame = self.notebook.nametowidget(tab_id)
            editor = tab_frame.winfo_children()[0]  # Первый и единственный child - это TrackEditorView

            data[track_name] = editor.get_track()
        return data

    def _center_dialog(self, dialog):
        """Центрировать диалоговое окно относительно родителя"""
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')


# Пример использования
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
    root.title("Редактор мультитреков")
    root.geometry("1000x700")

    # Создаем главный редактор
    editor = MultitrackEditorView(
        root,
        get_steps_types_names=demo_get_steps_types_names,
        get_step_dict_by_type_name=demo_get_step_dict_by_type_name
    )
    editor.pack(fill="both", expand=True)


    # Меню для демонстрации загрузки/сохранения
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(
        label="Открыть...",
        command=lambda: editor.load_json_multitrack(filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])))
    filemenu.add_command(label="Сохранить", command=editor.save_multitrack)
    filemenu.add_command(label="Сохранить как...", command=editor._save_as)
    menubar.add_cascade(label="Файл", menu=filemenu)
    root.config(menu=menubar)

    root.mainloop()