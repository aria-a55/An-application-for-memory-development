import random


class MemoryGame:
    def __init__(self, words_list, max_rounds=10, max_errors=3):
        self.WORDS = words_list
        self.max_rounds = max_rounds
        self.max_errors = max_errors
        self.reset_game()

    def reset_game(self):
        self.sequence = []
        self.current_round = 1
        self.score = 0
        self.errors = 0
        self.game_over = False
        # Список уже использованных слов для текущей последовательности
        self.used_words = []
        # отслеживания правильности предыдущего ответа
        self.last_answer_correct = True

    def generate_sequence(self):
        # Если предыдущий ответ был неправильным, показываем ту же последовательность
        if not self.last_answer_correct:
            self.last_answer_correct = True
            return self.sequence.copy()

        # Для первого раунда - одно случайное слово
        if self.current_round == 1:
            word = random.choice(self.WORDS)
            self.sequence = [word]
            self.used_words = [word]
        else:
            # Для последующих раундов сохраняем предыдущую последовательность
            # и добавляем новое слово
            available_words = [w for w in self.WORDS if w not in self.used_words]

            # Если все слова использованы, очищаем список использованных
            if not available_words:
                available_words = self.WORDS.copy()
                self.used_words = []

            new_word = random.choice(available_words)
            self.sequence.append(new_word)
            self.used_words.append(new_word)

        return self.sequence.copy()

    def check_answer(self, user_words):
        user_words_list = [w.strip() for w in user_words.split()]

        if len(user_words_list) != len(self.sequence):
            return False

        # Проверяем каждое слово
        for i, word in enumerate(user_words_list):
            if word.lower() != self.sequence[i].lower():
                return False

        return True

    def process_correct_answer(self):
        # Начисляем очки: 10 за каждое слово в последовательности
        self.score += len(self.sequence) * 10
        self.current_round += 1
        self.last_answer_correct = True

        # Проверяем, не закончилась ли игра по количеству раундов
        if self.current_round > self.max_rounds:
            self.game_over = True

        return True

    def process_wrong_answer(self):
        self.errors += 1
        self.last_answer_correct = False

        if self.errors >= self.max_errors:
            self.game_over = True

        return False

    def is_game_over(self):
        return self.game_over

    def get_game_state(self):
        return {
            'current_round': self.current_round,
            'score': self.score,
            'errors': self.errors,
            'max_rounds': self.max_rounds,
            'max_errors': self.max_errors,
            'sequence': self.sequence.copy(),
            'sequence_length': len(self.sequence)
        }

    def get_display_sequence(self):
        """Возвращает последовательность для отображения пользователю"""
        return " ".join(self.sequence)