import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class StartWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Тренажер")
        self.root.geometry("400x300")
        self.center_window()
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
            text="Добро пожаловать в Тренажер!",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=30)

        menu_button = tk.Button(
            self.root,
            text="Перейти в меню игр",
            command=self.open_main_menu,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10)
        )
        menu_button.pack(pady=10)

        # Кнопка информации
        info_button = (tk.Button
            (self.root,
            text="О программе",
            command=self.show_info,
            width=20,
            height=2,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10)
        ))
        info_button.pack(pady=10)

        # Кнопка выхода
        exit_button = tk.Button(
            self.root,
            text="Выход",
            command=self.exit_app,
            width=20,
            height=2,
            bg="#f44336",
            fg="white",
            font=("Arial", 10)
        )
        exit_button.pack(pady=10)

    def open_main_menu(self):
        self.root.withdraw()
        main_file = os.path.join(os.path.dirname(__file__), "main.py")
        self.process = subprocess.Popen([sys.executable, main_file])

        self.process.wait()

        self.root.deiconify()
        self.root.deiconify()

    def show_info(self):
        info_text = """Тренажер для развития когнитивных способностей
Доступные игры:
1. Игра на запоминание - развивает память
2. Тест Струпа - тренирует внимание и реакцию"""

        messagebox.showinfo("О программе", info_text)

    def exit_app(self):
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = StartWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()