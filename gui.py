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
        self.editing_item_id = None # Для отслеживания редактируемой записи
        
        # ... (Код стилей опущен для краткости, он есть в предыдущем ответе) ...

        # --- Блок ввода Операций (с добавлением кнопки "Обновить") ---
        input_frame = tk.LabelFrame(root, text="Управление записью", padx=10, pady=5)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Сумма:").grid(row=0, column=0)
        self.ent_amt = tk.Entry(input_frame, width=10)
        self.ent_amt.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Категория:").grid(row=0, column=2)
        self.ent_cat = tk.Entry(input_frame, width=15)
        self.ent_cat.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4)
        self.ent_date = tk.Entry(input_frame, width=12)
        self.ent_date.insert(0, "2026-01-03")
        self.ent_date.grid(row=0, column=5, padx=5)

        # Кнопки "Добавить" и "Обновить"
        self.btn_add = tk.Button(input_frame, text="Добавить", command=self.add_entry, bg="#e3f2fd")
        self.btn_add.grid(row=0, column=6, padx=5, sticky="we")

        self.btn_update = tk.Button(input_frame, text="Обновить", command=self.update_entry, bg="#fff8e1", state=tk.DISABLED)
        self.btn_update.grid(row=0, column=7, padx=5, sticky="we")

        # ... (Код блока Бюджета и Фильтрации остается прежним) ...
        control_frame = tk.Frame(root, padx=10, pady=5)
        control_frame.pack(fill="x")
        # ... (UI элементы фильтра и бюджета, привязки) ...
        tk.Label(control_frame, text="Плановый бюджет:").pack(side=tk.LEFT)
        self.ent_budget = tk.Entry(control_frame, width=10); self.ent_budget.insert(0, "50000"); self.ent_budget.pack(side=tk.LEFT, padx=5)
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
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        # Привязка события выбора строки к функции on_tree_select
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        self.tree.tag_configure('over_budget', background='#ffcdd2')


        # --- Подвал ---
        footer = tk.Frame(root, padx=10, pady=10)
        footer.pack(fill="x")
        self.lbl_total = tk.Label(footer, text="Потрачено: 0", font=("Arial", 10))
        self.lbl_total.pack(side=tk.LEFT)
        self.lbl_remain = tk.Label(footer, text="Остаток: 0", font=("Arial", 11, "bold"), padx=20)
        self.lbl_remain.pack(side=tk.LEFT)
        tk.Button(footer, text="📊 График", command=self.show_chart).pack(side=tk.RIGHT)

        self.refresh_table()
        
    def on_tree_select(self, event):
        """Заполняет поля ввода данными из выбранной строки."""
        selected_item = self.tree.selection()
        if selected_item:
            self.editing_item_id = self.tree.item(selected_item)['values'][0] # Получаем ID из первого столбца
            values = self.tree.item(selected_item)['values']
            
            # Очищаем поля и вставляем данные
            self.ent_amt.delete(0, tk.END); self.ent_amt.insert(0, values[1])
            self.ent_cat.delete(0, tk.END); self.ent_cat.insert(0, values[2])
            self.ent_date.delete(0, tk.END); self.ent_date.insert(0, values[3])
            
            # Активируем кнопку "Обновить" и деактивируем "Добавить"
            self.btn_update.config(state=tk.NORMAL)
            self.btn_add.config(state=tk.DISABLED)

    def update_entry(self):
        """Обрабатывает обновление существующей записи."""
        if not self.editing_item_id: return

        amt, dt, cat = self.ent_amt.get(), self.ent_date.get(), self.ent_cat.get()
        if validate_amount(amt) and validate_date(dt) and cat:
            updated_op = FinancialOperation(amt, cat, dt, "comment", op_id=self.editing_item_id)
            
            if self.storage.update_operation(updated_op):
                messagebox.showinfo("Успех", f"Запись ID {self.editing_item_id} обновлена.")
                self.reset_ui_state()
            else:
                messagebox.showerror("Ошибка", "Ошибка обновления данных.")
        else:
            messagebox.showwarning("Ввод", "Неверные данные.")

    def reset_ui_state(self):
        """Сбрасывает интерфейс в режим добавления."""
        self.editing_item_id = None
        self.ent_amt.delete(0, tk.END)
        self.ent_cat.delete(0, tk.END)
        # self.ent_date.delete(0, tk.END) # Дату можно оставить
        self.btn_update.config(state=tk.DISABLED)
        self.btn_add.config(state=tk.NORMAL)
        self.refresh_table()

    def refresh_table(self):
        # ... (Код refresh_table остается прежним, использует analysis.py) ...
        data = self.storage.load_all()
        cats = sorted(list(set(r['category'] for r in data)))
        self.filter_combo['values'] = ["Все"] + cats

        try: budget_val = float(self.ent_budget.get()) if self.ent_budget.get() else 0.0
        except ValueError: budget_val = 0.0

        analysis = FinanceAnalysis(data)
        rows, total, remain = analysis.get_summary(self.filter_var.get(), budget_val)

        self.tree.delete(*self.tree.get_children())
        is_over = remain < 0

        for r in rows:
            tag = 'over_budget' if is_over else ''
            self.tree.insert("", tk.END, values=(r['id'], f"{float(r['amount']):.2f}", r['category'], r['date']), tags=(tag,))

        self.lbl_total.config(text=f"Потрачено: {total:.2f}")
        self.lbl_remain.config(text=f"Остаток: {remain:.2f}", fg="red" if is_over else "green")


    def add_entry(self):
        """Обработка добавления новой записи."""
        # ... (Код add_entry остается прежним) ...
        amt, dt, cat = self.ent_amt.get(), self.ent_date.get(), self.ent_cat.get()
        if validate_amount(amt) and validate_date(dt) and cat:
            if self.storage.save_operation(FinancialOperation(amt, cat, dt, "comment")):
                self.reset_ui_state() # Сброс после добавления
            else: messagebox.showerror("Ошибка", "Ошибка записи")
        else: messagebox.showwarning("Ввод", "Неверные данные")

    def show_chart(self):
        # ... (Код show_chart остается прежним) ...
        try:
            FinanceAnalysis(self.storage.load_all()).plot_pie()
        except Exception as e: messagebox.showinfo("Инфо", str(e))
