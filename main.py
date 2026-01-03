import tkinter as tk
from gui import FinanceApp

if __name__ == "__main__":
    root = tk.Tk()
    # Установка минимального размера окна
    root.minsize(600, 400)
    app = FinanceApp(root)
    root.mainloop()
