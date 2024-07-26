# Depedencies
import pandas as pd
from typing import List

# Local Modules
from extract import render_sales_df, render_sku_df
from transform import list_products, combine_data
from load import render_sales_data
import utils

TEST_MODE = True
# True if use local test files rather than API Call for data
LOCAL_RUN = True
#Ingest AMZ Report CSV & convert to dataframe
if TEST_MODE or LOCAL_RUN:
    AMAZON_REPORT = "./test_inputs/Sales Report.csv"
    ALL_LISTINGS_REPORT = "./test_inputs/All Listings Report.txt"


def main():

    sales_df = render_sales_df(AMAZON_REPORT)
    sku_df = render_sku_df(ALL_LISTINGS_REPORT)

    # Combine data from sales_df and sku_df based on child ASIN
    full_df = combine_data(sales_df=sales_df, sku_df=sku_df)
    # Render a csv for working review

    product_objects: List = list_products(full_df)
    success = render_sales_data(product_objects)
    if success:
        print('Program Ran Successfully!')
    else:
        print("Some Issue Somewhere")


    if TEST_MODE:
        utils.create_testing_output(product_objects)
        full_df.to_csv("./test_outputs/full.csv", index=False)

    


if __name__ == "__main__":
    main()
