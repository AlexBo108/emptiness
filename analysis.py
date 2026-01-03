import pandas as pd
import matplotlib.pyplot as plt

class FinanceAnalysis:
    """Класс для анализа и визуализации данных."""
    def __init__(self, data_list):
        self.df = pd.DataFrame(data_list)
        if not self.df.empty:
            self.df['amount'] = pd.to_numeric(self.df['amount'])
            self.df['date'] = pd.to_datetime(self.df['date'])

    def get_category_totals(self):
        """Считает расходы по категориям."""
        if self.df.empty: return "Нет данных"
        expenses = self.df[self.df['op_type'] == 'expense']
        return expenses.groupby('category')['amount'].sum()

    def plot_pie_chart(self):
        """Строит круговую диаграмму расходов."""
        totals = self.get_category_totals()
        if isinstance(totals, str): return
        
        plt.figure(figsize=(8, 6))
        totals.plot(kind='pie', autopct='%1.1f%%')
        plt.title("Расходы по категориям")
        plt.ylabel("")
        plt.show()
        