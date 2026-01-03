import re

def validate_amount(amount_str):
    """Проверка числового ввода."""
    return bool(re.match(r"^\d+(\.\d{1,2})?$", amount_str))

def validate_date(date_str):
    """Проверка формата даты YYYY-MM-DD для 2026 года."""
    pattern = r"^202[6-9]-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\d|3[0-1])$"
    return bool(re.match(pattern, date_str))

def sort_treeview_column(tree, col, reverse):
    """Сортировка таблицы."""
    l = [(tree.set(k, col), k) for k in tree.get_children('')]
    try:
        l.sort(key=lambda t: float(t[0]), reverse=reverse)
    except ValueError:
        l.sort(key=lambda t: t[0].lower(), reverse=reverse)
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)
    tree.heading(col, command=lambda: sort_treeview_column(tree, col, not reverse))
