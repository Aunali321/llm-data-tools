"""
JSONL Message Order Checker

Checks the order of messages in a JSONL dataset and logs specific patterns.

Usage: python check_message_order.py <input_file>

Input: Path to the input JSONL file

Example:
python check_message_order.py persona-based-chat-messages-1k-augmented-cleaned.jsonl

Input JSONL Example:
{"messages": [{"content": "...", "role": "system"}, {"content": "...", "role": "user"}, {"content": ".....", "role": "assistant"}, {"content": "...", "role": "user"}, {"content": "....", "role": "assistant"}, {"content": "....", "role": "assistant"}]}

Output:
Row 682, Index 4: Assistant message followed by another assistant message and then user message.
"""

import json
import argparse

def check_message_order(input_file: str):
    # Load the JSONL data
    with open(input_file, 'r') as f:
        data = [json.loads(line) for line in f]

    # Iterate through the data
    for i, row in enumerate(data):
        messages = row['messages']

        # Iterate through the messages
        for j in range(len(messages) - 2):
            # Check if the order is Assistant -> Assistant -> User
            if messages[j]['role'] == 'assistant' and messages[j+1]['role'] == 'assistant' and messages[j+2]['role'] == 'user':
                print(
                    f"Row {i+1}, Index {j}: Assistant message followed by another assistant message and then user message.")
            # Check if the order is Assistant -> Assistant -> Assistant -> User
            elif messages[j]['role'] == 'assistant' and messages[j+1]['role'] == 'assistant' and messages[j+2]['role'] == 'assistant' and messages[j+3]['role'] == 'user':
                print(
                    f"Row {i+1}, Index {j}: Assistant message followed by two more assistant messages and then user message.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check message order in JSONL dataset")
    parser.add_argument(
        "input_file", help="Path to input JSONL file")
    args = parser.parse_args()

    check_message_order(args.input_file)