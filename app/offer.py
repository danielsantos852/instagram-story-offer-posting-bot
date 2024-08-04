# --- Imports ---

# Standard
import logging


# --- Global configuration ---

# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)

# Global variables
DEFAULT_INPUT_TXT_PATH = './offers/paste-urls-inside-this-file.txt'
DEFAULT_INPUT_TXT_CONTENT = "Paste a single url per line, no more, no less.\n"


# --- The Scraper class ---
class Scraper:

    # Reset offer input txt file
    @classmethod
    def reset_input_txt(cls,
                        input_txt_path:str = DEFAULT_INPUT_TXT_PATH,
                        input_txt_content:str = DEFAULT_INPUT_TXT_CONTENT
                        ) -> str:

        # Create/Overwrite input txt file
        with open(file=input_txt_path, mode='w') as file:
            
            # Rewrite input txt content
            file.write(input_txt_content)

        # Return path to input txt file
        return input_txt_path


    # Scrape amazon offer
    @classmethod
    def scrape_amazon_offer(cls, offer_url):
        
        ...

