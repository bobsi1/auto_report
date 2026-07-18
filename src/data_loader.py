import pandas as pd
def load_data(path):
    df = pd.read_csv(path)
    return df

def data_preprocessing(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
    df['Postal Code'] = df['Postal Code'].astype(str).replace('.0', '', regex=False)
    df['shipping_time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Order_month'], df['Order_day'], df['Order_year'], df['Order_weekday'] = df['Order Date'].dt.month, df[
        'Order Date'].dt.day, df['Order Date'].dt.year, df['Order Date'].dt.weekday
    df['Order year_month'] = df['Order_year'].astype(str) + '-' + df['Order_month'].astype(str)
    df['Order year_month'] = pd.to_datetime(df['Order year_month'], format='%Y-%m')
    df['Ship_month'], df['Ship_day'], df['Ship_year'] = df['Ship Date'].dt.month, df['Ship Date'].dt.day, df[
        'Ship Date'].dt.year
    df['Postal Code'] = df['Postal Code'].fillna('05401')
    return df