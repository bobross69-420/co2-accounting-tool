import sys
from data_loader import load_csv_data
from logic import calculate_invoice_emissions
from analytics import generate_text_report, export_results

# --- Constants ---
# Defining filenames as constants here avoids "Hardcoded Values" deep in the code logic.
# This makes it easier to change filenames in the future from a single location.
INVOICE_FILE = 'invoices.csv'
FACTORS_FILE = 'emission_factors.csv'
OUTPUT_FILE = 'invoice_with_co2_results.csv'

def main() -> None:
    """
    Main execution flow of the CO2 Accounting Tool.
    """
    print("Starting CO2 Accounting Tool...")

    # 1. Load Data
    # Using try/except blocks to prevent the program from crashing immediately 
    # if a user forgets to add the input files.
    try:
        print(f"Loading '{FACTORS_FILE}'...")
        factors_db = load_csv_data(FACTORS_FILE)
        
        print(f"Loading '{INVOICE_FILE}'...")
        invoices = load_csv_data(INVOICE_FILE)
    except Exception as e:
        print(f"Critical Error during loading: {e}")
        sys.exit(1)

    # Validate data integrity before proceeding
    if not factors_db or not invoices:
        print("Error: One or more input files were empty or invalid. Exiting.")
        sys.exit(1)

    # 2. Process Data (The Engine)
    print("Matching invoices to emission factors...")
    final_data = calculate_invoice_emissions(invoices, factors_db)

    # 3. Generate Analytics
    generate_text_report(final_data)

    # 4. Export Data
    export_results(final_data, OUTPUT_FILE)

    print("Done.")

if __name__ == "__main__":
    main()