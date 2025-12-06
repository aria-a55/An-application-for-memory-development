import tkinter as tk
import memory_game
import stroop_test

def start_memory_game_wrapper():
    memory_game.start_memory_game(root)

def start_stroop_test_wrapper():
    stroop_test.start_stroop_test(root)

# Создание главного окна
root = tk.Tk()
root.title("Тренажер")

# Настройка геометрии окна
root.geometry("400x300")
root.configure(padx=20, pady=20)

# Заголовок
title_label = tk.Label(
    root,
    text="Выберите игру",
    font=("Arial", 16, "bold")
)
title_label.pack(pady=(0, 20))

# Кнопка для игры на запоминание
memory_button = tk.Button(
    root,
    text="Игра на запоминание",
    font=("Arial", 12),
    height=2,
    width=20,
    command=start_memory_game_wrapper
)
memory_button.pack(pady=10)

# Кнопка для теста Струпа
stroop_button = tk.Button(
    root,
    text="Тест Струпа",
    font=("Arial", 12),
    height=2,
    width=20,
    command=start_stroop_test_wrapper
)
stroop_button.pack(pady=10)

# Кнопка выхода
exit_button = tk.Button(
    root,
    text="Выход",
    font=("Arial", 12),
    height=1,
    width=15,
    command=root.destroy
)
exit_button.pack(pady=20)

# Запуск основного цикла
root.mainloop()