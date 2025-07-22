import tkinter as tk
from tkinter import ttk


class TabbedFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        # Создаем Notebook (контейнер для вкладок)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # Создаем несколько фреймов-вкладок
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        # Добавляем вкладки в Notebook
        self.notebook.add(self.tab1, text="Вкладка 1")
        self.notebook.add(self.tab2, text="Вкладка 2")
        self.notebook.add(self.tab3, text="Вкладка 3")

        # Добавляем содержимое на вкладки (для примера)
        self.add_content_to_tab1()
        self.add_content_to_tab2()
        self.add_content_to_tab3()

    def add_content_to_tab1(self):
        """Добавляем виджеты на первую вкладку"""
        label = ttk.Label(self.tab1, text="Это содержимое первой вкладки")
        label.pack(pady=10)

        button = ttk.Button(self.tab1, text="Кнопка 1", command=lambda: print("Нажата кнопка на вкладке 1"))
        button.pack(pady=5)

    def add_content_to_tab2(self):
        """Добавляем виджеты на вторую вкладку"""
        label = ttk.Label(self.tab2, text="Это содержимое второй вкладки")
        label.pack(pady=10)

        entry = ttk.Entry(self.tab2)
        entry.pack(pady=5)
        entry.insert(0, "Введите текст здесь")

    def add_content_to_tab3(self):
        """Добавляем виджеты на третью вкладку"""
        label = ttk.Label(self.tab3, text="Это содержимое третьей вкладки")
        label.pack(pady=10)

        checkbutton = ttk.Checkbutton(self.tab3, text="Выбрать опцию")
        checkbutton.pack(pady=5)


# Пример использования
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Пример фрейма с вкладками")
    root.geometry("400x300")

    app = TabbedFrame(root)

    root.mainloop()