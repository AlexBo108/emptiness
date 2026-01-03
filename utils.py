import re

def validate_amount(amount_str):
    """Проверка суммы (число с 1-2 знаками после точки)."""
    return bool(re.match(r"^\d+(\.\d{1,2})?$", amount_str))

def validate_date(date_str):
    """Проверка формата даты YYYY-MM-DD."""
    return bool(re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", date_str))
