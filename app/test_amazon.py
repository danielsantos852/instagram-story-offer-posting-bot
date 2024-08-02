# --- Imports ---

# Local
from amazon import Scraper


# --- Main Function ---
def main():
    
    test_new_offers_table()


# Test new offers table
def test_new_offers_table():
    
    # Create new offers table
    Scraper.new_offers_table()

    # Return nothing
    return None


# Call main function
if __name__=='__main__': main()