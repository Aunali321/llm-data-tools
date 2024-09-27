"""
JSONL to Text Converter

Converts a JSONL file to a text file with a specific format.

Usage: python convert_jsonl_to_text.py <input_file> <output_file>

Input:
- input_file: Path to the input JSONL file
- output_file: Path to save the converted text file

Example:
python convert_jsonl_to_text.py preferences_kto.jsonl preferences_kto.txt

Input JSONL Example:
{"query": "What is your name?", "response": "I am an AI assistant.", "label": true}

Output Text Example:
Query: What is your name?
Response: I am an AI assistant.
Label: true
"""

import json
import argparse

def convert_jsonl_to_text(input_file, output_file):
    # Open the output file in write mode
    with open(output_file, 'w') as output_file:
        # Read the JSONL file
        with open(input_file, 'r') as input_file:
            for line in input_file:
                data = json.loads(line)

                # Convert to desired format
                formatted_output = f"Query: {data['query']}\nResponse: {data['response']}\nLabel: {data['label']}\n\n"

                # Write the formatted output to the file
                output_file.write(formatted_output)

    print(f"Conversion complete. Output saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSONL to text format")
    parser.add_argument(
        "input_file", help="Path to input JSONL file")
    parser.add_argument(
        "output_file", help="Path to save the converted text file")
    args = parser.parse_args()

    convert_jsonl_to_text(args.input_file, args.output_file)