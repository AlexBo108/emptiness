class FinancialOperation:
    """Класс сущности финансовой операции с локализованными типами."""
    def __init__(self, amount, category, date, comment="", op_type="Расход", op_id=None):
        self.id = op_id
        self.amount = float(amount)
        self.category = category.strip()
        self.date = date
        self.comment = comment.strip()
        self.op_type = op_type  # "Расход" или "Доход"

    def to_dict(self):
        """Преобразует объект в словарь для сохранения."""
        return {
            "id": self.id, 
            "amount": self.amount, 
            "category": self.category,
            "date": self.date, 
            "comment": self.comment, 
            "op_type": self.op_type
        }
