# llm-data-tools

This repository provides a set of Python scripts for working with datasets commonly used in Large Language Model (LLM) applications.  The scripts offer functionalities for data conversion, processing, validation, and extraction, making it easier to prepare and manage data for LLM training and evaluation.

## File Tree

```
llm-data-tools/
├── check_message_order.py
├── convert_dataset.py
├── convert_file_format.py
├── convert_format_and_count_tokens.py
├── convert_kto_jsonl_to_text.py
├── extract_random_samples.py
├── filter_csv_columns.py
├── merge_datasets.py
├── remove_last_user_message.py
├── transform_dataset.py
├── validate_jsonl.py
├── pyproject.toml
└── README.md
```

## Installation

We recommend using `uv` for environment management and dependency installation.  If you don't have `uv` installed, you can install it using the following commands:

**Linux/macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Once `uv` is installed, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Aunali321/llm-data-tools.git
   ```

2. Create and activate a virtual environment:

   ```bash
   cd llm-data-tools
   uv venv --python 3.12 
   source .venv/bin/activate  # On Linux/macOS
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:

   ```bash
   uv pip install -r pyproject.toml
   ```

## Scripts

* **`check_message_order.py`**: Checks the order of messages (e.g., system, user, assistant) in a JSONL file.
* **`convert_file_format.py`**: Converts between CSV, JSONL, and Parquet formats.
* **`convert_dataset.py`**: Converts dataset to ChatML format.
* **`convert_format_and_count_tokens.py`**: Converts JSONL conversations to text and counts tokens.
* **`convert_jsonl_to_text.py`**: Converts JSONL to a formatted text file.
* **`extract_random_samples.py`**: Extracts random samples from a Hugging Face dataset.
* **`filter_csv_columns.py`**: Filters a CSV file to keep only specified columns.
* **`merge_datasets.py`**: Merges multiple Hugging Face datasets into a Parquet file.
* **`remove_last_user_message.py.`**: Removes the last "user" message from JSONL conversations.
* **`transform_dataset.py`**: Transforms JSONL conversation data for LLM training.
* **`validate_jsonl.py`**: Validates JSONL file structure and content.


## Usage

Refer to each script's docstrings for detailed usage instructions and examples. Each script is run from the command line with specific arguments.  Use `python script_name.py --help` for help.


## Contributing

Contributions are welcome!  Open an issue for bugs or feature requests.

## License
MIT