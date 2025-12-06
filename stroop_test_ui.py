import tkinter as tk
from tkinter import messagebox
from stroop_test_logic import StroopTest


class StroopTestUI:
    def __init__(self, main_window=None):
        self.main_window = main_window

        # Создаем экземпляр теста
        self.test = StroopTest(test_duration=30)

        self.setup_ui()

    def setup_ui(self):
        """Настройка интерфейса"""
        if self.main_window:
            self.main_window.withdraw()

        self.window = tk.Toplevel()
        self.window.title("Тест Струпа")
        self.window.geometry("600x500")
        self.window.configure(bg='lightgray')

        self.create_widgets()

    def create_widgets(self):
        """Создание виджетов интерфейса"""
        # Метка для инструкции
        self.instruction_label = tk.Label(
            self.window,
            text="Выберите ЦВЕТ текста (не значение слова!)",
            font=("Arial", 14, "bold"),
            bg='lightgray'
        )
        self.instruction_label.pack(pady=10)

        # Метка для отображения слова (стимула)
        self.word_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 36, "bold"),
            bg='lightgray',
            height=2
        )
        self.word_label.pack(pady=20)

        # Фрейм для кнопок
        self.buttons_frame = tk.Frame(self.window, bg='lightgray')
        self.buttons_frame.pack(pady=20)

        # Метки для отображения информации
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

        # Создание кнопок выбора цвета
        self.create_color_buttons()

        # Кнопка возврата в меню
        self.menu_button = tk.Button(
            self.window,
            text="В меню",
            font=("Arial", 12),
            width=15,
            height=1,
            command=self.return_to_menu
        )
        self.menu_button.pack(pady=20)

    def create_color_buttons(self):
        """Создание кнопок выбора цвета"""
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
        """Обновление информационных меток"""
        state = self.test.get_test_state()
        self.score_label.config(text=f"Счет: {state['score']}")
        self.timer_label.config(text=f"Время: {state['time_left']} сек")

    def new_stimulus(self):
        """Создание и отображение нового стимула"""
        if not self.test.is_test_active():
            return

        # Генерируем новый стимул
        word, color = self.test.generate_stimulus()

        # Обновляем метку
        self.word_label.config(text=word, fg=color)

        # Запускаем таймер реакции
        self.test.start_stimulus_timing()

        # Обновляем окно
        self.window.update()

    def on_button_click(self, selected_color):
        """Обработка нажатия кнопки выбора цвета"""
        if not self.test.is_test_active():
            return

        # Вычисляем время реакции
        reaction_time = self.test.get_reaction_time()

        # Получаем текущий цвет текста
        current_color = self.word_label.cget("fg")

        # Проверяем ответ через логику теста
        is_correct = self.test.check_answer(selected_color, reaction_time)

        # Визуальная обратная связь
        if is_correct:
            self.word_label.config(bg='lightgreen')
            self.window.after(100, lambda: self.word_label.config(bg='lightgray'))

        # Обновляем информацию
        self.update_info_labels()

        # Создаем новый стимул
        self.new_stimulus()

    def update_timer(self):
        """Обновление таймера"""
        if not self.test.is_test_active():
            return

        # Уменьшаем время через логику теста
        time_ended = self.test.decrease_time()

        # Обновляем метку времени
        self.update_info_labels()

        if time_ended:
            self.end_test()
        else:
            # Продолжаем обновление таймера
            self.window.after(1000, self.update_timer)

    def end_test(self):
        """Завершение теста и показ статистики"""
        # Отключаем кнопки
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

        # Получаем статистику
        stats = self.test.calculate_statistics()

        # Показываем окно статистики
        self.show_statistics(stats)

    def show_statistics(self, stats):
        """Показать окно со статистикой"""
        # Создаем окно статистики
        stats_window = tk.Toplevel(self.window)
        stats_window.title("Результаты теста Струпа")
        stats_window.geometry("450x350")
        stats_window.configure(bg='lightgray')

        # Отображаем статистику
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

        # Кнопка для возврата в меню
        def return_to_menu_from_stats():
            stats_window.destroy()
            self.return_to_menu()

        return_btn = tk.Button(
            stats_window,
            text="В меню",
            font=("Arial", 12),
            width=15,
            height=2,
            command=return_to_menu_from_stats
        )
        return_btn.pack(pady=10)

        # Кнопка для повторного прохождения теста
        retry_btn = tk.Button(
            stats_window,
            text="Пройти еще раз",
            font=("Arial", 12),
            width=15,
            height=2,
            command=lambda: self.retry_test(stats_window)
        )
        retry_btn.pack(pady=5)

    def retry_test(self, stats_window):
        """Перезапуск теста"""
        stats_window.destroy()

        # Сбрасываем тест
        self.test.reset_test()

        # Включаем кнопки
        for btn in self.buttons:
            btn.config(state=tk.NORMAL)

        # Сбрасываем интерфейс
        self.word_label.config(text="", fg="black", bg='lightgray')
        self.update_info_labels()

        # Запускаем тест заново
        self.start_test()

    def return_to_menu(self):
        """Возврат в главное меню"""
        if self.main_window:
            self.main_window.deiconify()
        self.window.destroy()

    def on_closing(self):
        """Обработка закрытия окна"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти? Результаты не будут сохранены."):
            self.return_to_menu()

    def start_test(self):
        """Начало теста"""
        # Создаем первый стимул
        self.new_stimulus()

        # Запускаем таймер
        self.update_timer()

    def start(self):
        """Запуск теста"""
        # Обработка закрытия окна
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Начинаем тест
        self.start_test()

        # Запускаем главный цикл окна
        self.window.mainloop()