# --- Imports ---

# Standard
import logging

# Third party
#import pandas as pd


# --- Global configuration ---

# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)

# Global variables
DEFAULT_INPUT_TXT_FIRST_LINER = "Paste a single offer url per line, no more, no less.\n"
DEFAULT_INPUT_TXT_PATH = './offers/input.txt'
DEFAULT_VALID_URL_PREFIXES = ['https://amzn.to/', 
                              'https://www.amazon.com.br/']


# --- The Scraper class ---

class Scraper:

    # --- Public Methods ---

    # Respawn input text file
    @classmethod
    def respawn_input_txt(cls,
                          path:str,
                          content:str
                          ) -> str:

        # (Re-)Create text file
        with open(file=path, mode='w') as file:
            file.write(content)

        # Return path to text file
        return path


    # Parse input text file
    @classmethod
    def parse_input_txt(cls,
                        path:str = DEFAULT_INPUT_TXT_PATH,
                        first_liner:str = DEFAULT_INPUT_TXT_FIRST_LINER
                        ) -> str:

        # With text file open:
        with open(file=path, mode='r+') as file:

            # Read text file lines to memory
            lines = file.readlines()

            # Re-write first line message in text file
            file.seek(0)
            file.write(first_liner)

            # Flag for first-found valid line
            valid_line_found = False

            # For each line in lines:
            for line in lines:

                # Check line for valid url prefixes:
                for valid_prefix in DEFAULT_VALID_URL_PREFIXES:

                    # If valid prefix found:
                    if valid_prefix in line:
                        
                        # If first occurrence:
                        if not valid_line_found:

                            # Save line to memory, update flag, stop check
                            valid_line = line
                            valid_line_found = True
                            break

                        # If second+ occurence:
                        else:

                            # Write valid line back into file, stop check
                            file.write(line)
                            break

            # Delete any content ahead of cursor
            file.truncate()

        # Clean valid url
        print(valid_line)

        # Return valid url
        return valid_line


    # Scrape amazon offer
    @classmethod
    def scrape_amazon_offer(cls, offer_url):
        ...

