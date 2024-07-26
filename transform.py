from classes import Product
from typing import List
from dataclasses import asdict
import pandas as pd

# Local Modules
import utils



def combine_data(TEST_MODE, sales_df, sku_df):
    # Combine data from sales_df and sku_df based on child ASIN
    full_df = pd.merge(sales_df, sku_df, on="(Child) ASIN", how='outer')

    if TEST_MODE:
        full_df.to_csv("./test_outputs/full.csv", index=False)

    return full_df



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
    
    def get_aspect_ratio(sku):

        aspect_ratio_mapping = {
            'F1': '4x3',
            'F2': '4x3',
            'F3': '4x3',
            'T1': '2x3',
            'T2': '2x3',
            'T3': '2x3',
            'O1': '1x1',
            'O2': '1x1',
            'O3': '1x1',
            'O4': '1x1',
            'P1': '4x3',
            'P2': '2x3',
            'P3': '1x1',
            'P9': '4x3'
        }

        sku_head = sku[:2]

        if sku_head in aspect_ratio_mapping:
            aspect_ratio = aspect_ratio_mapping[sku_head]
        else:
            aspect_ratio = None

        return aspect_ratio

    # Check for the criteria to exclude certain records
    if filter_product(row):
        return None
    
    product_object =  Product(
        parent_asin=row.get('(Parent) ASIN'),
        child_asin=row.get('(Child) ASIN'),
        units_sold=int(row.get(('Units Sold'))),
        total_sales=row.get(('Total Sales')),
        sku=get_sku(row.get('seller-sku')),
        title=row.get('Title'),
        aspect_ratio=None,
        is_fba=True if row.get('is_fba') == "AMAZON_NA" else False,
        is_active=True if row.get('status') == "Active" else False
        )
    
    # Prefix and Suffix get derived from sku and set into the object
    prefix, suffix = product_object.sku.split('-', 1)
    product_object.prefix = prefix
    product_object.suffix = suffix
    product_object.aspect_ratio = get_aspect_ratio(product_object.sku)
        
    return product_object




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

    return seen_products




def generate_list_of_product_objects(full_df):
    # Initialize an empty list to store Product objects
    product_list = []

    # Iterate through the DataFrame rows
    for _, row in full_df.iterrows():
        product = row_to_product_object(row)
        if product is not None:
            product_list.append(product)

    #reduced_product_list = reduce_likeable_data(product_list)

    return product_list




def list_products(full_df, TEST_MODE):
    # Convert Product objects to dictionaries
    list_of_products = generate_list_of_product_objects(full_df)

    if TEST_MODE:   
        # Convert list of Product objects to list of dictionaries
        product_dicts = [asdict(product) for product in list_of_products]
        utils.create_testing_output(product_dicts)

    return list_of_products

if __name__ == "__main__":
    print("[X] Warning: This module is not meant to be run directly!")