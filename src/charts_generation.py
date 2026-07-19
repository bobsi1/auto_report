import matplotlib.pyplot as plt
from pathlib import Path

def create_overview_charts(df):
    proj_path = Path.cwd().parent
    charts_path = proj_path / 'charts'
    charts_paths = {}

    #Orders by months chart
    orders_by_year_month = df.groupby('Order year_month')['Order ID'].nunique()
    plt.figure(figsize=(12, 6))
    plt.plot(orders_by_year_month.index,
             orders_by_year_month.values, marker='o', color='#CCCCFF',
             markeredgecolor='#9966CC', markersize=5)
    plt.xticks(orders_by_year_month.index[::3], rotation=-45)
    plt.title('Orders by months')
    plt.xlabel('Months')
    plt.ylabel('Number of Orders')
    plt.savefig(charts_path / 'orders_by_months_line.png')
    charts_paths['orders_by_months_line'] = charts_path / 'orders_by_months_line.png'

    #Orders by years chart
    orders_by_year = df.groupby('Order_year')['Order ID'].nunique()
    plt.figure(figsize=(9, 6))
    plt.bar(orders_by_year.index, orders_by_year.values,
            color='#CCCCFF', edgecolor='#9966CC')
    plt.xticks(orders_by_year.index[::1], rotation=-45)
    plt.title('Orders by years')
    plt.xlabel('Years')
    plt.ylabel('Number of Orders')
    plt.savefig(charts_path / 'orders_by_years_bar.png')
    charts_paths['orders_by_years_bar'] = charts_path / 'orders_by_years_bar.png'

    #Sales by months 2018 year
    plt.figure(figsize=(12, 6))
    df_2018 = df.loc[df['Order_year'] == 2018]
    df_2018 = df_2018.groupby('Order_month')['Sales'].sum()
    plt.bar(df_2018.index, df_2018.values,
            color='#CCCCFF', edgecolor='#9966CC')
    plt.xticks(df_2018.index[::1], rotation=-45)
    plt.title('Sales by months (2018)')
    plt.xlabel('Months')
    plt.ylabel('Sales by months')
    plt.savefig(charts_path / 'sales_by_months_line.png')
    charts_paths['sales_by_months_line'] = charts_path / 'sales_by_months_line.png'

