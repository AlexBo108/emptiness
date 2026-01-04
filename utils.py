import re

def validate_amount(amount_str):
    """Проверка корректности суммы."""
    return bool(re.match(r"^\d+(\.\d{1,2})?$", amount_str))

def validate_date(date_str):
    """
    Проверка формата даты YYYY-MM-DD.
    Разрешает даты с 2000 по 2039 год (включая прошлые периоды).
    """
    if not date_str: return False
    pattern = r"^(20[0-3]\d)-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\d|3[0-1])$"
    return bool(re.match(pattern, date_str))

def sort_treeview_column(tree, col, reverse):
    """Сортировка таблицы по любой колонке."""
    data_list = [(tree.set(k, col), k) for k in tree.get_children('')]
    def try_convert(val):
        try: return float(val)
        except: return str(val).lower()
    data_list.sort(key=lambda t: try_convert(t), reverse=reverse)
    for index, (val, k) in enumerate(data_list):
        tree.move(k, '', index)
    tree.heading(col, command=lambda: sort_treeview_column(tree, col, not reverse))
