import csv
import os

class FileStorage:
    """Хранение данных в CSV."""
    def __init__(self, filename="data/finance.csv"):
        self.filename = filename
        self.fieldnames = ["id", "amount", "category", "date", "comment", "op_type"]
        if not os.path.exists("data"):
            os.makedirs("data")

    def load_all(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return [row for row in csv.DictReader(f) if row]
        except Exception:
            return []

    def save_operation(self, op):
        try:
            data = self.load_all()
            ids = [int(d['id']) for d in data if d.get('id', '').isdigit()]
            op.id = max(ids, default=0) + 1
            file_empty = not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0
            with open(self.filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                if file_empty: writer.writeheader()
                writer.writerow(op.to_dict())
            return True
        except Exception:
            return False
