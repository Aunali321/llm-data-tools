"""
JSONL Validator

Validates a JSONL file to ensure each line contains valid JSON and that the 'messages' field is a list.

Usage: python validate_jsonl.py <input_file>

Input:
- input_file: Path to the input JSONL file

Example:
python validate_jsonl.py augmented_train_data.jsonl

Input JSONL Example:
{"messages": [{"content": "You are a helpful assistant.", "role": "system"}, {"content": "Hello", "role": "user"}, {"content": "Hi there!", "role": "assistant"}]}

Output:
Warning: Empty line at line 2
Error in line 3: 'messages' is not a list
Content: {"messages": "invalid"}
---
"""

import json
import argparse

def validate_jsonl(file_path):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                print(f"Warning: Empty line at line {line_number}")
                continue
            try:
                data = json.loads(line)
                if not isinstance(data.get('messages', {}).get('messages'), list):
                    print(f"Error in line {line_number}: 'messages' is not a list")
                    print(f"Content: {line}")
                    print("---")
            except json.JSONDecodeError as e:
                print(f"JSON decode error in line {line_number}: {e}")
                print(f"Content: {line}")
                print("---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate JSONL file")
    parser.add_argument(
        "input_file", help="Path to input JSONL file")
    args = parser.parse_args()

    validate_jsonl(args.input_file)