import pandas as pd

#Ingest AMZ Report CSV & convert to dataframe
AMAZON_REPORT = "./Sales Report.csv"
ALL_LISTINGS_REPORT = "./All Listings Report.txt"

sales_df = pd.read_csv(AMAZON_REPORT)
sales_df.drop('Sessions - Total', axis=1)
sales_df.drop('Sessions - Total - B2B', axis=1)
sales_df.drop('Session Percentage - Total', axis=1)
sales_df.drop('Session Percentage - Total - B2B', axis=1)
sales_df.drop('Page Views - Total', axis=1)
sales_df.drop('Page Views - Total - B2B', axis=1)
sales_df.drop('Page Views Percentage - Total', axis=1)
sales_df.drop('Page Views Percentage - Total - B2B', axis=1)
sales_df.drop('Featured Offer (Buy Box) Percentage', axis=1)
sales_df.drop('Featured Offer (Buy Box) Percentage - B2B', axis=1)
sales_df.drop('Unit Session Percentage', axis=1)
sales_df.drop('Unit Session Percentage - B2B', axis=1)


# Get Listing Data and Drop unwanted columns
sku_df = pd.read_csv(ALL_LISTINGS_REPORT, delimiter='\t')
sku_df.drop('listing-id', axis=1)
sku_df.drop('quantity', axis=1)
sku_df.drop('open-date', axis=1)

# Adjust display options for better readability
pd.set_option('display.max_rows', 20)  # Show all rows
pd.set_option('display.max_columns', 5)  # Show all columns
pd.set_option('display.width', 1000)  # Set display width
pd.set_option('display.max_colwidth', 500)  # No limit on column width

print(sales_df.head())
#sku_df.to_csv("./test.csv", index=False)

#Transfrom Data