import tkinter as tk
from tkinter import messagebox, ttk
from models import FinancialOperation
from storage import FileStorage
from utils import validate_amount, validate_date
from analysis import FinanceAnalysis

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый планер 2026")
        self.storage = FileStorage()
        
        # UI Элементы
        tk.Label(root, text="Сумма:").grid(row=0, column=0)
        self.entry_amount = tk.Entry(root)
        self.entry_amount.grid(row=0, column=1)

        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0)
        self.entry_date = tk.Entry(root)
        self.entry_date.grid(row=1, column=1)

        tk.Label(root, text="Категория:").grid(row=2, column=0)
        self.entry_cat = tk.Entry(root)
        self.entry_cat.grid(row=2, column=1)

        self.btn_add = tk.Button(root, text="Добавить расход", command=self.add_data)
        self.btn_add.grid(row=3, column=0, columnspan=2)

        self.btn_plot = tk.Button(root, text="Показать график", command=self.show_chart)
        self.btn_plot.grid(row=4, column=0, columnspan=2)

    def add_data(self):
        amount = self.entry_amount.get()
        date = self.entry_date.get()
        cat = self.entry_cat.get()

        if validate_amount(amount) and validate_date(date):
            try:
                op = FinancialOperation(amount, cat, date, "Комментарий", "expense")
                self.storage.save_operation(op)
                messagebox.showinfo("Успех", "Данные сохранены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
        else:
            messagebox.showwarning("Ошибка ввода", "Проверьте формат суммы и даты!")

    def show_chart(self):
        data = self.storage.load_all()
        analysis = FinanceAnalysis(data)
        analysis.plot_pie_chart()
