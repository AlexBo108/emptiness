import pandas as pd
import matplotlib.pyplot as plt

class FinanceAnalysis:
    """Анализ данных через Pandas."""
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        if not self.df.empty:
            self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
            self.df.dropna(subset=['amount', 'category'], inplace=True)

    def get_filtered_data(self, category=None):
        """Возвращает отфильтрованные данные и их сумму."""
        if self.df.empty:
            return [], 0.0
        
        filtered_df = self.df
        if category and category != "Все":
            filtered_df = self.df[self.df['category'] == category]
            
        total = filtered_df['amount'].sum()
        return filtered_df.to_dict('records'), total

    def plot_expenses(self):
        """Круговая диаграмма расходов."""
        if self.df.empty: raise ValueError("Нет данных")
        summary = self.df.groupby('category')['amount'].sum()
        summary.plot(kind='pie', autopct='%1.1f%%', title='Расходы по категориям 2026')
        plt.ylabel('')
        plt.show()
