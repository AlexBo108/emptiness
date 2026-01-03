import tkinter as tk
from tkinter import ttk, messagebox
from models import FinancialOperation
from storage import FileStorage
from utils import validate_amount, validate_date, sort_treeview_column
from analysis import FinanceAnalysis

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый менеджер 2026")
        self.storage = FileStorage()
        
        # Стили для превышения бюджета
        self.style = ttk.Style()
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview", rowheight=25)
        
        # --- Блок ввода Операций ---
        input_frame = tk.LabelFrame(root, text="Новая запись", padx=10, pady=5)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Сумма:").grid(row=0, column=0)
        self.ent_amt = tk.Entry(input_frame, width=10)
        self.ent_amt.grid(row=0, column=1)

        tk.Label(input_frame, text="Категория:").grid(row=0, column=2)
        self.ent_cat = tk.Entry(input_frame, width=15)
        self.ent_cat.grid(row=0, column=3)

        tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4)
        self.ent_date = tk.Entry(input_frame, width=12)
        self.ent_date.insert(0, "2026-01-03")
        self.ent_date.grid(row=0, column=5, padx=5)

        tk.Button(input_frame, text="Добавить", command=self.add_entry, bg="#e3f2fd").grid(row=0, column=6, padx=5)

        # --- Блок Бюджета и Фильтра ---
        control_frame = tk.Frame(root, padx=10, pady=5)
        control_frame.pack(fill="x")

        tk.Label(control_frame, text="Плановый бюджет:").pack(side=tk.LEFT)
        self.ent_budget = tk.Entry(control_frame, width=10)
        self.ent_budget.insert(0, "50000")
        self.ent_budget.pack(side=tk.LEFT, padx=5)
        self.ent_budget.bind("<KeyRelease>", lambda e: self.refresh_table())

        tk.Label(control_frame, text="Фильтр:").pack(side=tk.LEFT, padx=(20, 0))
        self.filter_var = tk.StringVar(value="Все")
        self.filter_combo = ttk.Combobox(control_frame, textvariable=self.filter_var, state="readonly", width=15)
        self.filter_combo.pack(side=tk.LEFT, padx=5)
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("ID", "Sum", "Cat", "Date"), show='headings')
        for col, head in zip(self.tree["columns"], ["ID", "Сумма", "Категория", "Дата"]):
            self.tree.heading(col, text=head, command=lambda c=col: sort_treeview_column(self.tree, c, False))
            self.tree.column(col, anchor="center")
        
        # Настройка тега для красного цвета
        self.tree.tag_configure('over_budget', background='#ffcdd2')
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Подвал с итогами ---
        footer = tk.Frame(root, padx=10, pady=10)
        footer.pack(fill="x")

        self.lbl_total = tk.Label(footer, text="Потрачено: 0", font=("Arial", 10))
        self.lbl_total.pack(side=tk.LEFT)

        self.lbl_remain = tk.Label(footer, text="Остаток: 0", font=("Arial", 11, "bold"), padx=20)
        self.lbl_remain.pack(side=tk.LEFT)

        tk.Button(footer, text="📊 График", command=self.show_chart).pack(side=tk.RIGHT)

        self.refresh_table()

    def refresh_table(self):
        data = self.storage.load_all()
        # Обновление категорий в комбобоксе
        cats = sorted(list(set(r['category'] for r in data)))
        self.filter_combo['values'] = ["Все"] + cats

        # Расчет бюджета
        try:
            budget_val = float(self.ent_budget.get()) if self.ent_budget.get() else 0.0
        except ValueError:
            budget_val = 0.0

        analysis = FinanceAnalysis(data)
        rows, total, remain = analysis.get_summary(self.filter_var.get(), budget_val)

        self.tree.delete(*self.tree.get_children())
        
        # Определяем, есть ли превышение общего лимита
        is_over = remain < 0

        for r in rows:
            # Если общий остаток отрицательный, красим все отфильтрованные строки
            tag = 'over_budget' if is_over else ''
            self.tree.insert("", tk.END, values=(r['id'], f"{r['amount']:.2f}", r['category'], r['date']), tags=(tag,))

        # Обновление текста
        self.lbl_total.config(text=f"Потрачено: {total:.2f}")
        self.lbl_remain.config(text=f"Остаток: {remain:.2f}", fg="red" if is_over else "green")

    def add_entry(self):
        amt, dt, cat = self.ent_amt.get(), self.ent_date.get(), self.ent_cat.get()
        if validate_amount(amt) and validate_date(dt) and cat:
            if self.storage.save_operation(FinancialOperation(amt, cat, dt, "auto")):
                self.refresh_table()
                self.ent_amt.delete(0, tk.END)
            else: messagebox.showerror("Ошибка", "Ошибка записи")
        else: messagebox.showwarning("Ввод", "Неверные данные (ГГГГ-ММ-ДД)")

    def show_chart(self):
        try:
            FinanceAnalysis(self.storage.load_all()).plot_pie()
        except Exception as e: messagebox.showerror("Ошибка", str(e))
