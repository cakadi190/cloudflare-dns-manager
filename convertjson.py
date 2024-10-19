import json, signal

def ignore_sigint(signum, frame):
    """Handler to ignore CTRL+C interruptions."""
    print("\nCTRL+C is disabled. Please use 'exit' to terminate the program.")
    return

def get_json_input() -> str:
    """Prompts the user for JSON input and returns it as a string."""
    return input("Enter your JSON data here:\n")

def parse_json(data: str) -> dict:
    """Parses a JSON string into a Python dictionary.

    Raises:
        ValueError: If the JSON string is invalid.
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format! Please enter a valid JSON string.")

def save_json_to_file(json_data: dict, filename: str = "add-dns.json") -> None:
    """Saves the provided JSON data to a specified file in minified format.

    Args:
        json_data (dict): The JSON data to save.
        filename (str): The name of the file to save the data in.
    """
    with open(filename, "w") as file:
        json.dump(json_data, file, separators=(',', ':'))  # Minified format

    print("\n🔃 Sedang mengubah ke file *.json, tunggu sebentar")
    print(f'✅ Successfully written into "{filename}" in minified format!')

def handle_json_operations():
    """Coordinates the JSON input, parsing, and saving operations."""
    json_data = get_json_input()
    parsed_data = parse_json(json_data)
    save_json_to_file(parsed_data)

def main():
    """Main function to run the program."""
    signal.signal(signal.SIGINT, ignore_sigint)  # Ignore CTRL+C
    try:
        handle_json_operations()
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
