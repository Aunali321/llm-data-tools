"""
Conversation Format Converter and Token Counter

Converts a JSONL file with conversations to a text file with a specific format and counts the number of tokens.

Usage: python convert_format_and_count_tokens.py <input_file> <output_file>

Input:
- input_file: Path to the input JSONL file
- output_file: Path to save the converted text file

Example:
python convert_format_and_count_tokens.py datasets/part2/synthetic_dataset_mythomax-l2-13b.jsonl datasets/part2/synthetic_dataset_mythomax-l2-13b.txt

Input JSONL Example:
{"messages": [{"content": "You are a helpful assistant.", "role": "system"}, {"content": "Hello", "role": "user"}, {"content": "Hi there!", "role": "assistant"}]}

Output Text Example:
Human: Hello
Assistant: Hi there!

Output Token Count:
...
Conversation 835: 633 tokens

Total conversations: 835
Total tokens: 619749
Average tokens per conversation: 742.21
"""

import json
import tiktoken
import argparse

def count_tokens(text, encoding_name="cl100k_base"):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def convert_format_and_count_tokens(input_file, output_file):
    with open(input_file, 'r') as f:
        conversations = f.readlines()

    total_tokens = 0
    conversation_count = 0

    with open(output_file, 'w') as f:
        for conversation in conversations:
            try:
                data = json.loads(conversation.strip())
                conversation_tokens = 0
                conversation_text = ""
                for message in data['messages']:
                    if message['role'] == 'user':
                        line = f"Human: {message['content']}\n"
                    elif message['role'] == 'assistant':
                        line = f"Assistant: {message['content']}\n"
                    else:
                        continue

                    f.write(line)
                    conversation_text += line
                    conversation_tokens += count_tokens(line)

                f.write("\n")  # Add a blank line between conversations
                total_tokens += conversation_tokens
                conversation_count += 1

                # Ccomment the following line to hide print the number of tokens in each conversation
                print(
                    f"Conversation {conversation_count}: {conversation_tokens} tokens")

            except json.JSONDecodeError:
                print(f"Skipping invalid JSON: {conversation}")

    print(f"\nTotal conversations: {conversation_count}")
    print(f"Total tokens: {total_tokens}")
    print(
        f"Average tokens per conversation: {total_tokens / conversation_count:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert conversation format and count tokens")
    parser.add_argument(
        "input_file", help="Path to input JSONL file")
    parser.add_argument(
        "output_file", help="Path to save the converted text file")
    args = parser.parse_args()

    convert_format_and_count_tokens(args.input_file, args.output_file)