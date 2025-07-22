

import tkinter as tk
from tkinter import scrolledtext
import json
from typing import Dict, Optional
import re


class StepTextRedactor(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Настройка grid для расширения
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Создание текстового поля с прокруткой
        self.text_widget = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            font=('Consolas', 10),
            undo=True  # Включение отмены действий
        )
        self.text_widget.grid(row=0, column=0, sticky="nsew")

        # Настройка подсветки синтаксиса
        self._setup_syntax_highlighting()

        # Привязка событий
        self.text_widget.bind('<KeyRelease>', self._auto_format)
        self.text_widget.bind('<Control-s>', self._format_json)
        self.text_widget.bind('<Control-r>', self._reformat_json)

    def _setup_syntax_highlighting(self):
        """Настройка подсветки синтаксиса для JSON"""
        self.text_widget.tag_config('key', foreground='blue')
        self.text_widget.tag_config('string', foreground='green')
        self.text_widget.tag_config('number', foreground='dark orange')
        self.text_widget.tag_config('boolean', foreground='purple')
        self.text_widget.tag_config('null', foreground='gray')
        self.text_widget.tag_config('error', background='#ffdddd')

    def _auto_format(self, event=None):
        """Автоматическое форматирование при вводе"""
        if event and event.keysym in ('Return', 'BackSpace', 'Delete'):
            self._reformat_json()

    def _format_json(self, event=None):
        """Форматирование JSON с сохранением позиции курсора"""
        try:
            cursor_pos = self.text_widget.index(tk.INSERT)
            content = self.text_widget.get("1.0", tk.END)
            data = json.loads(content)
            formatted = json.dumps(data, indent=4, ensure_ascii=False)

            if content.strip() != formatted.strip():
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert("1.0", formatted)
                self.text_widget.mark_set(tk.INSERT, cursor_pos)

            self._highlight_syntax()
            self._clear_errors()
            return "break"  # Предотвращаем стандартную обработку события

        except json.JSONDecodeError as e:
            self._mark_error_position(e)
            return "break"

    def _reformat_json(self, event=None):
        """Переформатирование JSON без сохранения позиции курсора"""
        try:
            content = self.text_widget.get("1.0", tk.END)
            data = json.loads(content)
            formatted = json.dumps(data, indent=4, ensure_ascii=False)

            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", formatted)
            self._highlight_syntax()
            self._clear_errors()

        except json.JSONDecodeError as e:
            self._mark_error_position(e)

    def _highlight_syntax(self):
        """Подсветка синтаксиса JSON"""
        self.text_widget.tag_remove('key', "1.0", tk.END)
        self.text_widget.tag_remove('string', "1.0", tk.END)
        self.text_widget.tag_remove('number', "1.0", tk.END)
        self.text_widget.tag_remove('boolean', "1.0", tk.END)
        self.text_widget.tag_remove('null', "1.0", tk.END)

        text = self.text_widget.get("1.0", tk.END)

        # Подсветка ключей
        for match in re.finditer(r'"(.*?)"\s*:', text):
            self.text_widget.tag_add('key',
                                     f"1.0 + {match.start()}c",
                                     f"1.0 + {match.end()}c")

        # Подсветка строковых значений
        for match in re.finditer(r':\s*"(.*?)"(?=\s*[,}\]])', text):
            self.text_widget.tag_add('string',
                                     f"1.0 + {match.start() + 2}c",
                                     f"1.0 + {match.end()}c")

        # Подсветка чисел
        for match in re.finditer(r':\s*(-?\d+\.?\d*)(?=\s*[,}\]])', text):
            self.text_widget.tag_add('number',
                                     f"1.0 + {match.start() + 2}c",
                                     f"1.0 + {match.end()}c")

        # Подсветка булевых значений и null
        for match in re.finditer(r':\s*(true|false|null)(?=\s*[,}\]])', text):
            if match.group(1) in ('true', 'false'):
                self.text_widget.tag_add('boolean',
                                         f"1.0 + {match.start() + 2}c",
                                         f"1.0 + {match.end()}c")
            else:
                self.text_widget.tag_add('null',
                                         f"1.0 + {match.start() + 2}c",
                                         f"1.0 + {match.end()}c")

    def _mark_error_position(self, error: json.JSONDecodeError):
        """Пометить позицию ошибки в JSON"""
        self._clear_errors()
        if error.pos is not None:
            line = error.lineno
            col = error.colno
            pos = f"{line}.{col - 1}"
            self.text_widget.tag_add('error', pos, f"{pos} + 1c")
            self.text_widget.see(pos)

    def _clear_errors(self):
        """Очистить подсветку ошибок"""
        self.text_widget.tag_remove('error', "1.0", tk.END)

    def set_step_dict(self, step_data: Dict):
        """Установить словарь для редактирования"""
        formatted = json.dumps(step_data, indent=4, ensure_ascii=False)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", formatted)
        self._highlight_syntax()

    def get_step_dict(self) -> Dict:
        """Получить словарь из текстового поля"""
        content = self.text_widget.get("1.0", tk.END)
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            self._mark_error_position(e)
            raise ValueError(f"Invalid JSON: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("JSON Editor Frame")
    root.geometry("800x600")

    # Пример данных
    sample_data = {
        "name": "John Doe",
        "age": 30,
        "is_active": True,
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "coordinates": {
                "lat": 40.7128,
                "lng": -74.0060
            }
        },
        "skills": ["Python", "JavaScript", "SQL"],
        "metadata": None
    }

    # Создание редактора
    editor = StepTextRedactor(root, bg="white", padx=10, pady=10)
    editor.pack(expand=True, fill="both", padx=10, pady=10)

    # Установка данных
    editor.set_step_dict(sample_data)

    # Панель управления
    control_frame = tk.Frame(root)
    control_frame.pack(fill="x", padx=10, pady=(0, 10))


    def print_data():
        try:
            data = editor.get_step_dict()
            print("Current data:", json.dumps(data, indent=2))
        except ValueError as e:
            print("Error:", e)


    tk.Button(control_frame, text="Get Data", command=print_data).pack(side="left", padx=5)
    tk.Button(control_frame, text="Format (Ctrl+S)",
              command=lambda: editor._format_json()).pack(side="left", padx=5)
    tk.Button(control_frame, text="Reformat (Ctrl+R)",
              command=lambda: editor._reformat_json()).pack(side="left", padx=5)

    root.mainloop()