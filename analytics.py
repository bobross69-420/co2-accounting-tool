import csv

def generate_text_report(processed_data: list[dict]) -> None:
    """
    Prints a statistical summary of the carbon footprint to the console.
    """
    total_co2 = 0.0
    highest_item = None
    highest_val = -1.0
    
    print("\n" + "="*40)
    print("       CO2 ACCOUNTING REPORT       ")
    print("="*40)
    
    for row in processed_data:
        co2 = row['total_line_co2']
        total_co2 += co2
        
        # Track the highest emitter for the summary
        if co2 > highest_val:
            highest_val = co2
            highest_item = row['item_description']
            
    print(f"Total Carbon Footprint: {total_co2:.2f} kg CO2")
    if highest_item:
        print(f"Highest Emitting Item:  {highest_item} ({highest_val:.2f} kg)")
    
    # Basic warning for unmatched items to alert the user of data quality issues
    unmatched_count = sum(1 for row in processed_data if row['matched_factor'] == 0)
    if unmatched_count > 0:
        print(f"Warning: {unmatched_count} items could not be matched to emission factors.")
    
    print("="*40 + "\n")

def export_results(processed_data: list[dict], filename: str) -> None:
    """
    Saves the processed list of dictionaries to a new CSV file.
    
    Args:
        processed_data (list[dict]): The data to save.
        filename (str): The name of the output file.
    """
    if not processed_data:
        print("No data to export.")
        return

    keys = processed_data[0].keys()
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(processed_data)
        print(f"SUCCESS: Detailed results exported to '{filename}'")
    except IOError as e:
        print(f"Error exporting file: {e}")