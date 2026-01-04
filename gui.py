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
        self.editing_id = None
        self.style = ttk.Style()
        self.style.configure("Treeview.overbudget", background='#ffcdd2')

        # --- Блок ввода ---
        input_fr = tk.LabelFrame(root, text="Управление операциями", padx=10, pady=10)
        input_fr.pack(fill="x", padx=10, pady=5)
        tk.Label(input_fr, text="Сумма").grid(row=0, column=0, sticky="w")
        self.ent_amt = tk.Entry(input_fr, width=15); self.ent_amt.grid(row=1, column=0, padx=5)
        tk.Label(input_fr, text="Категория").grid(row=0, column=1, sticky="w")
        self.ent_cat = tk.Entry(input_fr, width=20); self.ent_cat.grid(row=1, column=1, padx=5)
        tk.Label(input_fr, text="Дата (ГГГГ-ММ-ДД)").grid(row=0, column=2, sticky="w")
        self.ent_date = tk.Entry(input_fr, width=15); self.ent_date.insert(0, "2026-01-04"); self.ent_date.grid(row=1, column=2, padx=5)
        self.btn_add = tk.Button(input_fr, text="Добавить", command=self.add_entry, bg="#e1f5fe", width=10); self.btn_add.grid(row=1, column=3, padx=5)
        self.btn_upd = tk.Button(input_fr, text="Изменить", command=self.update_entry, state=tk.DISABLED, width=10); self.btn_upd.grid(row=1, column=4, padx=5)

        # --- Блок фильтров ---
        filter_fr = tk.LabelFrame(root, text="Фильтрация и Бюджет", padx=10, pady=10)
        filter_fr.pack(fill="x", padx=10, pady=5)
        tk.Label(filter_fr, text="Дата (ГГГГ-ММ-ДД) С:").grid(row=0, column=0)
        self.ent_start = tk.Entry(filter_fr, width=12); self.ent_start.grid(row=0, column=1, padx=5)
        tk.Label(filter_fr, text="Дата (ГГГГ-ММ-ДД) По:").grid(row=0, column=2)
        self.ent_end = tk.Entry(filter_fr, width=12); self.ent_end.grid(row=0, column=3, padx=5)
        tk.Label(filter_fr, text="Бюджет:").grid(row=0, column=4, padx=(15,0))
        self.ent_budget = tk.Entry(filter_fr, width=10); self.ent_budget.insert(0, "50000"); self.ent_budget.grid(row=0, column=5)
        self.filter_var = tk.StringVar(value="Все")
        self.filter_combo = ttk.Combobox(filter_fr, textvariable=self.filter_var, state="readonly", width=15)
        self.filter_combo.grid(row=0, column=6, padx=15)
        tk.Button(filter_fr, text="Применить фильтр", command=self.refresh_table, bg="#c8e6c9").grid(row=0, column=7, padx=5)
        # Новая кнопка сброса
        tk.Button(filter_fr, text="Сброс", command=self.reset_filters, bg="#ffecb3").grid(row=0, column=8, padx=5)


        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("ID", "Sum", "Cat", "Date"), show='headings')
        for col, head in zip(self.tree["columns"], ["ID", "Сумма", "Категория", "Дата"]):
            self.tree.heading(col, text=head, command=lambda c=col: sort_treeview_column(self.tree, c, False))
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        self.tree.tag_configure('over', background='#ffcdd2')

        # --- Итоги ---
        footer = tk.Frame(root, padx=10, pady=10)
        footer.pack(fill="x")
        self.lbl_spent = tk.Label(footer, text="Потрачено: 0", fg="red", font=("Arial", 10, "bold"))
        self.lbl_spent.pack(side=tk.LEFT)
        self.lbl_remain = tk.Label(footer, text="Остаток: 0", font=("Arial", 10, "bold"))
        self.lbl_remain.pack(side=tk.LEFT, padx=20)
        tk.Button(footer, text="График месяцев", command=lambda: self.show_chart(True)).pack(side=tk.RIGHT)
        tk.Button(footer, text="Круговая диаграмма", command=lambda: self.show_chart(False)).pack(side=tk.RIGHT, padx=5)

        self.refresh_table()
        
    def reset_filters(self):
        """Сбрасывает все поля фильтрации и обновляет таблицу."""
        self.ent_start.delete(0, tk.END)
        self.ent_end.delete(0, tk.END)
        self.filter_var.set("Все") # Устанавливаем категорию по умолчанию
        self.refresh_table() # Применяем сброшенные фильтры

    def on_select(self, event):
        item = self.tree.selection()
        if item:
            v = self.tree.item(item)['values']
            self.editing_id = v
            self.ent_amt.delete(0, tk.END); self.ent_amt.insert(0, v)
            self.ent_cat.delete(0, tk.END); self.ent_cat.insert(0, v)
            self.ent_date.delete(0, tk.END); self.ent_date.insert(0, v)
            self.btn_upd.config(state=tk.NORMAL); self.btn_add.config(state=tk.DISABLED)

    def refresh_table(self):
        data = self.storage.load_all()
        cats = sorted(list(set(r['category'] for r in data)))
        self.filter_combo['values'] = ["Все"] + cats
        
        try: b_val = float(self.ent_budget.get() or 0)
        except: b_val = 0.0

        s_dt = self.ent_start.get() if validate_date(self.ent_start.get()) else None
        e_dt = self.ent_end.get() if validate_date(self.ent_end.get()) else None

        ana = FinanceAnalysis(data)
        rows, spent, rem = ana.get_summary(self.filter_var.get(), b_val, s_dt, e_dt)
        
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            tag = 'over' if rem < 0 else ''
            self.tree.insert("", tk.END, values=(r['id'], f"{float(r['amount']):.2f}", r['category'], r['date']), tags=(tag,))
        
        self.lbl_spent.config(text=f"Потрачено: {spent:.2f}")
        self.lbl_remain.config(text=f"Остаток: {rem:.2f}", fg="red" if rem < 0 else "green")

    def add_entry(self):
        a, c, d = self.ent_amt.get(), self.ent_cat.get(), self.ent_date.get()
        if validate_amount(a) and validate_date(d) and c:
            self.storage.save_operation(FinancialOperation(a, c, d))
            self.refresh_table()
        else: messagebox.showwarning("Ввод", "Ошибка в сумме или дате (ГГГГ-ММ-ДД)")

    def update_entry(self):
        a, c, d = self.ent_amt.get(), self.ent_cat.get(), self.ent_date.get()
        op = FinancialOperation(a, c, d, op_id=self.editing_id)
        if self.storage.update_operation(op):
            self.btn_upd.config(state=tk.DISABLED); self.btn_add.config(state=tk.NORMAL)
            self.refresh_table()

    def show_chart(self, monthly):
        try:
            ana = FinanceAnalysis(self.storage.load_all())
            if monthly: ana.plot_monthly()
            else: ana.plot_pie()
        except Exception as e: messagebox.showinfo("Инфо", str(e))
