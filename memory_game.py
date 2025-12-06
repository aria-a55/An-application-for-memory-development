from memory_game_ui import MemoryGameUI

def start_memory_game(main_window=None):
    game = MemoryGameUI(main_window)
    game.start()