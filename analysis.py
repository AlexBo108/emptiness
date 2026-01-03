import pandas as pd
import matplotlib.pyplot as plt

class FinanceAnalysis:
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        if not self.df.empty:
            self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
            self.df.dropna(subset=['amount'], inplace=True)

    def get_summary(self, category_filter="Все", budget=0.0):
        if self.df.empty: return [], 0.0, budget
        filtered_df = self.df
        if category_filter != "Все":
            filtered_df = self.df[self.df['category'] == category_filter]
        total_spent = filtered_df['amount'].sum()
        remaining = budget - total_spent
        return filtered_df.to_dict('records'), total_spent, remaining

    def plot_pie(self):
        if self.df.empty: return
        self.df.groupby('category')['amount'].sum().plot(kind='pie', autopct='%1.1f%%')
        plt.title("Распределение трат 2026")
        plt.show()
