import tkinter as tk
from gui import FinanceApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x550")
    app = FinanceApp(root)
    root.mainloop()
