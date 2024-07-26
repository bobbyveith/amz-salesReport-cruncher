import pandas as pd



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

    
    return sku_df


if __name__ == "__main__":
    print("[X] Warning: This module is not meant to be run directly!")