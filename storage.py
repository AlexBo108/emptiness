import csv
import os

class FileStorage:
    """Безопасное хранение данных в CSV с автоинкрементом."""
    def __init__(self, filename="data/finance.csv"):
        self.filename = filename
        self.fieldnames = ["id", "amount", "category", "date", "comment", "op_type"]
        if not os.path.exists("data"):
            os.makedirs("data")

    def load_all(self):
        """Загрузка данных с обработкой ошибок файла."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return [row for row in reader if row]
        except Exception as e:
            print(f"Ошибка чтения: {e}")
            return []

    def save_operation(self, op):
        """Сохранение с генерацией ID и защитой от ошибок записи."""
        try:
            data = self.load_all()
            ids = [int(d['id']) for d in data if d.get('id') and d['id'].isdigit()]
            op.id = max(ids, default=0) + 1

            file_empty = not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0
            
            with open(self.filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                if file_empty:
                    writer.writeheader()
                writer.writerow(op.to_dict())
            return True
        except (IOError, PermissionError) as e:
            print(f"Ошибка доступа к файлу: {e}")
            return False
