import csv
import os

def load_csv_data(filepath: str) -> list[dict]:
    """
    Reads a CSV file and returns a list of dictionaries.
    
    Args:
        filepath (str): The path to the CSV file.
        
    Returns:
        list[dict]: A list of dictionaries, where each key is a column header.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the CSV file is empty.
    """
    data = []
    
    # Check if file exists before trying to open it to provide a clear user-friendly error 
    # rather than a raw Python stack trace.
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: The file '{filepath}' was not found. Please check the path.")

    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Check headers to ensure the file isn't empty before processing
            if not reader.fieldnames:
                raise ValueError(f"Error: The file '{filepath}' appears to be empty.")

            for row in reader:
                # We strip whitespace from all values immediately to ensure clean data 
                # flows through the rest of the application.
                clean_row = {k: v.strip() for k, v in row.items() if v is not None}
                data.append(clean_row)
                
    except UnicodeDecodeError:
        print(f"Critical Error: Could not decode '{filepath}'. Is it a valid text CSV?")
        return []
    except Exception as e:
        print(f"Unexpected error reading '{filepath}': {e}")
        return []

    return data