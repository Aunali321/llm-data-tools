"""
JSONL Dataset Transformer

Transforms a JSONL dataset by processing conversations and saving the transformed dataset in Parquet and JSONL formats.

Usage: python transform_dataset.py <input_file>

Input: Path to the input JSONL file

Example:
python transform_dataset.py augmented_train_data.jsonl

Input JSONL Example:
{"conv_id": "1", "messages": {"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]}}

Output JSONL Example:
{"messages": [{"content": "You are a helpful assistant.", "role": "system"}, {"content": "Hello", "role": "user"}, {"content": "Hi there!", "role": "assistant"}]}
"""

import json
from datasets import Dataset
from typing import Dict, Any, List
import logging
from tqdm import tqdm
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def safe_load_json(file_path: str) -> List[Dict[str, Any]]:
    data = []
    with open(file_path, 'r') as f:
        for i, line in enumerate(tqdm(f, desc="Loading JSON")):
            try:
                item = json.loads(line)
                # Convert all values to strings to ensure consistency
                item = {k: json.dumps(v) for k, v in item.items()}
                data.append(item)
            except json.JSONDecodeError:
                logging.warning(f"Skipping row {i+1}: Invalid JSON")
    return data

def transform_conversation(example: Dict[str, str]) -> Dict[str, List[Dict[str, str]]]:
    try:
        conv_id = example['conv_id']

        messages = json.loads(example['messages'])['messages']
        conversations = []

        # Add the system message first (if present)
        system_message = next(
            (msg for msg in messages if msg['role'] == 'system'), None)
        if system_message:
            conversations.append({
                "content": system_message['content'],
                "role": "system"
            })
            logging.debug("Added system message")

        # Add the rest of the messages
        for msg in messages:
            if msg['role'] != 'system':
                conversations.append({
                    "content": msg['content'],
                    "role": msg['role']
                })

        logging.debug(f"Processed {len(conversations)} messages")
        return {"messages": conversations}
    except Exception as e:
        logging.error(f"Error processing conversation {conv_id}: {str(e)}")
        return {"messages": []}

def main(input_file: str):
    logging.info(f"Starting transformation of {input_file}")

    # Load the dataset using our custom function
    try:
        data = safe_load_json(input_file)
        dataset = Dataset.from_list(data)
        logging.info(
            f"Successfully loaded dataset with {len(dataset)} examples")
    except Exception as e:
        logging.error(f"Failed to load dataset: {str(e)}")
        return

    # Transform the dataset
    try:
        transformed_dataset = dataset.map(
            transform_conversation,
            remove_columns=dataset.column_names
        )
        logging.info(f"Successfully transformed dataset")
    except Exception as e:
        logging.error(f"Failed to transform dataset: {str(e)}")
        return

    # Save the transformed dataset as parquet
    output_parquet = input_file.replace('.jsonl', '.parquet')
    try:
        transformed_dataset.to_parquet(output_parquet)
        logging.info(f"Saved transformed dataset as parquet: {output_parquet}")
    except Exception as e:
        logging.error(f"Failed to save parquet file: {str(e)}")

    # Save the transformed dataset as jsonl
    output_jsonl = input_file.replace('.jsonl', '_transformed.jsonl')
    try:
        transformed_dataset.to_json(output_jsonl)
        logging.info(f"Saved transformed dataset as JSONL: {output_jsonl}")
    except Exception as e:
        logging.error(f"Failed to save JSONL file: {str(e)}")

    logging.info("Transformation complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform JSONL dataset")
    parser.add_argument(
        "input_file", help="Path to input JSONL file")
    args = parser.parse_args()

    main(args.input_file)
