import pandas as pd
from classes import Product
from dataclasses import asdict
from typing import List
import csv #TODO delte this

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

# Report containing all sales data
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
    'Total Order Items - B2B', 'Units Ordered', 'Units Ordered - B2B', 'Ordered Product Sales', 'Ordered Product Sales - B2B', '(Parent) ASIN'
]

# Drop unwanted columns
sales_df.drop(columns=columns_to_drop, inplace=True)



# Get Product Listing Data and Drop unwanted columns
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
    def filter_product(row):
        bad_asins = {
                "B0BPJS1WL3": None,
                "B0BPJRX5JZ": None,
                "B09HSNYHV4": None,
                "B09HSNVPZ5": None,
                "B09HSQ37R7": None,
                "B09X1DR2RW": None,
                "B09HSPHG4M": None,
                "B09HSPHWC8": None,
                "B09HSN2ZM3": None,
                "B09HSQL58F": None,
                "B0BPJLXGYV": None,
                "B0BPKRWRCW": None,
                "B0BPJXX3WV": None,
                "B0BPJJLMHK": None,
                "B0BQ19FVHS": None,
                "B0BQ1DMV33": None,
                "B0BQ1YYZF5": None,
                "B08NXZVV47": None,
                "B08NXYKN9W": None,
                "B08NXZXNY1": None,
                "B08NY26NMB": None,
                "B08NY41M7K": None,
                "B0BQ26DD69": None,
                "B0BQRX3RWB": None,
                "B000EIDV7W": None,
                "B00OW8GLRM": None,
                "B0BPJVG893": None,
                "B00OW8GLRM": None,
                "B003HLAX6U": None,
                "B003HLAX6U": None,
                "B000EIDV7W": None,
                "B000GCGB8M": None
            }

        if pd.isna(row.get('Units Sold')) or row.get('Units Sold') == 0.0 or row.get('(Child) ASIN') in bad_asins:
            return True
        return False
    
    def get_modified_sku(sku):
        if sku.startswith('FBA-'):
            sku = sku.replace('FBA-', '')
        return sku

    # Check for the criteria to exclude certain records
    if filter_product(row):
        return None
    
    product_object =  Product(
        parent_asin=row.get('(Parent) ASIN'),
        child_asin=get_modified_sku(row.get('(Child) ASIN')),
        units_sold=row.get(('Units Sold')),
        total_sales=row.get(('Total Sales')),
        sku=row.get('seller-sku'),
        title=row.get('Title'),
        is_fba=True if row.get('is_fba') == "AMAZON_NA" else False,
        is_active=True if row.get('status') == "Active" else False
        )
        
    return product_object

# Convert each row to a Product instance
products = full_df.apply(lambda row: row_to_product(row), axis=1)

# Convert to list of Product objects
product_list = [product for product in products.tolist() if product is not None] 

# Identify SKUs that start with these strings
prefixes = ('F1', 'F2', 'F3', 'T1', 'T2', 'T3', 'O1', 'O2', 'O3', 'O4', 'P1', 'P2', 'P3', 'P9')

# Parse SKU
for product in product_list:
    if product.sku.startswith(prefixes):
        prefix, suffix = product.sku.split('-', 1)
        product.prefix = prefix
        product.suffix = suffix

def create_product_objects(product_list: List[Product]) -> List[dict]:
    # Dictionary of product dicts where objects that have the same ASIN are combined in Units Sold and Total Sales
    seen_products = {}
    for product in product_list:
        if product.child_asin not in seen_products:
            seen_products[product.child_asin] = asdict(product)
        else:
            float_keys = ['units_sold', 'total_sales']
            for key in float_keys:
                seen_products[product.child_asin][key] += asdict(product)[key]

    product_dicts = list(seen_products.values())
    return product_dicts


# Convert Product objects to dictionaries
product_dicts = create_product_objects(product_list)

# Get the header from the keys of the first product dictionary
header = product_dicts[0].keys()

# Write the product dictionaries to a CSV file
with open('products.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    writer.writerows(product_dicts)
