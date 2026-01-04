import re

def validate_amount(amount_str):
    """Проверка числового ввода."""
    return bool(re.match(r"^\d+(\.\d{1,2})?$", amount_str))

def validate_date(date_str):
    """Проверка формата даты YYYY-MM-DD."""
    pattern = r"^20[2-3]\d-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\d|3[0-1])$"
    return bool(re.match(pattern, date_str))

def sort_treeview_column(tree, col, reverse):
    """Сортировка данных в Treeview по любой колонке."""
    data_list = [(tree.set(k, col), k) for k in tree.get_children('')]

    def try_convert(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return str(val).lower()

    data_list.sort(key=lambda t: try_convert(t[0]), reverse=reverse)
    for index, (val, k) in enumerate(data_list):
        tree.move(k, '', index)
    
    # Переключаем направление сортировки для следующего клика
    tree.heading(col, command=lambda: sort_treeview_column(tree, col, not reverse))
