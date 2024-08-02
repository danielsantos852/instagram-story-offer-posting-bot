# --- Imports ---

# Standard
import logging

# Third party
import pandas as pd

# --- Global configuration ---

# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)

# Global variables
DEFAULT_OFFERS_TABLE_DATA = {"sitestripe_url":[]}
DEFAULT_OFFERS_TABLE_OUTPUT_PATH = './offers/offers.xlsx'
DEFAULT_OFFERS_TABLE_SHEET_NAME = 'offers'


# --- The Scraper class ---
class Scraper:

    # New offers spreadsheet (empty, for human to fill manually)
    @classmethod
    def new_offers_table(cls, 
                         output_path:str = DEFAULT_OFFERS_TABLE_OUTPUT_PATH
                         ) -> str:
        
        # Create new dataframe from template
        offers_spreadsheet = pd.DataFrame(data=DEFAULT_OFFERS_TABLE_DATA)
        
        # Save dataframe as Excel file
        offers_spreadsheet.to_excel(output_path,
                                    sheet_name=DEFAULT_OFFERS_TABLE_SHEET_NAME,
                                    index=False)

        # Return output file path
        return output_path


    # Scrape amazon offers