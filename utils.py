import re

def validate_amount(amount_str):
    """Проверяет корректность ввода суммы с помощью регулярных выражений."""
    pattern = r"^\d+(\.\d{1,2})?$"
    if re.match(pattern, amount_str):
        return True
    return False

def validate_date(date_str):
    """Проверяет формат даты YYYY-MM-DD."""
    pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    return bool(re.match(pattern, date_str))
