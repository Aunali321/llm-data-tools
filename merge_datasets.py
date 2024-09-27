"""
Dataset Merger

Merges multiple datasets from Hugging Face into a single DataFrame and saves it as a Parquet file.

Usage: python merge_datasets.py <dataset_names> <output_file> [--rename_columns <rename_columns>] [--drop_columns <drop_columns>]

Input:
- dataset_names: Comma-separated list of Hugging Face dataset names
- output_file: Path to save the merged dataset as a Parquet file
- rename_columns: Optional JSON string to rename columns (e.g., '{"old_name": "new_name"}')
- drop_columns: Optional comma-separated list of columns to drop

Example:
python merge_datasets.py 'Norquinal/claude_multi_instruct_1k,Norquinal/claude_evol_instruct_100k,flozi00/reflection-llama3.1-70b-alpaca-170924' instruct.parquet --rename_columns '{"input": "instruction"}' --drop_columns 'system,reflection'
"""

import pandas as pd
from datasets import load_dataset
import argparse
import json

def merge_datasets(dataset_names, rename_columns=None, drop_columns=None):
    combined_df = pd.DataFrame()

    for dataset_name in dataset_names:
        # Load the dataset
        dataset = load_dataset(dataset_name, cache_dir='.')

        # Convert to pandas DataFrame
        df = dataset['train'].to_pandas()

        # Rename columns if specified
        if rename_columns:
            df = df.rename(columns=rename_columns)

        # Drop columns if specified
        if drop_columns:
            df = df.drop(columns=drop_columns, errors='ignore')

        # Concatenate with the combined DataFrame
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge datasets from Hugging Face")
    parser.add_argument(
        "dataset_names", help="Comma-separated list of Hugging Face dataset names")
    parser.add_argument(
        "output_file", help="Path to save the merged dataset as a Parquet file")
    parser.add_argument(
        "--rename_columns", type=str, help="JSON string to rename columns (e.g., '{\"old_name\": \"new_name\"}')")
    parser.add_argument(
        "--drop_columns", type=str, help="Comma-separated list of columns to drop")
    args = parser.parse_args()

    dataset_names = args.dataset_names.split(',')
    rename_columns = json.loads(args.rename_columns) if args.rename_columns else None
    drop_columns = args.drop_columns.split(',') if args.drop_columns else None

    result = merge_datasets(dataset_names, rename_columns=rename_columns, drop_columns=drop_columns)

    # Save the result to a parquet file
    result.to_parquet(args.output_file, index=False)
    print(f"Merged dataset saved to {args.output_file}")
