import pandas as pd
import matplotlib.pyplot as plt

class FinanceAnalysis:
    """Аналитика данных с использованием Pandas."""
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        if not self.df.empty:
            # errors='coerce' превратит битые данные в NaN, чтобы программа не упала
            self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
            self.df.dropna(subset=['amount', 'category'], inplace=True)

    def plot_expenses(self):
        """Визуализация расходов."""
        if self.df.empty:
            raise ValueError("Нет данных для анализа")
        
        exp_df = self.df[self.df['op_type'] == 'expense']
        if exp_df.empty:
            raise ValueError("Нет данных по расходам")

        summary = exp_df.groupby('category')['amount'].sum()
        plt.figure(figsize=(8, 6))
        summary.plot(kind='pie', autopct='%1.1f%%', title='Расходы 2026')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()
