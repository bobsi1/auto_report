import pandas as pd

def get_growth_word(diff):
    if diff > 0:
        return 'increased'
    elif diff < 0:
        return 'decreased'
    else:
        return 'not changed'

def get_diff(data):
    return (data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100

def create_overview_text(df):
    texts = {}

    #Orders by months chart's text
    orders_by_year_month = df.groupby('Order year_month')['Order ID'].nunique()
    max_order = orders_by_year_month.max()
    max_month = orders_by_year_month.idxmax()
    min_order = orders_by_year_month.min()
    min_month = orders_by_year_month.idxmin()
    diff = get_diff(orders_by_year_month)
    growth_flag = get_growth_word(diff)
    orders_by_year_month_title = "Orders by months by all analyzed years"
    orders_by_year_month_text = (f"Total number of orders {growth_flag} by {abs(diff):.2f}% between the first and the last month of the analyzed period.\n"
                                 f"The peak was observed in {max_month} with {max_order} orders.\n"
                                 f"Minimum was reached in {min_month} with {min_order} orders.\n")
    texts['orders_by_months_line'] = {
        'title' : orders_by_year_month_title,
        'text' : orders_by_year_month_text
    }

    #Orders by years chart's text
    orders_by_year = df.groupby('Order_year')['Order ID'].nunique()
    max_order = orders_by_year.max()
    max_year = orders_by_year.idxmax()
    diff = get_diff(orders_by_year)
    growth_flag = get_growth_word(diff)
    orders_by_year_title = "Orders by all analyzed years"
    orders_by_year_text = (f"Total number of orders {growth_flag} by {abs(diff):.2f}% between the first and the last year of the analyzed period.\n"
                                 f"The highest number of orders was recorded in {max_year} with {max_order} orders.\n")
    texts['orders_by_years_bar'] = {
        'title' : orders_by_year_title,
        'text' : orders_by_year_text
    }

    #Sales by months 2018 year chart's text
    df_2018 = df.loc[df['Order_year'] == 2018]
    df_2018 = df_2018.groupby('Order_month')['Sales'].sum()
    max_sales = df_2018.max()
    max_month = df_2018.idxmax()
    min_sales = df_2018.min()
    min_month = df_2018.idxmin()
    mean_sales = df_2018.mean()
    diff = get_diff(df_2018)
    growth_flag = get_growth_word(diff)
    months = {
        1 : 'January',
        2 : 'February',
        3 : 'March',
        4 : 'April',
        5 : 'May',
        6 : 'June',
        7 : 'July',
        8 : 'August',
        9 : 'September',
        10 : 'October',
        11 : 'November',
        12 : 'December'
    }
    sales_by_months_title = "Sales by months in 2018"
    sales_by_months_text = (
        f"Total sales {growth_flag} by {abs(diff):.2f}% between the first and the last month of the year.\n"
        f"Average sales over the year was {mean_sales:.2f}\n"
        f"The highest sales were recorded in {months[max_month]} with {max_sales} orders, while {months[min_month]} showed the lowest sales - {min_sales}\n")
    texts['sales_by_months_line'] = {
        'title': sales_by_months_title,
        'text': sales_by_months_text
    }
    return texts

def create_sales_structure_texts(df, texts):
    #Categories and Sub-categories pie
    sales_categories = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    biggest_category = sales_categories.idxmax()
    biggest_category_size = sales_categories.max()

    sales_subs_biggest_category = df.loc[df['Category'] == biggest_category].groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False)
    biggest_subcategory = sales_subs_biggest_category.idxmax()
    biggest_subcategory_size = sales_subs_biggest_category.max()

    sub_of_cat_percent = (biggest_subcategory_size / biggest_category_size) * 100

    cats_and_subs_title = "Categories & Sub-Categories"
    cats_and_subs_text = (f"The biggest category is {biggest_category} with {biggest_category_size} sales.\n"
                          f"Within this category,  {biggest_subcategory} is the biggest sub-category with {biggest_subcategory_size}, representing the {sub_of_cat_percent:.2f}% of category\n")
    texts['cats_subcats_pie'] = {
        'title': cats_and_subs_title,
        'text': cats_and_subs_text
    }

    #Line and bar categories chart
    df_cats_ym = df.groupby(['Order year_month', 'Category'])['Order ID'].nunique().unstack()

    cols = df_cats_ym.columns
    maxs = {}
    for col in cols:
        max_col = df_cats_ym[col].idxmax()
        max_col_size = df_cats_ym[col].max()
        maxs[col] = {'max_date' : max_col, 'max_size' : max_col_size}

    maxs_text = ""
    for category, size in maxs.items():
        maxs_text += (
            f"{category}: {size['max_size']} orders in {size['max_date'].strftime('%B %Y')}\n"
        )

    diffs = {}
    all_diff = ''
    for col in cols:
        diff = get_diff(df_cats_ym[col])
        diffs[col] = diff
    if all(value >= 0 for value in diffs.values()):
        all_diff = 'positive'
    elif all(value < 0 for value in diffs.values()):
        all_diff = 'negative'
    else:
        all_diff = 'neutral'

    line_and_bar_cats_title = 'Categories & Categories dynamic'
    line_and_bar_cats_text = (f"Dynamic of sales by categories can be named {all_diff}\n"
                              f"Each category peak:\n"
                              f"{maxs_text}")
    texts['categories_lines_bar'] = {
        'title': line_and_bar_cats_title,
        'text': line_and_bar_cats_text
    }

    #Top-Products
    df_by_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False)
    max_product = df_by_products.idxmax()
    max_product_size = df_by_products.max()
    max_product_percent = (max_product_size / df_by_products.sum()) * 100
    top_product_percent = (df_by_products.head(10).sum / df_by_products.sum()) * 100
    top_subs_products_title = 'Top Sub-Categories and products by Sales'
    top_subs_products_text = (f"The ten best-selling products accounted for {top_product_percent}% of all sales.\n"
                              f"The biggest product by sales is {max_product} with {max_product_size}, which is {max_product_percent} of all Sales.")
    texts['top_subs'] = {
        'title': top_subs_products_title,
        'text': top_subs_products_text
    }
    return texts

def create_customers_texts(df, texts):

    # Orders and Sales by Ship Mode
    df_by_ship_mode = df.groupby('Ship Mode').agg({'Order ID' : 'nunique', 'Sales' : 'sum'})
    max_mode = df_by_ship_mode['Order ID'].idxmax()
    max_mode_orders = df_by_ship_mode['Order ID'].max()
    max_mode_sales = df_by_ship_mode.loc[max_mode, 'Sales']

    min_mode = df_by_ship_mode['Order ID'].idxmin()
    min_mode_orders = df_by_ship_mode['Order ID'].min()
    min_mode_sales = df_by_ship_mode.loc[min_mode, 'Sales']
    ship_mode_bars_title = 'Sales and Orders by Ship Mode'
    ship_mode_bars_text = (f"The most frequently used shipping mode was {max_mode} ({max_mode_orders} orders - {max_mode_sales} sales).\n"
                 f"The least frequently used shipping mode was {min_mode} ({min_mode_orders} orders - {min_mode_sales} sales).")
    texts['ship_mode_bars'] = {
        'title' : ship_mode_bars_title,
        'text': ship_mode_bars_text
    }




