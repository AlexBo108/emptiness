import csv
import os

class FileStorage:
    """Управление CSV файлом с поддержкой обновления записей."""
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
        """Сохранение новой операции с генерацией ID."""
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
            
    def update_operation(self, updated_op):
        """Обновление существующей операции по ID."""
        data = self.load_all()
        found = False
        for i, row in enumerate(data):
            if int(row['id']) == int(updated_op.id):
                data[i] = updated_op.to_dict()
                found = True
                break
        
        if found:
            # Перезаписываем весь файл с обновленными данными
            try:
                with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
                return True
            except Exception:
                return False
        return False
