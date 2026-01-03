import datetime

class FinancialOperation:
    """Класс, описывающий одну финансовую операцию."""
    def __init__(self, amount, category, date, comment, op_type="expense"):
        self.amount = float(amount)
        self.category = category
        self.date = date  # Формат YYYY-MM-DD
        self.comment = comment
        self.op_type = op_type  # 'income' или 'expense'

    def to_dict(self):
        """Преобразует объект в словарь для сохранения."""
        return self.__dict__
    