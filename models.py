class FinancialOperation:
    """Класс сущности финансовой операции с поддержкой ID."""
    def __init__(self, amount, category, date, comment, op_type="expense", op_id=None):
        self.id = op_id
        self.amount = float(amount)
        self.category = category
        self.date = date
        self.comment = comment
        self.op_type = op_type

    def to_dict(self):
        """Преобразует объект в словарь для записи в CSV."""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "comment": self.comment,
            "op_type": self.op_type
        }
