import tkinter as tk
from gui import FinanceApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1150x600")
    app = FinanceApp(root)
    root.mainloop()
