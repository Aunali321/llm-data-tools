"""
File Format Converter

Converts between CSV, JSONL, and Parquet formats.

Usage: python convert_file_format.py <input_file> <output_file> <conversion_type>

Input:
- input_file: Path to the input file (CSV, JSONL, or Parquet)
- output_file: Path to save the converted file (CSV, JSONL, or Parquet)
- conversion_type: Type of conversion ('csv_to_jsonl', 'parquet_to_jsonl', 'jsonl_to_parquet', 'jsonl_to_csv')

Example:
python convert_file_format.py input.csv output.jsonl csv_to_jsonl
python convert_file_format.py input.parquet output.jsonl parquet_to_jsonl
python convert_file_format.py input.jsonl output.parquet jsonl_to_parquet
python convert_file_format.py input.jsonl output.csv jsonl_to_csv

Input CSV Example:
column1,column2
value1,value2

Output JSONL Example:
{"column1": "value1", "column2": "value2"}

Input JSONL Example:
{"column1": "value1", "column2": "value2"}

Output Parquet Example:
(Parquet file content)

Output CSV Example:
column1,column2
value1,value2
"""

import pandas as pd
import json
from pathlib import Path
import numpy as np
import argparse

def numpy_to_python(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    return obj

def csv_to_jsonl(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Open the output file in write mode
    with open(output_file, 'w') as f:
        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            # Convert the row to a dictionary, handling NumPy types
            row_dict = {k: numpy_to_python(v)
                        for k, v in row.to_dict().items()}
            # Convert to JSON string
            json_str = json.dumps(row_dict)
            # Write the JSON string to the file, followed by a newline
            f.write(json_str + '\n')

    print(f"Conversion complete. JSONL file saved as {output_file}")

def parquet_to_jsonl(input_file, output_file):
    # Read the Parquet file
    df = pd.read_parquet(input_file)

    # Open the output file in write mode
    with open(output_file, 'w') as f:
        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            # Convert the row to a dictionary, handling NumPy types
            row_dict = {k: numpy_to_python(v)
                        for k, v in row.to_dict().items()}
            # Convert to JSON string
            json_str = json.dumps(row_dict)
            # Write the JSON string to the file, followed by a newline
            f.write(json_str + '\n')

    print(f"Conversion complete. JSONL file saved as {output_file}")

def jsonl_to_parquet(input_file, output_file):
    # Read the JSONL file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Convert each line to a dictionary
    data = [json.loads(line) for line in lines]

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame to a Parquet file
    df.to_parquet(output_file, index=False)

    print(f"Conversion complete. Parquet file saved as {output_file}")

def jsonl_to_csv(input_file, output_file):
    # Read the JSONL file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Convert each line to a dictionary
    data = [json.loads(line) for line in lines]

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame to a CSV file
    df.to_csv(output_file, index=False)

    print(f"Conversion complete. CSV file saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert between CSV, JSONL, and Parquet formats")
    parser.add_argument(
        "input_file", help="Path to input file (CSV, JSONL, or Parquet)")
    parser.add_argument(
        "output_file", help="Path to save the converted file (CSV, JSONL, or Parquet)")
    parser.add_argument(
        "conversion_type", choices=['csv_to_jsonl', 'parquet_to_jsonl', 'jsonl_to_parquet', 'jsonl_to_csv'], help="Type of conversion")
    args = parser.parse_args()

    if args.conversion_type == 'csv_to_jsonl':
        csv_to_jsonl(args.input_file, args.output_file)
    elif args.conversion_type == 'parquet_to_jsonl':
        parquet_to_jsonl(args.input_file, args.output_file)
    elif args.conversion_type == 'jsonl_to_parquet':
        jsonl_to_parquet(args.input_file, args.output_file)
    elif args.conversion_type == 'jsonl_to_csv':
        jsonl_to_csv(args.input_file, args.output_file)
