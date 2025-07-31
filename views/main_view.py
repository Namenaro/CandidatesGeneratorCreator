
import tkinter as tk
from tkinter import ttk, scrolledtext

from views.multitrack_editor_view import MultitrackEditorView
from views.multitrack_result_view import MultitrackResultView
from views.track_view import TrackView



class MainView(tk.Frame):
    def __init__(self, get_steps_types_names, get_step_dict_by_type_name, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.get_steps_types_names = get_steps_types_names
        self.get_step_dict_by_type_name = get_step_dict_by_type_name

        self.create_menu()
        self.create_widgets()

    def create_widgets(self):
        # Создаем PanedWindow с начальным соотношением ширины 40:60
        self.paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=5)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Создаем панели для левой и правой частей
        left_panel = tk.Frame(self.paned)
        right_panel = tk.Frame(self.paned)

        # Добавляем панели в PanedWindow с начальным соотношением ширины
        self.paned.add(left_panel, minsize=300, width=int(self.winfo_screenwidth() * 0.3))  # 30% ширины экрана
        self.paned.add(right_panel, minsize=300)  # Оставшиеся 60%

        # Настраиваем левую панель
        self.setup_left_panel(left_panel)

        # Настраиваем правую панель
        self.setup_right_panel(right_panel)

    def setup_left_panel(self, panel):
        panel.grid_rowconfigure(2, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        # Текстовое поле для информации о мультитреке
        self.text_multitrack_info = scrolledtext.ScrolledText(
            panel,
            wrap=tk.WORD,
            width=40,  # Увеличиваем ширину
            height=4,  # Увеличиваем высоту
            font=('Arial', 10)
        )
        self.text_multitrack_info.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        self.text_multitrack_info.insert(tk.END, "Информация о мультитреке:")

        # Текстовое поле для информации о примере
        self.text_example_info = scrolledtext.ScrolledText(
            panel,
            wrap=tk.WORD,
            width=40,  # Увеличиваем ширину
            height=4,  # Увеличиваем высоту
            font=('Arial', 10)
        )
        self.text_example_info.grid(row=1, column=0, sticky="nsew", pady=(0, 5))
        self.text_example_info.insert(tk.END, "Информация о примере:")

        # MultitrackEditorView
        self.multitrack_editor = MultitrackEditorView(panel, get_steps_types_names= self.get_steps_types_names, get_step_dict_by_type_name=self.get_step_dict_by_type_name)
        self.multitrack_editor.grid(row=2, column=0, sticky="nsew")

        # Кнопка "Сохранить и запустить"
        self.save_button = ttk.Button(
            panel,
            text="Сохранить и запустить",
            style="Green.TButton",
            command=self.on_save_and_run
        )
        self.save_button.grid(row=3, column=0, sticky="ew", pady=(5, 0))

    def setup_right_panel(self, panel):
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        # TrackView
        self.track_view = TrackView(panel)
        self.track_view.grid(row=0, column=0, sticky="nsew")

        # MultitrackResultView
        self.multitrack_result = MultitrackResultView(panel)
        self.multitrack_result.grid(row=1, column=0, sticky="nsew")

        # Кнопка "Следующий образец"
        self.next_button = ttk.Button(
            panel,
            text="Следующий образец",
            style="Blue.TButton",
            command=self.on_next_sample
        )
        self.next_button.grid(row=2, column=0, sticky="ew", pady=(5, 0))

        # Стили для кнопок
        style = ttk.Style()
        style.configure("Green.TButton", background="green", foreground="white")
        style.configure("Blue.TButton", background="blue", foreground="white")

    def create_menu(self):
        # Создаем главное меню
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Добавляем пункты меню
        file_menu.add_command(
            label="Запустить тест мультитрека",
            command=self.on_run_test
        )
        file_menu.add_command(
            label="Документация",
            command=self.on_show_docs
        )


    def on_run_test(self):
        """Обработчик запуска теста мультитрека"""
        print("Запуск теста мультитрека...")
        # Здесь будет логика запуска теста

    def on_show_docs(self):
        """Обработчик показа документации в новом окне"""
        doc_window = tk.Toplevel(self.master)
        doc_window.title("Документация")
        doc_window.geometry("800x600")

        # Создаем текстовое поле с прокруткой
        text_area = scrolledtext.ScrolledText(
            doc_window,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        text_area.pack(fill=tk.BOTH, expand=True)

        try:
            # Пытаемся загрузить текст из файла
            with open('documentation.txt', 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = "Файл документации не найден\nСоздайте файл documentation.txt в корне проекта"
        except Exception as e:
            content = f"Ошибка загрузки документации: {str(e)}"

        # Вставляем текст и делаем поле доступным только для чтения
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)

        # Кнопка закрытия
        close_btn = ttk.Button(
            doc_window,
            text="Закрыть",
            command=doc_window.destroy
        )
        close_btn.pack(pady=10)

    def reset_multitrack_info(self, info: str):
        """Очищает и устанавливает новый текст в поле информации о мультитреке"""
        self.text_multitrack_info.config(state=tk.NORMAL)
        self.text_multitrack_info.delete(1.0, tk.END)
        self.text_multitrack_info.insert(tk.END, info)
        self.text_multitrack_info.config(state=tk.DISABLED)

    def reset_example_info(self, info: str):
        """Очищает и устанавливает новый текст в поле информации о примере"""
        self.text_example_info.config(state=tk.NORMAL)
        self.text_example_info.delete(1.0, tk.END)
        self.text_example_info.insert(tk.END, info)
        self.text_example_info.config(state=tk.DISABLED)

    def on_save_and_run(self):
        print("Кнопка 'Сохранить и запустить' нажата")

    def on_next_sample(self):
        print("Кнопка 'Следующий образец' нажата")



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
    root.title("Анализ мультитреков")

    # Устанавливаем окно в максимальный размер
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width - 100}x{screen_height - 100}+0+0")
    root.state('zoomed')

    main_view = MainView(master=root, get_steps_types_names=demo_get_steps_types_names, get_step_dict_by_type_name=demo_get_step_dict_by_type_name)
    main_view.pack(fill="both", expand=True)

    root.mainloop()