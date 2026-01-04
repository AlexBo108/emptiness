import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        self.filtered_data_cache = []

        # --- Блок ввода ---
        input_fr = tk.LabelFrame(root, text="Данные операции", padx=10, pady=10)
        input_fr.pack(fill="x", padx=10, pady=5)
        
        tk.Label(input_fr, text="Сумма").grid(row=0, column=0, sticky="w")
        self.ent_amt = tk.Entry(input_fr, width=15); self.ent_amt.grid(row=1, column=0, padx=5)
        tk.Label(input_fr, text="Категория").grid(row=0, column=1, sticky="w")
        self.ent_cat = tk.Entry(input_fr, width=20); self.ent_cat.grid(row=1, column=1, padx=5)
        tk.Label(input_fr, text="Дата (ГГГГ-ММ-ДД)").grid(row=0, column=2, sticky="w")
        self.ent_date = tk.Entry(input_fr, width=15); self.ent_date.insert(0, "2026-01-04"); self.ent_date.grid(row=1, column=2, padx=5)
        
        tk.Label(input_fr, text="Комментарий").grid(row=2, column=0, sticky="w", pady=(5,0))
        self.ent_comm = tk.Entry(input_fr, width=55); self.ent_comm.grid(row=3, column=0, columnspan=3, padx=5, sticky="we")

        self.btn_exp = tk.Button(input_fr, text="Добавить Расход", bg="#ffcdd2", command=lambda: self.process_entry("Расход"))
        self.btn_exp.grid(row=3, column=3, padx=5)
        self.btn_inc = tk.Button(input_fr, text="Добавить Доход", bg="#c8e6c9", command=lambda: self.process_entry("Доход"))
        self.btn_inc.grid(row=3, column=4, padx=5)
        tk.Button(input_fr, text="Отмена", command=self.reset_ui).grid(row=3, column=5, padx=5)

        # --- ФИЛЬТРЫ ---
        filter_fr = tk.LabelFrame(root, text="Фильтры и Бюджет", padx=10, pady=10)
        filter_fr.pack(fill="x", padx=10, pady=5)
        tk.Label(filter_fr, text="Дата (ГГГГ-ММ-ДД) С:").grid(row=0, column=0)
        self.ent_start = tk.Entry(filter_fr, width=12); self.ent_start.grid(row=0, column=1, padx=5)
        tk.Label(filter_fr, text="Дата (ГГГГ-ММ-ДД) По:").grid(row=0, column=2)
        self.ent_end = tk.Entry(filter_fr, width=12); self.ent_end.grid(row=0, column=3, padx=5)
        tk.Label(filter_fr, text="Бюджет (Лимит):").grid(row=0, column=4, padx=(15,0))
        self.ent_budget = tk.Entry(filter_fr, width=10); self.ent_budget.insert(0, "50000"); self.ent_budget.grid(row=0, column=5)
        self.filter_var = tk.StringVar(value="Все")
        self.filter_combo = ttk.Combobox(filter_fr, textvariable=self.filter_var, state="readonly", width=15)
        self.filter_combo.grid(row=0, column=6, padx=10)
        tk.Button(filter_fr, text="Применить", command=self.refresh_table, bg="#c8e6c9").grid(row=0, column=7, padx=5)
        tk.Button(filter_fr, text="Сброс", command=self.reset_all_filters, bg="#ffecb3").grid(row=0, column=8, padx=5)
        tk.Button(filter_fr, text="Экспорт в CSV", command=self.export_csv, bg="#bbdefb").grid(row=0, column=9, padx=5)

        # --- ТАБЛИЦА ---
        self.tree = ttk.Treeview(root, columns=("ID", "Сумма", "Категория", "Дата", "Комментарий", "Тип"), show='headings')
        heads = [("ID", 50), ("Сумма", 100), ("Категория", 150), ("Дата", 100), ("Комментарий", 200), ("Тип", 100)]
        for h, w in heads:
            self.tree.heading(h, text=h, command=lambda c=h: sort_treeview_column(self.tree, c, False))
            self.tree.column(h, width=w, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        self.tree.tag_configure('over', background='#ffcdd2')

        # --- ИТОГИ ---
        footer = tk.Frame(root, padx=10, pady=10)
        footer.pack(fill="x")
        self.lbl_income = tk.Label(footer, text="Доход: 0", fg="green", font=("Arial", 10, "bold"))
        self.lbl_income.pack(side=tk.LEFT)
        self.lbl_spent = tk.Label(footer, text="Потрачено: 0", fg="red", font=("Arial", 10, "bold"), padx=20)
        self.lbl_spent.pack(side=tk.LEFT)
        self.lbl_rem = tk.Label(footer, text="Остаток: 0", font=("Arial", 10, "bold"))
        self.lbl_rem.pack(side=tk.LEFT)
        tk.Button(footer, text="Аналитика по месяцам", command=self.show_bar_chart).pack(side=tk.RIGHT, padx=5)
        tk.Button(footer, text="Круговая диаграмма", command=self.show_pie_chart).pack(side=tk.RIGHT, padx=5)
        self.refresh_table()

    def on_select(self, event):
        sel = self.tree.selection()
        if sel:
            v = self.tree.item(sel)['values']
            self.editing_id = v[0]
            self.ent_amt.delete(0, tk.END); self.ent_amt.insert(0, v[1])
            self.ent_cat.delete(0, tk.END); self.ent_cat.insert(0, v[2])
            self.ent_date.delete(0, tk.END); self.ent_date.insert(0, v[3])
            self.ent_comm.delete(0, tk.END); self.ent_comm.insert(0, v[4])
            self.btn_exp.config(text="Изменить Расход")
            self.btn_inc.config(text="Изменить Доход")

    def process_entry(self, op_type):
        a, c, d, cm = self.ent_amt.get(), self.ent_cat.get(), self.ent_date.get(), self.ent_comm.get()
        if validate_amount(a) and validate_date(d) and c:
            op = FinancialOperation(a, c, d, cm, op_type=op_type, op_id=self.editing_id)
            if self.editing_id: self.storage.update_operation(op)
            else: self.storage.save_operation(op)
            self.reset_ui()
        else: messagebox.showwarning("Ошибка", "Проверьте данные (сумма, категория, дата ГГГГ-ММ-ДД)")

    def reset_ui(self):
        self.editing_id = None
        self.ent_amt.delete(0, tk.END); self.ent_cat.delete(0, tk.END); self.ent_comm.delete(0, tk.END)
        self.btn_exp.config(text="Добавить Расход"); self.btn_inc.config(text="Добавить Доход")
        self.refresh_table()

    def refresh_table(self):
        data = self.storage.load_all()
        self.filter_combo['values'] = ["Все"] + sorted(list(set(r['category'] for r in data)))
        try: b = float(self.ent_budget.get())
        except: b = 0.0
        s_dt = self.ent_start.get() if validate_date(self.ent_start.get()) else None
        e_dt = self.ent_end.get() if validate_date(self.ent_end.get()) else None
        rows, spent, rem, inc = FinanceAnalysis(data).get_summary(self.filter_var.get(), b, s_dt, e_dt)
        self.filtered_data_cache = rows
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            tag = 'over' if rem < 0 and r['op_type'] == 'Расход' else ''
            self.tree.insert("", tk.END, values=(r['id'], f"{float(r['amount']):.2f}", r['category'], r['date'], r['comment'], r['op_type']), tags=(tag,))
        self.lbl_income.config(text=f"Доход: {inc:.2f}")
        self.lbl_spent.config(text=f"Потрачено: {spent:.2f}")
        self.lbl_rem.config(text=f"Остаток: {rem:.2f}", fg="red" if rem < 0 else "black")

    def export_csv(self):
        if not self.filtered_data_cache:
            messagebox.showwarning("Экспорт", "Нет данных")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path: self.storage.export_to_csv(self.filtered_data_cache, path)

    def reset_all_filters(self):
        self.filter_var.set("Все"); self.ent_start.delete(0, tk.END); self.ent_end.delete(0, tk.END)
        self.refresh_table()

    def show_pie_chart(self):
        FinanceAnalysis(self.storage.load_all()).plot_pie_chart()

    def show_bar_chart(self):
        FinanceAnalysis(self.storage.load_all()).plot_bar_chart()
