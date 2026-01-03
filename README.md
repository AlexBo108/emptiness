# Financial Planner 2026
Простое и надежное приложение для управления личными финансами.

## Возможности
- Добавление операций (доходы/расходы).
- Валидация данных через регулярные выражения.
- Хранение истории в CSV.
- Аналитика с помощью Pandas.
- Визуализация (Matplotlib).

## Как запустить
1. Установите зависимости: `pip install pandas matplotlib`
2. Запустите программу: `python main.py`
3. Для тестов: `python tests.py`

text

finance_planner/
├── main.py            # Точка входа
├── models.py          # Классы сущностей
├── storage.py         # Работа с CSV/БД
├── analysis.py        # Логика Pandas и Matplotlib
├── utils.py           # Валидация через re и вспомогательные функции
├── gui.py             # Интерфейс на Tkinter
├── tests.py           # Unit-тесты
└── data/              # Директория для CSV
