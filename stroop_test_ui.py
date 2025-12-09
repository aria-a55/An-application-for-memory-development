import tkinter as tk
from tkinter import messagebox
from stroop_test_logic import StroopTest

class StroopTestUI:
    def __init__(self, main_window=None):
        self.main_window = main_window

        self.test = StroopTest(test_duration=30)
        self.setup_ui()

    def setup_ui(self):
        if self.main_window:
            self.main_window.withdraw()

        self.window = tk.Toplevel()
        self.window.title("Тест Струпа")
        self.window.geometry("600x500")
        self.window.configure(bg='lightgray')

        self.create_widgets()

    def create_widgets(self):
        control_frame = tk.Frame(self.window, bg='lightgray')
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        self.menu_button = tk.Button(
            control_frame,
            text="В меню",
            font=("Arial", 10),
            width=10,
            height=1,
            command=self.return_to_menu
        )
        self.menu_button.pack(side=tk.LEFT, padx=5)

        self.instruction_label = tk.Label(
            self.window,
            text="Выберите ЦВЕТ текста (не значение слова!)",
            font=("Arial", 14, "bold"),
            bg='lightgray'
        )
        self.instruction_label.pack(pady=10)
        self.word_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 36, "bold"),
            bg='lightgray',
            height=2
        )
        self.word_label.pack(pady=20)

        self.buttons_frame = tk.Frame(self.window, bg='lightgray')
        self.buttons_frame.pack(pady=20)

        info_frame = tk.Frame(self.window, bg='lightgray')
        info_frame.pack(pady=10)

        self.score_label = tk.Label(
            info_frame,
            text=f"Счет: 0",
            font=("Arial", 12),
            bg='lightgray'
        )
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.timer_label = tk.Label(
            info_frame,
            text=f"Время: 30 сек",
            font=("Arial", 12),
            bg='lightgray'
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)

        self.create_color_buttons()

    def create_color_buttons(self):
        self.buttons = []

        for i, color_name in enumerate(self.test.colors_names):
            btn = tk.Button(
                self.buttons_frame,
                text=color_name,
                font=("Arial", 12),
                width=12,
                height=2,
                fg="black",
                command=lambda c=self.test.colors_hex[i]: self.on_button_click(c)
            )
            btn.grid(row=0, column=i, padx=5)
            self.buttons.append(btn)

    def update_info_labels(self):
        state = self.test.get_test_state()
        self.score_label.config(text=f"Счет: {state['score']}")
        self.timer_label.config(text=f"Время: {state['time_left']} сек")

    def new_stimulus(self):
        if not self.test.is_test_active():
            return

        word, color = self.test.generate_stimulus()

        self.word_label.config(text=word, fg=color)
        self.test.start_stimulus_timing()
        self.window.update()

    def on_button_click(self, selected_color):
        if not self.test.is_test_active():
            return

        reaction_time = self.test.get_reaction_time()
        current_color = self.word_label.cget("fg")
        is_correct = self.test.check_answer(selected_color, reaction_time)

        if is_correct:
            self.word_label.config(bg='lightgreen')
            self.window.after(100, lambda: self.word_label.config(bg='lightgray'))

        self.update_info_labels()

        self.new_stimulus()

    def update_timer(self):
        if not self.test.is_test_active():
            return

        time_ended = self.test.decrease_time()

        self.update_info_labels()

        if time_ended:
            self.end_test()
        else:
            self.window.after(1000, self.update_timer)

    def end_test(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

        stats = self.test.calculate_statistics()

        self.show_statistics(stats)

    def show_statistics(self, stats):
        stats_window = tk.Toplevel(self.window)
        stats_window.title("Результаты теста Струпа")
        stats_window.geometry("450x350")
        stats_window.configure(bg='lightgray')

        if stats['total_trials'] > 0:
            stats_text = f"""
            ТЕСТ ЗАВЕРШЕН!

            Общее количество попыток: {stats['total_trials']}
            Правильных ответов: {stats['correct_trials']}
            Неправильных ответов: {stats['incorrect_trials']}
            Точность: {stats['accuracy']:.1f}%
            Среднее время реакции: {stats['avg_reaction_time']:.3f} сек
            Итоговый счет: {stats['score']}

            Нажмите "В меню" для выхода.
            """
        else:
            stats_text = "Не было зарегистрировано ни одной попытки!"

        stats_label = tk.Label(
            stats_window,
            text=stats_text,
            font=("Arial", 12),
            bg='lightgray',
            justify=tk.LEFT
        )
        stats_label.pack(pady=20, padx=20)

        def return_to_menu_from_stats():
            stats_window.destroy()
            self.return_to_menu()

        button_frame = tk.Frame(stats_window, bg='lightgray')
        button_frame.pack(pady=10)

        return_btn = tk.Button(
            button_frame,
            text="В меню",
            font=("Arial", 12),
            width=15,
            height=2,
            command=return_to_menu_from_stats
        )
        return_btn.pack(side=tk.LEFT, padx=5)

        retry_btn = tk.Button(
            button_frame,
            text="Пройти еще раз",
            font=("Arial", 12),
            width=15,
            height=2,
            command=lambda: self.retry_test(stats_window)
        )
        retry_btn.pack(side=tk.LEFT, padx=5)

    def retry_test(self, stats_window):
        stats_window.destroy()

        self.test.reset_test()

        for btn in self.buttons:
            btn.config(state=tk.NORMAL)

        self.word_label.config(text="", fg="black", bg='lightgray')
        self.update_info_labels()

        self.start_test()

    def return_to_menu(self):
        if self.main_window:
            self.main_window.deiconify()
        self.window.destroy()

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти? Результаты не будут сохранены."):
            self.return_to_menu()

    def start_test(self):
        self.new_stimulus()
        self.update_timer()

    def start(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.start_test()
        self.window.mainloop()