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
        if not os.path.exists(self.filename): return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return [row for row in csv.DictReader(f) if row]
        except: return []

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
        except: return False

    def update_operation(self, op):
        data = self.load_all()
        for i, row in enumerate(data):
            if int(row['id']) == int(op.id):
                data[i] = op.to_dict()
                break
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except: return False
