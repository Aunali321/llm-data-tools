"""
Dataset Conversion Tool

Converts 'conversations' to 'messages' in datasets, supporting local JSONL and Hugging Face formats.

Usage: python convert_dataset.py <input> <output>

Input: Local JSONL file or Hugging Face dataset name
Output: Converted JSONL file

Example: 
# For local file
python convert_dataset.py input.jsonl output.jsonl
# For Hugging Face dataset
python convert_dataset.py username/dataset_name output.jsonl

Before:
{
  "conversations": [
    {"from": "human", "value": "Hello"},
    {"from": "gpt", "value": "Hi there!"}
  ]
}

After:
{
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
  ]
}
"""


import json
import argparse
import os
from datasets import load_dataset


def convert_conversation(conversation):
    role_mapping = {
        "system": "system",
        "human": "user",
        "gpt": "assistant"
    }

    if isinstance(conversation, list):
        return {
            "role": role_mapping.get(conversation[0], conversation[0]),
            "content": conversation[1]
        }
    elif isinstance(conversation, dict):
        return {
            "role": role_mapping.get(conversation.get("from"), conversation.get("from")),
            "content": conversation.get("value")
        }
    else:
        raise ValueError(f"Unexpected conversation format: {conversation}")


def process_dataset(data):
    if isinstance(data, dict):
        if 'conversations' in data:
            data['messages'] = [convert_conversation(
                conv) for conv in data['conversations']]
            del data['conversations']
        else:
            for key, value in data.items():
                data[key] = process_dataset(value)
    elif isinstance(data, list):
        return [process_dataset(item) for item in data]
    return data


def convert_dataset(input_path, output_path):
    if os.path.isfile(input_path):
        # Load local file
        with open(input_path, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f]
    else:
        # Try loading as a Hugging Face dataset
        try:
            dataset = load_dataset(input_path, split="train")
            data = [item for item in dataset]
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return

    converted_data = [process_dataset(item) for item in data]

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the converted data
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in converted_data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

    print(f"Converted dataset saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert dataset format")
    parser.add_argument(
        "input_path", help="Path to input dataset (local file or Hugging Face dataset)")
    parser.add_argument(
        "output_path", help="Path to save the converted dataset")
    args = parser.parse_args()

    convert_dataset(args.input_path, args.output_path)
