# --- Imports ---

# Local
from offer import Scraper


# --- Main Function ---

def main():
    test_parse_input_txt()


# --- Functions ---

# Test parse
def test_parse_input_txt():

    # Parse input text file
    url = Scraper.parse_input_txt()

    # Print extracted url
    print(url)

    # Return nothing
    return None


# Test reset input text file
def test_respawn_input_txt():

    # Reset input text file
    Scraper.respawn_input_txt()

    # Return nothing
    return None


# Call main function
if __name__=='__main__': main()