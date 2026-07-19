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



