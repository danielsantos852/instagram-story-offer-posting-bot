# --- Imports ---

# Standard
import os
import sys

# Local
from offer import Scraper as OfferScrapper
from image import Generator as ImageGenerator
from android import Device as AndroidDevice


# --- Global configuration ---

# Global variables
INPUT_TXT_PATH = './offers/input.txt'


# --- Main Function ---
def main():

    # If no input txt file, respawn it and exit program
    if not os.path.exists(path=INPUT_TXT_PATH):
        OfferScrapper.new_txt_file(path=INPUT_TXT_PATH)
        sys.exit(f'File "{INPUT_TXT_PATH}" not found, respawned. Run program again.')
    
    # Extract a valid offer url from input txt

    # Scrape offer data

    # Generate offer image

    # Post offer image


# Call main()
if __name__=='__main__': main()