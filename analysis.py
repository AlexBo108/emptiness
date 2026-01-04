import pandas as pd
import matplotlib.pyplot as plt

class FinanceAnalysis:
    """Анализ данных через Pandas с фильтрацией по датам."""
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        if not self.df.empty:
            self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
            self.df.dropna(subset=['amount', 'date'], inplace=True)

    def get_summary(self, category_filter="Все", budget=0.0, date_start=None, date_end=None):
        if self.df.empty: return [], 0.0, budget
        
        f_df = self.df.copy()
        
        # Фильтр по датам
        if date_start:
            f_df = f_df[f_df['date'] >= pd.to_datetime(date_start)]
        if date_end:
            f_df = f_df[f_df['date'] <= pd.to_datetime(date_end)]
            
        # Фильтр по категории
        if category_filter != "Все":
            f_df = f_df[f_df['category'] == category_filter]
            
        total = f_df['amount'].sum()
        # Возвращаем дату обратно в строку для интерфейса
        f_df['date'] = f_df['date'].dt.strftime('%Y-%m-%d')
        return f_df.to_dict('records'), total, budget - total

    def plot_pie(self):
        self.df.groupby('category')['amount'].sum().plot(kind='pie', autopct='%1.1f%%')
        plt.title("Расходы по категориям 2026")
        plt.ylabel(''); plt.show()

    def plot_monthly(self):
        self.df.set_index('date').resample('MS')['amount'].sum().plot(kind='bar', color='skyblue')
        plt.title("Траты по месяцам 2026")
        plt.tight_layout(); plt.show()
