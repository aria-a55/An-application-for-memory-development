import tkinter as tk
from memory_game_logic import MemoryGame


class MemoryGameUI:
    def __init__(self, main_window=None):
        self.main_window = main_window

        words_list = [
            "Солнце", "Стол", "Река", "Гора", "Лес", "Книга", "Часы", "Окно",
            "Дверь", "Стул", "Дом", "Цветок", "Море", "Небо", "Звезда", "Луна",
            "Птица", "Рыба", "Кот", "Собака", "Яблоко", "Хлеб", "Вода", "Огонь",
            "Земля", "Воздух", "Путь", "Город", "Улица", "Машина"
        ]
        self.game = MemoryGame(words_list)

        self.setup_ui()

    def setup_ui(self):
        if self.main_window:
            self.main_window.withdraw()

        self.game_window = tk.Toplevel()
        self.game_window.title("Игра на запоминание")
        self.game_window.geometry("700x600")
        self.game_window.configure(padx=20, pady=20)

        self.create_widgets()

    def create_widgets(self):
        control_frame = tk.Frame(self.game_window)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        self.menu_button = tk.Button(
            control_frame,
            text="В меню",
            font=("Arial", 10),
            height=1,
            width=10,
            command=self.return_to_menu
        )
        self.menu_button.pack(side=tk.LEFT, padx=5)

        self.restart_button = tk.Button(
            control_frame,
            text="Заново",
            font=("Arial", 10),
            height=1,
            width=10,
            command=self.restart_game,
            state=tk.DISABLED
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)

        self.info_label = tk.Label(
            self.game_window,
            text="",
            font=("Arial", 14, "bold")
        )
        self.info_label.pack(pady=(0, 20))

        self.word_label = tk.Label(
            self.game_window,
            text="Готовьтесь...",
            font=("Arial", 24, "bold"),
            height=5,
            width=30,
            relief="ridge",
            bg="lightblue"
        )
        self.word_label.pack(pady=20)

        self.instruction_label = tk.Label(
            self.game_window,
            text="Запомните слова, которые появятся на экране",
            font=("Arial", 12)
        )
        self.instruction_label.pack()

        input_frame = tk.Frame(self.game_window)
        input_frame.pack(pady=20)

        tk.Label(
            input_frame,
            text="Введите слова через пробел:",
            font=("Arial", 12)
        ).pack()

        self.user_input = tk.Entry(
            input_frame,
            font=("Arial", 14),
            width=40
        )
        self.user_input.pack(pady=5)
        self.user_input.config(state="disabled")

        self.check_button = tk.Button(
            self.game_window,
            text="Проверить",
            font=("Arial", 12),
            height=1,
            width=15,
            state="disabled",
            command=self.check_answer
        )
        self.check_button.pack(pady=10)

    def update_info_label(self):
        state = self.game.get_game_state()
        self.info_label.config(
            text=f"Раунд: {state['current_round']} | Счет: {state['score']} | Ошибки: {state['errors']}/{state['max_errors']}"
        )

    def show_word(self, index):
        if index < len(self.game.sequence):
            self.word_label.config(text=self.game.sequence[index])
            self.game_window.after(2000, self.show_word, index + 1)
        else:
            self.word_label.config(text="Ваша очередь!")
            self.instruction_label.config(text="Введите все слова в правильном порядке через пробел")
            self.user_input.config(state="normal")
            self.check_button.config(state="normal")
            self.user_input.focus()

    def start_round(self):
        self.user_input.delete(0, tk.END)
        self.user_input.config(state="disabled")
        self.check_button.config(state="disabled")

        self.game.generate_sequence()

        self.update_info_label()

        state = self.game.get_game_state()
        self.word_label.config(text=f"Запомните {state['current_round']} слово(в)")
        self.instruction_label.config(text="Сейчас появятся слова...")

        self.game_window.after(2000, self.show_word, 0)

    def check_answer(self):
        answer = self.user_input.get().strip()

        if not answer:
            return

        if self.game.check_answer(answer):
            self.game.process_correct_answer()
            self.word_label.config(text="Правильно! ✓", bg="lightgreen")
        else:
            self.game.process_wrong_answer()
            self.word_label.config(text="Неправильно! ✗", bg="lightcoral")

            correct_text = "Правильно: " + " ".join(self.game.sequence)
            self.instruction_label.config(text=correct_text)

        self.update_info_label()

        if self.game.is_game_over():
            self.end_game()
        else:
            self.game_window.after(3000, self.start_round)

    def end_game(self):
        self.user_input.config(state="disabled")
        self.check_button.config(state="disabled")
        self.restart_button.config(state=tk.NORMAL)

        state = self.game.get_game_state()
        self.word_label.config(
            text=f"Игра окончена!\nСчет: {state['score']}",
            bg="lightyellow",
            font=("Arial", 20, "bold")
        )

        if state['errors'] >= state['max_errors']:
            result_text = f"Слишком много ошибок ({state['errors']})"
        else:
            result_text = f"Достигнут максимум раундов ({state['max_rounds']})"

        self.instruction_label.config(
            text=f"{result_text}\nПравильных ответов: {state['current_round'] - 1}",
            font=("Arial", 12)
        )

    def restart_game(self):
        self.game.reset_game()
        self.user_input.delete(0, tk.END)
        self.user_input.config(state="disabled")
        self.check_button.config(state="disabled")
        self.restart_button.config(state=tk.DISABLED)

        self.word_label.config(
            text="Готовьтесь...",
            bg="lightblue",
            font=("Arial", 24, "bold")
        )
        self.instruction_label.config(text="Запомните слова, которые появятся на экране")

        self.update_info_label()
        self.game_window.after(1000, self.start_round)

    def return_to_menu(self):
        if self.main_window:
            self.main_window.deiconify()
        self.game_window.destroy()

    def on_closing(self):
        self.return_to_menu()

    def start(self):
        self.game_window.after(1000, self.start_round)
        self.game_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.game_window.mainloop()