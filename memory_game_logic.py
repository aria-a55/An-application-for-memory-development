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

    def generate_sequence(self):
        self.sequence = []
        for _ in range(self.current_round):
            word = random.choice(self.WORDS)
            while self.sequence and word == self.sequence[-1]:
                word = random.choice(self.WORDS)
            self.sequence.append(word)
        return self.sequence

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
        self.score += self.current_round * 10
        self.current_round += 1

        # Проверяем, не закончилась ли игра по количеству раундов
        if self.current_round > self.max_rounds:
            self.game_over = True

        return True

    def process_wrong_answer(self):
        self.errors += 1

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
            'sequence': self.sequence.copy()
        }