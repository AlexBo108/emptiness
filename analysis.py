import pandas as pd
import matplotlib.pyplot as plt

class FinanceAnalysis:
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        if not self.df.empty:
            self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
            self.df.dropna(subset=['amount', 'date'], inplace=True)

    def get_summary(self, category="Все", budget=0.0, start=None, end=None):
        if self.df.empty: return [], 0.0, budget, 0.0
        f_df = self.df.copy()
        if start: f_df = f_df[f_df['date'] >= pd.to_datetime(start)]
        if end: f_df = f_df[f_df['date'] <= pd.to_datetime(end)]
        if category != "Все": f_df = f_df[f_df['category'] == category]
            
        income = f_df[f_df['op_type'] == 'income']['amount'].sum()
        spent = f_df[f_df['op_type'] == 'expense']['amount'].sum()
        f_df['date'] = f_df['date'].dt.strftime('%Y-%m-%d')
        return f_df.to_dict('records'), spent, budget - spent, income

    def plot_pie_chart(self):
        """Круговая диаграмма расходов."""
        exp_df = self.df[self.df['op_type'] == 'expense']
        if exp_df.empty: return
        summary = exp_df.groupby('category')['amount'].sum()
        plt.figure(figsize=(8, 6))
        summary.plot(kind='pie', autopct='%1.1f%%', title="Расходы по категориям 2026")
        plt.ylabel('')
        plt.show()

    def plot_bar_chart(self):
        """Столбчатая диаграмма доходов и расходов по месяцам."""
        if self.df.empty: return
        # Группируем по месяцу и типу
        self.df['month'] = self.df['date'].dt.to_period('M')
        summary = self.df.pivot_table(index='month', columns='op_type', values='amount', aggfunc='sum').fillna(0)
        summary.plot(kind='bar', figsize=(10, 6))
        plt.title("Доходы и Расходы по месяцам 2026")
        plt.xlabel("Месяц")
        plt.ylabel("Сумма")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
