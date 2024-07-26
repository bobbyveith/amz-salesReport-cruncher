from typing import List, Dict, Tuple
import pandas as pd


# CreateSales by Prefix

def aggregate_sales_data(product_list: List[Dict]) -> Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, float]]]:
    """
    This function aggregates sales data from a list of Product objects into two dictionaries:
    one for sales data grouped by SKU prefix and one for sales data grouped by SKU suffix.

    Parameters:
    product_list (List[Product]): A list of Product objects.

    Returns:
    Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, float]]]:
        - sales_by_prefix: A dictionary where keys are SKU prefixes and values are dictionaries
            containing aggregated 'Units Sold' and 'Total Sales'.
        - sales_by_suffix: A dictionary where keys are SKU suffixes and values are dictionaries
            containing aggregated 'Units Sold', 'Total Sales', 'Aspect Ratio', and 'Product Name'.
    """
    sales_by_prefix: Dict[str, Dict[str, float]] = {}
    sales_by_suffix: Dict[str, Dict[str, float]] = {}

    for product in product_list:
        if product.prefix not in sales_by_prefix:
            sales_by_prefix[product.prefix] = {
                'Units Sold': product.units_sold,
                'Total Sales': product.total_sales
            }
        else:
            sales_by_prefix[product.prefix]['Units Sold'] += product.units_sold
            sales_by_prefix[product.prefix]['Total Sales'] += product.total_sales

        if product.suffix not in sales_by_suffix:
            sales_by_suffix[product.suffix] = {
                'Aspect Ratio': product.aspect_ratio,
                'Product Name': product.title,
                'Units Sold': product.units_sold,
                'Total Sales': product.total_sales
            }
        else:
            sales_by_suffix[product.suffix]['Units Sold'] += product.units_sold
            sales_by_suffix[product.suffix]['Total Sales'] += product.total_sales

    return sales_by_prefix, sales_by_suffix




# Load Prefix and Suffix sheets into one xlsx file

def write_dicts_to_xlsx(data: Tuple[Dict, Dict]):
    """
    Writes two dictionaries to an xlsx file where each dictionary is written to its own sheet.

    Parameters:
    data (Tuple[Dict, Dict]): A tuple containing two dictionaries.
    filename (str): The name of the output xlsx file.
    """
    sales_by_prefix, sales_by_suffix = data
    filename = './prod_output/sales_data.xlsx'

    # Create a Pandas Excel writer using Openpyxl as the engine
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Convert the dictionaries to DataFrames
        df_prefix = pd.DataFrame.from_dict(sales_by_prefix, orient='index')
        df_suffix = pd.DataFrame.from_dict(sales_by_suffix, orient='index')

        # Write the DataFrames to separate sheets
        df_prefix.to_excel(writer, sheet_name='Sales by Prefix')
        df_suffix.to_excel(writer, sheet_name='Sales by Suffix')


def render_sales_data(product_list, TEST_MODE):
    aggrigated_data = aggregate_sales_data(product_list)
    write_dicts_to_xlsx(aggrigated_data)

    if TEST_MODE:
        return True
    raise RuntimeError("[X] Warning: System run on dev mode")
    
        
    
