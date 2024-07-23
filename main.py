import pandas as pd
from classes import Product

#Ingest AMZ Report CSV & convert to dataframe
AMAZON_REPORT = "./Sales Report.csv"
ALL_LISTINGS_REPORT = "./All Listings Report.txt"

def convert_to_float(price_str):
    '''
    Convert price strings to floats
    '''
    if isinstance(price_str, str):
        # Remove the '$' sign and convert to float
        return float(price_str.replace('$', '').replace(',', ''))
    elif isinstance(price_str, (int, float)):
        # Directly return the value if it's already numeric
        return float(price_str)
    else:
        # Handle unexpected types (e.g., NaN)
        return 0.0


sales_df = pd.read_csv(AMAZON_REPORT)
# Convert columns to string to ensure proper formatting handling
sales_df['Units Ordered'] = sales_df['Units Ordered'].astype(str)
sales_df['Units Ordered - B2B'] = sales_df['Units Ordered - B2B'].astype(str)
sales_df['Ordered Product Sales'] = sales_df['Ordered Product Sales'].astype(str)
sales_df['Ordered Product Sales - B2B'] = sales_df['Ordered Product Sales - B2B'].astype(str)

# Apply conversion and perform calculations
sales_df['Units Sold'] = (
    sales_df['Units Ordered'].apply(convert_to_float) +
    sales_df['Units Ordered - B2B'].apply(convert_to_float)
)

sales_df['Total Sales'] = (
    sales_df['Ordered Product Sales'].apply(convert_to_float) +
    sales_df['Ordered Product Sales - B2B'].apply(convert_to_float)
)

columns_to_drop = [
    'Sessions - Total', 'Sessions - Total - B2B', 'Session Percentage - Total', 'Session Percentage - Total - B2B', 'Page Views - Total',
    'Page Views - Total - B2B', 'Page Views Percentage - Total', 'Page Views Percentage - Total - B2B', 'Featured Offer (Buy Box) Percentage',
    'Featured Offer (Buy Box) Percentage - B2B', 'Unit Session Percentage', 'Unit Session Percentage - B2B', 'Title', 'Total Order Items',
    'Total Order Items - B2B', 'Units Ordered', 'Units Ordered - B2B', 'Ordered Product Sales', 'Ordered Product Sales - B2B'
]

# Drop unwanted columns
sales_df.drop(columns=columns_to_drop, inplace=True)



# Get Listing Data and Drop unwanted columns
sku_df = pd.read_csv(ALL_LISTINGS_REPORT, delimiter='\t')
# Rename columns to match with sales_df for merge actions
sku_df.rename(columns={'asin1': '(Child) ASIN', 'item-name': 'Title'}, inplace=True)

# Drop unwanted columns
sku_df.drop(columns=['listing-id', 'quantity', 'open-date'], inplace=True)

# Adjust display options for better readability
pd.set_option('display.max_rows', 20)  # Show all rows
pd.set_option('display.max_columns', 5)  # Show all columns
pd.set_option('display.width', 1000)  # Set display width
pd.set_option('display.max_colwidth', 500)  # No limit on column width

#print(sales_df.head())
sku_df.to_csv("./test.csv", index=False)


full_df = pd.merge(sales_df, sku_df, on="(Child) ASIN", how='outer')





full_df.to_csv("./full.csv", index=False)

def row_to_product(row) -> Product:
    return Product(
        parent_asin=row.get('(Parent) ASIN'),
        child_asin=row.get('(Child) ASIN'),
        units_sold=row.get('Units Sold'),
        total_sales=row.get('Total Sales'),
        sku=row.get('seller-sku'),
        title=row.get('fulfillment-channel'),
        is_fba=True if row.get('is_fba') == "AMAZON_NA" else False,
        is_active=True if row.get('status') == "Active" else False
    )

# Convert each row to a Product instance
products = full_df.apply(lambda row: row_to_product(row), axis=1)

# Convert to list of Product objects
product_list = products.tolist()

counter = 0
for product in product_list:
    counter +=1
print(counter)
#Transfrom Data