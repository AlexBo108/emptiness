import csv
import os

class FileStorage:
    """Класс для работы с CSV файлом."""
    def __init__(self, filename="data/finance.csv"):
        self.filename = filename
        if not os.path.exists("data"):
            os.makedirs("data")

    def save_operation(self, op_obj):
        """Сохраняет операцию в файл."""
        try:
            file_exists = os.path.isfile(self.filename)
            with open(self.filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=op_obj.to_dict().keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(op_obj.to_dict())
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")

    def load_all(self):
        """Загружает все данные."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []
