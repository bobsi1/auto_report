import matplotlib.pyplot as plt
from pathlib import Path
import plotly.express as px

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
    plt.close()

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
    plt.close()

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
    plt.close()
    return charts_paths

def create_sales_structure_charts(df, charts_paths):
    proj_path = Path.cwd().parent
    charts_path = proj_path / 'charts'

    #Categories and Sub-categories pie
    fig = px.sunburst(df,
                      path=['Category', 'Sub-Category'],
                      values='Sales',
                      color='Category'
                      )
    fig.write_image(charts_path / 'cats_subcats.png')
    charts_paths['cats_subcats_pie'] = charts_path / 'cats_subcats.png'

    #Line and bar categories chart
    df_by_categories = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(15, 3))
    axes[1].bar(df_by_categories.index, df_by_categories.values, color='#CCCCFF', edgecolor='#9966CC')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].set_title("Sales by Category")

    df_cats_ym = df.groupby(['Order year_month', 'Category'])['Order ID'].nunique().unstack()
    df_cats_ym.plot(kind='line',
                                                                                 color=['#CCCCFF', '#9966CC', '#CC99FF',
                                                                                        '#9900CC'],markeredgecolor='#9966CC', markersize=5, marker='o', ax = axes[0])
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].set_title("Number of orders dynamic by Category")
    plt.savefig(charts_path / 'categories_lines_bar.png')
    charts_paths['categories_lines_bar'] = charts_path / 'categories_lines_bar.png'
    plt.close()

    #Top Subcategories chart
    df_by_subs = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    axes[0].bar(df_by_subs.index, df_by_subs.values,color='#CCCCFF', edgecolor='#9966CC')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].set_title('Top-10 Sub-Categories by Sales')

    df_by_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
    axes[1].bar(df_by_products.index, df_by_products.values, color='#CCCCFF', edgecolor='#9966CC')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].set_title('Top-10 Products by Sales')
    plt.tight_layout()
    plt.savefig(charts_path / 'top_subs.png')
    charts_paths['top_subs'] = charts_path / 'top_subs.png'
    plt.close()
    return charts_paths

def create_customers_charts(df, charts_paths):
    proj_path = Path.cwd().parent
    charts_path = proj_path / 'charts'

    #Orders and Sales by Ship Mode
    df_by_ship_mode = df.groupby('Ship Mode')['Order ID'].nunique().sort_values(ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    axes[0].bar(df_by_ship_mode.index, df_by_ship_mode.values, color='#CCCCFF', edgecolor='#9966CC')
    axes[0].set_title("Orders by Ship Mode")

    sales_by_ship_mode = df.groupby('Ship Mode')['Sales'].sum().sort_values(ascending=False)
    axes[1].bar(sales_by_ship_mode.index, sales_by_ship_mode.values, color='#CCCCFF', edgecolor='#9966CC')
    axes[1].set_title("Sales by Ship Mode")
    plt.savefig(charts_path / 'ship_mode_bars.png')
    charts_paths['ship_mode_bars'] = charts_path / 'ship_mode_bars.png'
    plt.close()

    #Orders and Sales by Segment
    df_by_segment = df.groupby('Segment')['Order ID'].nunique().sort_values(ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    axes[0].bar(df_by_segment.index, df_by_segment.values, color='#CCCCFF', edgecolor='#9966CC')
    axes[0].set_title("Orders by Segment")

    sales_by_segment = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)
    axes[1].bar(sales_by_segment.index, sales_by_segment.values, color='#CCCCFF', edgecolor='#9966CC')
    axes[1].set_title("Sales by Segment")
    plt.savefig(charts_path / 'segment_bars.png')
    charts_paths['segment_bars'] = charts_path / 'segment_bars.png'
    plt.close()
    return charts_paths

def geographic_charts(df, charts_paths):
    proj_path = Path.cwd().parent
    charts_path = proj_path / 'charts'

    #Sales and orders by regions
    fig, axes = plt.subplots(1, 3, figsize=(15, 3))
    orders_by_regions = df.groupby('Region')['Order ID'].nunique()
    axes[0].pie(orders_by_regions.values,orders_by_regions.index, colors = ['#CCCCFF','#9966CC', '#CC99FF', '#6600CC'], labeldistance = 0.3, autopct='%1.1f%%', textprops={'fontsize': 9})
    axes[0].set_title("Orders by Region")

    sales_by_regions = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    axes[1].bar(sales_by_regions.index, sales_by_regions.values, color='#CCCCFF', edgecolor='#9966CC')
    axes[1].set_title("Sales by Region")
    plt.savefig(charts_path / 'regions.png')
    charts_paths['regions'] = charts_path / 'regions.png'
    plt.close()

    #Top-10 States
    sales_by_states = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(9, 6))
    plt.bar(sales_by_states.index, sales_by_states.values, color='#CCCCFF', edgecolor='#9966CC')
    plt.title('Sales by States')
    plt.xticks(rotation=45)
    plt.savefig(charts_path / 'states.png')
    charts_paths['states'] = charts_path / 'states.png'
    plt.close()

    # Top-10 States
    sales_by_cities = df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(9, 6))
    plt.bar(sales_by_cities.index, sales_by_cities.values, color='#CCCCFF', edgecolor='#9966CC')
    plt.title('Sales by Cities')
    plt.xticks(rotation=45)
    plt.savefig(charts_path / 'cities.png')
    charts_paths['cities'] = charts_path / 'cities.png'
    plt.close()
    return charts_paths





