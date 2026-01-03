from gui import FinanceApp
import tkinter as tk

def main():
    """Точка входа в приложение."""
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
