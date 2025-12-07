import tkinter as tk
import memory_game
import stroop_test

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Тренажер - Меню игр")
        self.root.geometry("400x350")

        self.center_window()
        self.root.configure(padx=20, pady=20)
        self.create_widgets()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="Выберите игру",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

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

        help_button = tk.Button(
            self.root,
            text="Как играть?",
            font=("Arial", 12),
            height=2,
            width=20,
            bg="#FF9800",
            fg="white",
            command=self.show_instructions
        )
        help_button.pack(pady=10)

        back_button = tk.Button(
            self.root,
            text="Назад",
            font=("Arial", 10),
            height=1,
            width=20,
            command=self.return_to_start
        )
        back_button.pack(pady=5)

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
        memory_game.start_memory_game(self.root)

    def start_stroop_test_wrapper(self):
        stroop_test.start_stroop_test(self.root)

    def return_to_start(self):
        self.root.destroy()

    def show_instructions(self):
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Инструкция")
        instructions_window.geometry("500x400")
        instructions_window.configure(padx=20, pady=20)

        # Центрирование окна инструкций
        instructions_window.update_idletasks()
        width = instructions_window.winfo_width()
        height = instructions_window.winfo_height()
        x = (instructions_window.winfo_screenwidth() // 2) - (width // 2)
        y = (instructions_window.winfo_screenheight() // 2) - (height // 2)
        instructions_window.geometry(f'{width}x{height}+{x}+{y}')

        text_widget = tk.Text(instructions_window, wrap=tk.WORD, font=("Arial", 10))
        text_widget.pack(fill=tk.BOTH, expand=True)

        instructions = """
        ИГРА НА ЗАПОМИНАНИЕ:
        1. На экране появится последовательность слов
        2. Запомните порядок
        3. После сигнала повторите последовательность
        4. С каждым уровнем длина последовательности увеличивается

        ТЕСТ СТРУПА:
        1. На экране появляются слова, обозначающие цвета
        2. Слово может быть написано в цвете, который не совпадает с его значением
        3. Вам нужно выбрать ЦВЕТ ТЕКСТА, а не прочитать слово
        4. Нажмите на кнопку с соответствующим цветом

        Управление:
        - Используйте мышь для нажатия кнопок
        - Внимательно читайте задания
        - Старайтесь отвечать быстро и точно
        """

        text_widget.insert(tk.END, instructions)
        text_widget.configure(state=tk.DISABLED)

        close_button = tk.Button(
            instructions_window,
            text="Закрыть",
            font=("Arial", 10),
            command=instructions_window.destroy
        )
        close_button.pack(pady=10)


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()