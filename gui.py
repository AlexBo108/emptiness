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
        self.editing_id = None

        # --- Форма ввода ---
        input_fr = tk.LabelFrame(root, text="Управление операциями", padx=10, pady=10)
        input_fr.pack(fill="x", padx=10, pady=5)

        # Подписи над полями
        tk.Label(input_fr, text="Сумма").grid(row=0, column=0, sticky="w")
        self.ent_amt = tk.Entry(input_fr, width=15)
        self.ent_amt.grid(row=1, column=0, padx=5)

        tk.Label(input_fr, text="Категория").grid(row=0, column=1, sticky="w")
        self.ent_cat = tk.Entry(input_fr, width=20)
        self.ent_cat.grid(row=1, column=1, padx=5)

        tk.Label(input_fr, text="Дата (ГГГГ-ММ-ДД)").grid(row=0, column=2, sticky="w")
        self.ent_date = tk.Entry(input_fr, width=15)
        self.ent_date.insert(0, "2026-01-04")
        self.ent_date.grid(row=1, column=2, padx=5)

        self.btn_add = tk.Button(input_fr, text="Добавить", command=self.add_entry, width=10, bg="#e1f5fe")
        self.btn_add.grid(row=1, column=3, padx=5)
        
        self.btn_upd = tk.Button(input_fr, text="Изменить", command=self.update_entry, state=tk.DISABLED, width=10)
        self.btn_upd.grid(row=1, column=4, padx=5)

        # --- Бюджет и Фильтр ---
        ctrl_fr = tk.Frame(root, padx=10)
        ctrl_fr.pack(fill="x", pady=5)
        
        tk.Label(ctrl_fr, text="Ваш бюджет:").pack(side=tk.LEFT)
        self.ent_budget = tk.Entry(ctrl_fr, width=12)
        self.ent_budget.insert(0, "50000")
        self.ent_budget.pack(side=tk.LEFT, padx=5)
        self.ent_budget.bind("<KeyRelease>", lambda e: self.refresh_table())

        self.filter_var = tk.StringVar(value="Все категории")
        self.filter_combo = ttk.Combobox(ctrl_fr, textvariable=self.filter_var, state="readonly")
        self.filter_combo.pack(side=tk.RIGHT)
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("ID", "Sum", "Cat", "Date"), show='headings')
        for col, head in zip(self.tree["columns"], ["ID", "Сумма", "Категория", "Дата"]):
            self.tree.heading(col, text=head, command=lambda c=col: sort_treeview_column(self.tree, c, False))
            self.tree.column(col, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        self.tree.tag_configure('over', background='#ffcdd2') # Подсветка строк при превышении

        # --- Подвал с итогами ---
        footer = tk.Frame(root, padx=10, pady=10)
        footer.pack(fill="x")
        
        # Потрачено (всегда Красный и Жирный)
        self.lbl_spent = tk.Label(footer, text="Потрачено: 0", fg="red", font=("Arial", 10, "bold"))
        self.lbl_spent.pack(side=tk.LEFT)

        # Остаток (Цвет меняется динамически)
        self.lbl_remain = tk.Label(footer, text="Остаток: 0", font=("Arial", 10, "bold"))
        self.lbl_remain.pack(side=tk.LEFT, padx=20)

        tk.Button(footer, text="График месяцев", command=lambda: self.show_chart(True)).pack(side=tk.RIGHT)
        tk.Button(footer, text="Круговая диаграмма", command=lambda: self.show_chart(False)).pack(side=tk.RIGHT, padx=5)

        self.refresh_table()

    def on_select(self, event):
        item = self.tree.selection()
        if item:
            v = self.tree.item(item)['values']
            self.editing_id = v[0]
            self.ent_amt.delete(0, tk.END); self.ent_amt.insert(0, v[1])
            self.ent_cat.delete(0, tk.END); self.ent_cat.insert(0, v[2])
            self.ent_date.delete(0, tk.END); self.ent_date.insert(0, v[3])
            self.btn_upd.config(state=tk.NORMAL); self.btn_add.config(state=tk.DISABLED)

    def refresh_table(self):
        data = self.storage.load_all()
        cats = sorted(list(set(r['category'] for r in data)))
        self.filter_combo['values'] = ["Все категории"] + cats
        
        try: b_val = float(self.ent_budget.get() or 0)
        except: b_val = 0.0

        ana = FinanceAnalysis(data)
        rows, spent, rem = ana.get_summary(self.filter_var.get() if self.filter_var.get() != "Все категории" else "Все", b_val)
        
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            tag = 'over' if rem < 0 else ''
            self.tree.insert("", tk.END, values=(r['id'], f"{float(r['amount']):.2f}", r['category'], r['date']), tags=(tag,))
        
        # Обновление лейблов
        self.lbl_spent.config(text=f"Потрачено: {spent:.2f}")
        
        # Логика цвета Остатка
        rem_color = "red" if rem < 0 else "green"
        self.lbl_remain.config(text=f"Остаток: {rem:.2f}", fg=rem_color)

    def add_entry(self):
        a, c, d = self.ent_amt.get(), self.ent_cat.get(), self.ent_date.get()
        if validate_amount(a) and validate_date(d) and c:
            self.storage.save_operation(FinancialOperation(a, c, d))
            self.refresh_table()
            self.ent_amt.delete(0, tk.END)
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
            ana.plot_monthly() if monthly else ana.plot_pie()
        except Exception as e: messagebox.showinfo("Инфо", str(e))
