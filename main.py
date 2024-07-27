# Depedencies
import pandas as pd
from typing import List

# Local Modules
import extract, transform, load

# True when testing
TEST_MODE = True
# True if use local test files rather than API Call for data
LOCAL_RUN = True

#Ingest AMZ Report CSV & convert to dataframe
if TEST_MODE or LOCAL_RUN:
    AMAZON_REPORT = "./test_inputs/Sales Report.csv"
    ALL_LISTINGS_REPORT = "./test_inputs/All Listings Report.txt"
else:
    AMAZON_REPORT = input("Enter the path to the Sales Report: ")
    ALL_LISTINGS_REPORT = input("Enter the path to the All Listings Report: ")


def main():

    sales_df = extract.render_sales_df(AMAZON_REPORT)
    sku_df = extract.render_sku_df(ALL_LISTINGS_REPORT)

    # Combine data from sales_df and sku_df based on child ASIN
    full_df = transform.combine_data(TEST_MODE, sales_df=sales_df, sku_df=sku_df)
    # Render a csv for working review

    product_objects: List = transform.list_products(full_df, TEST_MODE)
    success = load.render_sales_data(product_objects, TEST_MODE)

    if success:
        print('Program Ran Successfully!')
    else:
        print("Some Issue Somewhere")

    


if __name__ == "__main__":
    main()
