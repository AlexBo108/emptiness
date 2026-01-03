import tkinter as tk
from tkinter import ttk, messagebox
from models import FinancialOperation
from storage import FileStorage
from utils import validate_amount, validate_date, sort_treeview_column
from analysis import FinanceAnalysis

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Planner Pro 2026")
        self.storage = FileStorage()

        # Интерфейс ввода
        frame = tk.LabelFrame(root, text="Новая операция", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Сумма:").grid(row=0, column=0)
        self.ent_amount = tk.Entry(frame)
        self.ent_amount.grid(row=0, column=1)

        tk.Label(frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=2)
        self.ent_date = tk.Entry(frame)
        self.ent_date.insert(0, "2026-01-03")
        self.ent_date.grid(row=0, column=3)

        tk.Label(frame, text="Категория:").grid(row=1, column=0)
        self.ent_cat = tk.Entry(frame)
        self.ent_cat.grid(row=1, column=1)

        tk.Button(frame, text="Добавить расход", command=self.add_entry, bg="#e1f5fe").grid(row=1, column=2, columnspan=2, sticky="we")

        # Таблица (Treeview)
        self.tree = ttk.Treeview(root, columns=("ID", "Sum", "Cat", "Date"), show='headings')
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Конфигурация заголовков и привязка сортировки
        for col, head in zip(self.tree["columns"], ["ID", "Сумма", "Категория", "Дата"]):
            self.tree.heading(col, text=head, command=lambda c=col: sort_treeview_column(self.tree, c, False))
            self.tree.column(col, width=100) # Базовая ширина

        # Кнопка анализа
        tk.Button(root, text="📊 Построить график", command=self.show_chart).pack(pady=10)
        self.refresh_table()

    def refresh_table(self):
        """Обновление данных в таблице."""
        self.tree.delete(*self.tree.get_children())
        for row in self.storage.load_all():
            self.tree.insert("", tk.END, values=(row['id'], row['amount'], row['category'], row['date']))

    def add_entry(self):
        """Обработка добавления новой записи."""
        try:
            amt, dt, cat = self.ent_amount.get(), self.ent_date.get(), self.ent_cat.get()
            if not validate_amount(amt) or not validate_date(dt) or not cat:
                raise ValueError("Некорректные данные. Проверьте сумму, категорию и формат даты.")
            
            op = FinancialOperation(amt, cat, dt, "Auto", "expense")
            if self.storage.save_operation(op):
                self.refresh_table()
                self.ent_amount.delete(0, tk.END)
            else:
                raise IOError("Ошибка доступа к файлу")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def show_chart(self):
        """Отображение графика."""
        try:
            data = self.storage.load_all()
            ana = FinanceAnalysis(data)
            ana.plot_expenses()
        except Exception as e:
            messagebox.showwarning("Анализ", f"Не удалось создать график: {e}")
