import difflib

def get_emission_factor(item_description: str, factors_db: list[dict]) -> float:
    """
    Determines the CO2 emission factor for a given item description using a 4-step matching process.
    
    Algorithm:
    1. Normalization: Clean input string (lowercase, strip).
    2. Direct Keyword Match: Check if a known category matches a substring of the description.
    3. Fuzzy Word Match: Split description into words and fuzzy match each against database.
    
    Args:
        item_description (str): The raw text from the invoice.
        factors_db (list): List of dicts from emission_factors.csv.
        
    Returns:
        float: The matched emission factor (kg CO2). Returns 0.0 if no match found.
    """
    
    # --- Step 1: Normalization ---
    # We normalize inputs to lowercase to ensure matching works regardless of 
    # capitalization (e.g., "Laptop" vs "laptop").
    clean_desc = item_description.lower().strip()
    
    # Build a fast lookup map
    # We create a dictionary here to improve lookup speed (O(1)) compared to iterating a list repeatedly,
    # and to ensure all numeric factors are actually floats before calculation.
    factor_map = {}
    for entry in factors_db:
        try:
            # Strip whitespace from keys to handle messy CSV data (e.g., " laptop ")
            key = entry['category'].lower().strip()
            val = float(entry['factor_kg_co2_per_unit'])
            factor_map[key] = val
        except ValueError:
            # Skip rows where the factor isn't a valid number to prevent crashes later
            continue

    known_categories = list(factor_map.keys())

    # --- Step 2: Keyword / Substring Matching ---
    # We iterate through known categories to catch cases where the category is embedded 
    # in a longer sentence (e.g., finding "uber" inside "Uber Ride to Airport").
    for category in known_categories:
        if category in clean_desc:
            return factor_map[category]

    # --- Step 3: Fuzzy Matching on Individual Words ---
    # We split the description into words to handle typo correction on specific terms.
    # For example, "Ppr Ream" won't match "paper", but the single word "Ppr" is close enough.
    description_words = clean_desc.split()
    
    for word in description_words:
        # We use a strict cutoff (0.7) to ensure we don't accidentally match unrelated words
        # while still catching genuine typos.
        matches = difflib.get_close_matches(word, known_categories, n=1, cutoff=0.7)
        if matches:
            best_match = matches[0]
            return factor_map[best_match]

    return 0.0

def calculate_invoice_emissions(invoice_data: list[dict], factors_db: list[dict]) -> list[dict]:
    """
    Processes the full invoice list and appends CO2 data to each row.
    """
    processed_invoices = []
    
    for row in invoice_data:
        description = row.get('item_description', 'Unknown')
        
        # safely parse quantity, defaulting to 1.0 to prevent zero-division or type errors
        try:
            qty = float(row.get('quantity', 1))
        except ValueError:
            qty = 1.0
            
        factor = get_emission_factor(description, factors_db)
        total_co2 = qty * factor
        
        # We use .copy() to preserve the original data integrity and avoid side effects
        new_row = row.copy()
        new_row['matched_factor'] = factor
        new_row['total_line_co2'] = total_co2
        
        processed_invoices.append(new_row)
        
    return processed_invoices

# --- Unit Test / Self-Check ---
# This block only runs if you execute 'python3 logic.py' directly.
# It validates that the matching logic works as expected before running the main program.
if __name__ == "__main__":
    print("Running Logic Self-Check...")
    
    # Mock Database
    test_db = [
        {'category': 'laptop', 'factor_kg_co2_per_unit': '250.0'},
        {'category': 'coffee', 'factor_kg_co2_per_unit': '5.0'}
    ]
    
    # Test Case 1: Exact Match (Normalization)
    assert get_emission_factor("Laptop", test_db) == 250.0, "Test 1 Failed: Capitalization check"
    
    # Test Case 2: Substring Match
    assert get_emission_factor("Premium Coffee Beans", test_db) == 5.0, "Test 2 Failed: Substring check"
    
    # Test Case 3: Fuzzy Typo Match
    # 'Mackbook' isn't in DB, but 'laptop' is. Let's test a known typo if we had 'macbook' in DB.
    # For this specific test DB, let's test a typo of 'coffee' -> 'coffe'
    assert get_emission_factor("Coffe", test_db) == 5.0, "Test 3 Failed: Typo check"
    
    print("✅ All Logic Tests Passed!")