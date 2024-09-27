"""
CSV Column Filter

Filters a CSV file to keep only selected columns.

Usage: python filter_csv_columns.py <input_file> <output_file> <columns_to_keep>

Input: Path to the input CSV file
Output: Path to save the filtered CSV file
Columns to Keep: Comma-separated list of columns to keep

Example:
python filter_csv_columns.py input.csv output.csv name,age
"""

import pandas as pd
import argparse

def keep_selected_columns(input_file, output_file, columns_to_keep):
    # Read the input CSV file
    data = pd.read_csv(input_file)

    # Filter the data to keep only the selected columns
    filtered_data = data[columns_to_keep]

    # Write the filtered data to the output CSV file
    filtered_data.to_csv(output_file, index=False)

    print(f"Selected columns have been written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter CSV columns")
    parser.add_argument(
        "input_file", help="Path to input CSV file")
    parser.add_argument(
        "output_file", help="Path to save the filtered CSV file")
    parser.add_argument(
        "columns_to_keep", help="Comma-separated list of columns to keep")
    args = parser.parse_args()

    # Convert the columns_to_keep argument from a string to a list
    columns_to_keep = args.columns_to_keep.split(',')

    keep_selected_columns(args.input_file, args.output_file, columns_to_keep)
