"""
JSONL Processor

Processes a JSONL file by removing the last message if it is from the user.

Usage: python process_jsonl_file.py <input_file> <output_file>

Input:
- input_file: Path to the input JSONL file
- output_file: Path to save the processed JSONL file

Example:
python process_jsonl_file.py augmented_conversations_hf.jsonl augmented_conversations_hf_modified.jsonl

Input JSONL Example:
{"messages": [{"content": "You are a helpful assistant.", "role": "system"}, {"content": "Hello", "role": "user"}, {"content": "Hi there!", "role": "assistant"}, {"content": "Another message", "role": "user"}]}

Output JSONL Example:
{"messages": [{"content": "You are a helpful assistant.", "role": "system"}, {"content": "Hello", "role": "user"}, {"content": "Hi there!", "role": "assistant"}]}
"""

import json
import argparse

def process_jsonl_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            data = json.loads(line.strip())
            messages = data.get('messages', [])

            # Remove the last message if it's from the user
            if messages and messages[-1]['role'] == 'user':
                messages.pop()

            # Update the messages in the data
            data['messages'] = messages

            # Write the modified data to the output file
            json.dump(data, outfile)
            outfile.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSONL file by removing the last user message")
    parser.add_argument(
        "input_file", help="Path to input JSONL file")
    parser.add_argument(
        "output_file", help="Path to save the processed JSONL file")
    args = parser.parse_args()

    process_jsonl_file(args.input_file, args.output_file)
