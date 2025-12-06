import random
import time


class StroopTest:
    def __init__(self, test_duration=30):
        self.colors_names = ["Красный", "Синий", "Зеленый", "Желтый"]
        self.colors_hex = ["red", "blue", "green", "yellow"]

        self.test_duration = test_duration
        self.reset_test()

    def reset_test(self):
        """Сброс состояния теста"""
        self.score = 0
        self.time_left = self.test_duration
        self.results = []  # Каждый элемент: (реакция_верная, время_реакции)
        self.current_stimulus_start = 0
        self.test_active = True
        self.current_word = ""
        self.current_color = ""

    def generate_stimulus(self):
        """Создание нового стимула (несовпадающие слово и цвет)"""
        # Выбираем случайное слово
        word = random.choice(self.colors_names)

        # Выбираем случайный цвет, который НЕ совпадает со значением слова
        word_index = self.colors_names.index(word)
        available_colors = [
            color for i, color in enumerate(self.colors_hex)
            if i != word_index
        ]
        color = random.choice(available_colors)

        self.current_word = word
        self.current_color = color

        return word, color

    def check_answer(self, selected_color, reaction_time):
        """Проверка ответа пользователя"""
        # Проверяем ответ
        is_correct = (selected_color == self.current_color)

        # Сохраняем результат
        self.results.append((is_correct, reaction_time))

        # Обновляем счет
        if is_correct:
            self.score += 1

        return is_correct

    def decrease_time(self):
        """Уменьшение оставшегося времени"""
        if self.time_left > 0:
            self.time_left -= 1
            return False
        else:
            self.test_active = False
            return True

    def calculate_statistics(self):
        """Вычисление статистики теста"""
        if not self.results:
            return {
                'total_trials': 0,
                'correct_trials': 0,
                'incorrect_trials': 0,
                'accuracy': 0,
                'avg_reaction_time': 0,
                'score': self.score
            }

        correct_trials = [r for r in self.results if r[0]]
        incorrect_trials = [r for r in self.results if not r[0]]

        total_trials = len(self.results)
        accuracy = len(correct_trials) / total_trials * 100 if total_trials > 0 else 0

        avg_reaction_time = sum(r[1] for r in correct_trials) / len(correct_trials) if correct_trials else 0

        return {
            'total_trials': total_trials,
            'correct_trials': len(correct_trials),
            'incorrect_trials': len(incorrect_trials),
            'accuracy': accuracy,
            'avg_reaction_time': avg_reaction_time,
            'score': self.score
        }

    def is_test_active(self):
        """Проверка, активен ли тест"""
        return self.test_active

    def get_test_state(self):
        """Возвращает текущее состояние теста"""
        return {
            'score': self.score,
            'time_left': self.time_left,
            'test_active': self.test_active,
            'current_word': self.current_word,
            'current_color': self.current_color
        }

    def start_stimulus_timing(self):
        """Начать отсчет времени реакции для текущего стимула"""
        self.current_stimulus_start = time.time()

    def get_reaction_time(self):
        """Получить время реакции для текущего стимула"""
        return time.time() - self.current_stimulus_start