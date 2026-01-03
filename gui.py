import tkinter as tk
from tkinter import ttk, messagebox
from models import FinancialOperation
from storage import FileStorage
from utils import validate_amount, validate_date, sort_treeview_column
from analysis import FinanceAnalysis

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый планер 2026")
        self.storage = FileStorage()

        # --- Блок ввода ---
        header = tk.LabelFrame(root, text="Добавить операцию", padx=10, pady=10)
        header.pack(fill="x", padx=10, pady=5)

        tk.Label(header, text="Сумма:").grid(row=0, column=0)
        self.ent_amt = tk.Entry(header)
        self.ent_amt.grid(row=0, column=1)

        tk.Label(header, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=2)
        self.ent_date = tk.Entry(header)
        self.ent_date.insert(0, "2026-01-03")
        self.ent_date.grid(row=0, column=3)

        tk.Label(header, text="Категория:").grid(row=1, column=0)
        self.ent_cat = tk.Entry(header)
        self.ent_cat.grid(row=1, column=1)

        tk.Button(header, text="Сохранить", command=self.add_entry, bg="#d4edda").grid(row=1, column=2, columnspan=2, sticky="we", padx=5)

        # --- Блок фильтрации ---
        filter_frame = tk.Frame(root, padx=10)
        filter_frame.pack(fill="x")

        tk.Label(filter_frame, text="Фильтр по категории:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="Все")
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, state="readonly")
        self.filter_combo.pack(side=tk.LEFT, padx=5)
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("ID", "Sum", "Cat", "Date"), show='headings')
        for col, head in zip(self.tree["columns"], ["ID", "Сумма", "Категория", "Дата"]):
            self.tree.heading(col, text=head, command=lambda c=col: sort_treeview_column(self.tree, c, False))
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Итоговая сумма и графики ---
        footer = tk.Frame(root, padx=10, pady=10)
        footer.pack(fill="x")

        self.lbl_total = tk.Label(footer, text="Итого: 0.00", font=("Arial", 12, "bold"))
        self.lbl_total.pack(side=tk.LEFT)

        tk.Button(footer, text="📊 Построить график", command=self.show_chart).pack(side=tk.RIGHT)
        
        self.refresh_table()

    def update_categories(self, data):
        """Обновляет список категорий в фильтре."""
        categories = sorted(list(set(row['category'] for row in data)))
        self.filter_combo['values'] = ["Все"] + categories

    def refresh_table(self):
        """Обновление таблицы с учетом фильтра."""
        all_data = self.storage.load_all()
        self.update_categories(all_data)
        
        analysis = FinanceAnalysis(all_data)
        filtered_rows, total = analysis.get_filtered_data(self.filter_var.get())
        
        self.tree.delete(*self.tree.get_children())
        for row in filtered_rows:
            self.tree.insert("", tk.END, values=(row['id'], f"{row['amount']:.2f}", row['category'], row['date']))
        
        self.lbl_total.config(text=f"Итого: {total:.2f}")

    def add_entry(self):
        amt, dt, cat = self.ent_amt.get(), self.ent_date.get(), self.ent_cat.get()
        if validate_amount(amt) and validate_date(dt) and cat.strip():
            op = FinancialOperation(amt, cat, dt, "comment")
            if self.storage.save_operation(op):
                self.refresh_table()
                self.ent_amt.delete(0, tk.END)
            else: messagebox.showerror("Ошибка", "Не удалось сохранить файл")
        else: messagebox.showwarning("Ввод", "Проверьте сумму, категорию и формат даты (YYYY-MM-DD)")

    def show_chart(self):
        try:
            FinanceAnalysis(self.storage.load_all()).plot_expenses()
        except Exception as e: messagebox.showinfo("Инфо", str(e))
