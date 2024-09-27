import datasets
import json
import random

# Load the dataset from Hugging Face
dataset = datasets.load_dataset("Kkordik/persona-based-chat-messages")

# Get the total number of rows
total_rows = len(dataset['train'])

# Generate 1062 unique random indices
random_indices = random.sample(range(total_rows), 1062)

# Extract the random samples
random_samples = [dataset['train'][i] for i in random_indices]

# Save the random samples to a new JSONL file
with open('random_samples.jsonl', 'w') as f:
    for sample in random_samples:
        json.dump(sample, f)
        f.write('\n')

print("1062 random samples have been extracted and saved to 'random_samples.jsonl'")
