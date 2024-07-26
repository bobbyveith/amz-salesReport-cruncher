import pandas as pd
from classes import Product
from dataclasses import asdict
from typing import List
import csv #TODO delte this


TEST_MODE = True
#Ingest AMZ Report CSV & convert to dataframe
if TEST_MODE:
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



def render_sales_df(sales_report):
    # Report containing all sales data
    sales_df = pd.read_csv(sales_report)
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
    return sales_df



def render_sku_df(all_listings_report):
    # Get Product Listing Data and Drop unwanted columns
    sku_df = pd.read_csv(all_listings_report, delimiter='\t')
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
    
    return sku_df


sales_df = render_sales_df(AMAZON_REPORT)
sku_df = render_sku_df(ALL_LISTINGS_REPORT)

# Combine data from sales_df and sku_df based on child ASIN
full_df = pd.merge(sales_df, sku_df, on="(Child) ASIN", how='outer')


# Render a csv for working review
if TEST_MODE:
    full_df.to_csv("./full.csv", index=False)


# ============= TRANSFORMATION LOGIC ====================

def row_to_product_object(row) -> Product:
    
    def filter_product(row):

        target_sku_prefixes = {
            'F1' : None,
            'F2' : None,
            'F3' : None,
            'T1' : None,
            'T2' : None,
            'T3' : None,
            'O1' : None,
            'O2' : None,
            'O3' : None,
            'O4' : None,
            'P1' : None,
            'P2' : None,
            'P3' : None,
            'P9' : None,
        }
        units_sold = row.get('Units Sold')
        seller_sku = row.get('seller-sku')

        # Dropping records that fail criteria
        if pd.isna(units_sold) or units_sold == 0.0 or seller_sku[:2] not in target_sku_prefixes.keys():
            return True
        return False
    
    
    def get_sku(sku):
        '''
        Drops FBA from sku name if applicable
        '''
        if sku.startswith('FBA-'):
            sku = sku.replace('FBA-', '')
        return sku

    # Check for the criteria to exclude certain records
    if filter_product(row):
        return None
    
    product_object =  Product(
        parent_asin=row.get('(Parent) ASIN'),
        child_asin=row.get('(Child) ASIN'),
        units_sold=row.get(('Units Sold')),
        total_sales=row.get(('Total Sales')),
        sku=get_sku(row.get('seller-sku')),
        title=row.get('Title'),
        is_fba=True if row.get('is_fba') == "AMAZON_NA" else False,
        is_active=True if row.get('status') == "Active" else False
        )
    
    # Prefix and Suffix get derived from sku and set into the object
    prefix, suffix = product_object.sku.split('-', 1)
    product_object.prefix = prefix
    product_object.suffix = suffix
        
    return product_object

def generate_list_or_product_objects(full_df):
    # Initialize an empty list to store Product objects
    product_list = []

    # Iterate through the DataFrame rows
    for _, row in full_df.iterrows():
        product = row_to_product_object(row)
        if product is not None:
            product_list.append(product)

    return product_list

product_list = generate_list_or_product_objects(full_df)

def reduce_likeable_data(product_list: List[Product]) -> List[dict]:
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
    return seen_products


# Convert Product objects to dictionaries
reduced_data = reduce_likeable_data(product_list)
product_dicts = list(reduced_data.values())

def create_testing_output():
    # Get the header from the keys of the first product dictionary
    header = product_dicts[0].keys()

    # Write the product dictionaries to a CSV file
    with open('products.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(product_dicts)
