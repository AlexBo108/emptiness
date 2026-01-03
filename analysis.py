import pandas as pd
import matplotlib.pyplot as plt

class FinanceAnalysis:
    """Анализ данных через Pandas и визуализация Matplotlib."""
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        if not self.df.empty:
            self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce') 
            self.df.dropna(subset=['amount', 'date', 'category'], inplace=True) # Очистка неполных строк

    def get_summary(self, category_filter="Все", budget=0.0):
        """Возвращает отфильтрованные данные, сумму и остаток бюджета."""
        if self.df.empty:
            return [], 0.0, budget

        filtered_df = self.df
        if category_filter != "Все":
            filtered_df = self.df[self.df['category'] == category_filter]

        total_spent = filtered_df['amount'].sum()
        remaining = budget - total_spent
        return filtered_df.to_dict('records'), total_spent, remaining

    def plot_pie_chart(self):
        """Круговая диаграмма расходов по категориям."""
        if self.df.empty: raise ValueError("Нет данных для анализа")
        summary = self.df.groupby('category')['amount'].sum()
        if summary.empty: raise ValueError("Нет данных для графика")
        plt.figure(figsize=(8, 6))
        summary.plot(kind='pie', autopct='%1.1f%%', title='Расходы по категориям 2026')
        plt.ylabel('')
        plt.show()
        
    def plot_monthly_expenses(self):
        """График трат по месяцам (гистограмма)."""
        if self.df.empty: raise ValueError("Нет данных для анализа")
        
        monthly_summary = self.df.set_index('date').resample('MS')['amount'].sum()
        if monthly_summary.empty: raise ValueError("Нет данных для графика")

        plt.figure(figsize=(10, 6))
        monthly_summary.plot(kind='bar', color='skyblue')
        plt.title("Траты по месяцам")
        plt.xlabel("Месяц")
        plt.ylabel("Сумма расходов")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--')
        plt.show()
