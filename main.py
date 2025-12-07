import tkinter as tk
import memory_game
import stroop_test
import sys
import os


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Тренажер - Меню игр")
        self.root.geometry("400x300")

        # Центрирование окна
        self.center_window()

        # Конфигурация отступов
        self.root.configure(padx=20, pady=20)

        # Создание виджетов
        self.create_widgets()

    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="Выберите игру",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Кнопка для игры на запоминание
        memory_button = tk.Button(
            self.root,
            text="Игра на запоминание",
            font=("Arial", 12),
            height=2,
            width=20,
            bg="#9C27B0",
            fg="white",
            command=self.start_memory_game_wrapper
        )
        memory_button.pack(pady=10)

        # Кнопка для теста Струпа
        stroop_button = tk.Button(
            self.root,
            text="Тест Струпа",
            font=("Arial", 12),
            height=2,
            width=20,
            bg="#3F51B5",
            fg="white",
            command=self.start_stroop_test_wrapper
        )
        stroop_button.pack(pady=10)

        # Кнопка возврата в стартовое окно
        back_button = tk.Button(
            self.root,
            text="Назад",
            font=("Arial", 10),
            height=1,
            width=20,
            command=self.return_to_start
        )
        back_button.pack(pady=5)

        # Кнопка выхода
        exit_button = tk.Button(
            self.root,
            text="Выход",
            font=("Arial", 10),
            height=1,
            width=15,
            bg="#f44336",
            fg="white",
            command=self.root.destroy
        )
        exit_button.pack(pady=20)

    def start_memory_game_wrapper(self):
        try:
            memory_game.start_memory_game(self.root)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Ошибка", f"Не удалось запустить игру на запоминание: {e}")

    def start_stroop_test_wrapper(self):
        try:
            stroop_test.start_stroop_test(self.root)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Ошибка", f"Не удалось запустить тест Струпа: {e}")

    def return_to_start(self):
        """Возврат в стартовое окно"""
        self.root.destroy()


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()