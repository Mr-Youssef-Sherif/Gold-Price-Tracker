import matplotlib.pyplot as plt
from datetime import date

today = date.today()

class GoldPricePlotter:
    def __init__(self, dates, column_Global_ounce, column_24k, column_22k, column_21k, column_18k, column_14k, column_12k, column_ounce, column_coin,path):
        self.dates = dates
        self.column_Global_ounce = column_Global_ounce
        self.column_24k = column_24k
        self.column_22k = column_22k
        self.column_21k = column_21k
        self.column_18k = column_18k
        self.column_14k = column_14k
        self.column_12k = column_12k
        self.column_ounce = column_ounce
        self.column_coin = column_coin
        self.path = path

    def annotate_points(self, ax, x, y):
        for i, (xi, yi) in enumerate(zip(x, y)):
            ax.annotate(f'{yi}', xy=(xi, yi), xytext=(0, -15), textcoords='offset points', ha='center', color='black')

    def get_line_color(self, items_list):
        if len(items_list) > 1:
            if items_list[-1] > items_list[-2]:
                return 'g.-'
            elif items_list[-1] < items_list[-2]:
                return 'r.-'
            else:
                return 'y.-'
        else:
            return 'g.-'

    def plot_gold_prices(self):
        fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(10, 14), dpi=500, edgecolor='black')

        data = [
            (self.column_Global_ounce, 'Global Ounce price'),
            (self.column_24k, '24 Karat price'),
            (self.column_22k, '22 Karat price'),
            (self.column_21k, '21 Karat price'),
            (self.column_18k, '18 Karat price'),
            (self.column_14k, '14 Karat price'),
            (self.column_12k, '12 Karat price'),
            (self.column_ounce, 'Gold ounce price'),
            (self.column_coin, 'Gold coin price')
        ]

        for i, (column, title) in enumerate(data):
            ax = axes[i // 2, i % 2]
            ax.plot(self.dates, column, self.get_line_color(column))
            ax.set_xlabel('Time yyyy/mm/dd')
            ax.set_ylabel('Price in EGP')
            ax.set_title(title)
            self.annotate_points(ax, self.dates, column)
            ax.tick_params(axis='x', rotation=70)

        fig.delaxes(axes.flatten()[-1])

        plt.tight_layout()
        plt.savefig(self.path, format='jpg', dpi=500)
        plt.close()
        print("Saved plots")