# Depedencies
from typing import List

# Local Modules
import extract, transform, load

# True when testing
TEST_MODE = False

def main(sales_report, listings_report):


    sales_df = extract.render_sales_df(sales_report)
    sku_df = extract.render_sku_df(listings_report)

    # Combine data from sales_df and sku_df based on child ASIN
    full_df = transform.combine_data(TEST_MODE, sales_df=sales_df, sku_df=sku_df)
    # Render a csv for working review

    product_objects: List = transform.list_products(full_df, TEST_MODE)
    xlsx_data = load.render_sales_data(product_objects, TEST_MODE)

    return xlsx_data

    


if __name__ == "__main__":
    print("[X] This module is in lambda branch and should not be run directly!")
