import csv


def create_testing_output(product_dicts):
    # Get the header from the keys of the first product dictionary
    header = product_dicts[0].keys()

    # Write the product dictionaries to a CSV file
    with open('./test_outputs/products.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(product_dicts)


if __name__ == "__main__":
    print("[X] Warning: This module is not meant to be run directly!")