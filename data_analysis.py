import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

def analyze_data(file_path='SalesPrediction/output/all_data_master.csv'):
    df = pd.read_csv(file_path)
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Best month for sales
    months_sales = df.groupby('month').sum().sort_values('total_sales', ascending=False)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    months_sales.index = pd.CategoricalIndex(months_sales.index, categories=months, ordered=True)
    months_sales = months_sales.sort_index()

    plt.figure(figsize=(10, 6))
    plt.bar(months, months_sales['total_sales'], width=0.5, color='g')
    plt.xticks(months, rotation='vertical')
    plt.xlabel("Months", color='darkblue', size=10)
    plt.ylabel("Sales ($)", color='darkblue', size=10)
    plt.title("Months' Sales in USD", color='darkred', size=12)
    plt.savefig("SalesPrediction/output/01_months_sales.png", bbox_inches='tight', dpi=300)
    plt.show()

    # City with most sales
    city_sales = df.groupby('city').sum()
    cities = city_sales.index.tolist()

    plt.figure(figsize=(10, 6))
    plt.bar(cities, city_sales['total_sales'], width=0.5)
    plt.xticks(cities, rotation='vertical', size=8)
    plt.xlabel("Cities", color='darkblue', size=10)
    plt.ylabel("Sales ($)", color='darkblue', size=10)
    plt.title("Cities' Sales in USD", color='darkred', size=12)
    plt.savefig("SalesPrediction/output/02_city_sales.png", bbox_inches='tight', dpi=300)
    plt.show()

    # Best time to advertise
    hour_sales = df.groupby('hour').sum()
    hours = hour_sales.index.tolist()

    plt.figure(figsize=(10, 6))
    plt.plot(hours, hour_sales['total_sales'], 'g.-')
    plt.xticks(hours, size=8)
    plt.xlabel("Hours of day", color='darkblue', size=10)
    plt.ylabel("Sales ($)", color='darkblue', size=10)
    plt.title("Sales over day's hours", color='darkred', size=12)
    plt.savefig("SalesPrediction/output/03_hour_sales.png", bbox_inches='tight', dpi=300)
    plt.show()

    # Products often sold together
    df_same_id = df[df['order_id'].duplicated(keep=False)]
    df_same_id['all_products'] = df_same_id.groupby('order_id')['product'].transform(lambda x: ', '.join(x))
    df_same_id.drop_duplicates('order_id', inplace=True)
    df_same_id = df_same_id[['order_id', 'all_products']]

    count = Counter()

    for row in df_same_id['all_products']:
        row_list = row.split(', ')
        count.update(Counter(combinations(row_list, 2)))

    for key, value in count.most_common(5):
        print(key, value)

    # Most sold product
    product_group = df.groupby('product')
    products = product_group.sum().index.tolist()

    plt.figure(figsize=(10, 6))
    plt.bar(products, product_group.sum()['quantity_ordered'])
    plt.xticks(products, rotation='vertical', size=8)
    plt.xlabel("Product name", color='darkblue', size=10)
    plt.ylabel("Quantity", color='darkblue', size=10)
    plt.title("Most sold products", color='darkred', size=12)
    plt.savefig("SalesPrediction/output/04_most_product.png", bbox_inches='tight', dpi=300)
    plt.show()

    prices = df.groupby('product').mean()['price_each']
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    ax1.bar(products, product_group.sum()['quantity_ordered'], alpha=0.75)
    ax2.plot(products, prices, 'r--')

    ax1.set_xlabel('Product name', size=10)
    ax1.set_ylabel('Quantity', color='b', size=10)
    ax2.set_ylabel('Price ($)', color='r', size=10)
    ax1.set_xticklabels(products, rotation='vertical', size=8)
    plt.title("Most sold products with price", color='darkred', size=12)
    plt.savefig("SalesPrediction/output/05_most_product_price.png", bbox_inches='tight', dpi=300)
    plt.show()

if __name__ == "__main__":
    analyze_data()
