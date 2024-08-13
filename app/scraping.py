# --- Imports ---

# Standard
from io import BytesIO
import requests
import logging

# Third party
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Local
from offer import Offer

# --- Global Configuration ---

# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)

# Global variables
DEFAULT_THUMBNAIL_DEST_FILE_NAME = 'thumbnail.png'
DEFAULT_THUMBNAIL_DEST_FOLDER = './temp/'

# --- The Scraper class ---
class Scraper:

    # --- Magic methods ---

    # __init__
    def __init__(self):

        # Instance logger setup
        self._logger = logging.getLogger(__name__)\
                              .getChild(self.__class__.__name__)

        # Set object attributes
        self.webdriver = None


    # --- Public methods ---

    # Get Scraper object
    @classmethod
    def get(cls):
        
        # Return Scraper object
        logger.info('Getting Scraper object...')
        return Scraper()


    # Scrape an amazon.com.br offer
    def scrape_amazon_offer(self,
                            url:str,
                            thumbnail_dest_file_name:str = DEFAULT_THUMBNAIL_DEST_FILE_NAME,
                            thumbnail_dest_folder:str = DEFAULT_THUMBNAIL_DEST_FOLDER
                            ) -> Offer:

        # Create a web driver
        self._logger.info('Creating webdriver...')
        self._create_webdriver()

        # Visit offer url
        offer_url = url
        self._logger.info('Visiting offer webpage...')
        self.driver.get(url=offer_url)

        # Get offer title
        self._logger.info('Getting offer title...')
        offer_title = self.driver.find_element(by=By.ID, value='productTitle').text.strip()
        self._logger.debug(f'offer_title = "{offer_title}"')

        # Get offer thumbnail url
        self._logger.info('Getting offer thumbnail source url...')
        _ = self.driver.find_element(by=By.ID, value='imgTagWrapperId')
        _ = _.find_element(by=By.TAG_NAME, value='img')
        url = _.get_attribute(name='src')

        # Download offer thumbnail, save file path
        self._logger.info('Downloading offer thumbnail...')
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        offer_thumbnail = f'{thumbnail_dest_folder}{thumbnail_dest_file_name}'
        image.save(fp=offer_thumbnail)
        self._logger.debug(f'offer_thumbnail = "{offer_thumbnail}"')

        # Get "now" price
        self._logger.info('Getting offer "now" price...')
        element = self.driver.find_element(by=By.ID, value='corePriceDisplay_desktop_feature_div')
        price_whole = element.find_element(by=By.CLASS_NAME, value='a-price-whole').text.strip()
        price_fraction = element.find_element(by=By.CLASS_NAME, value='a-price-fraction').text.strip()
        offer_price_now = float(f'{price_whole}.{price_fraction}')
        self._logger.debug(f'offer_price_now = {offer_price_now}')

        # Get "before" price
        try:
            self._logger.info('Getting offer "before" price...')
            _ = element.find_element(by=By.CLASS_NAME, value='a-spacing-small')
            _ = _.find_element(by=By.CLASS_NAME, value='a-text-price').text
            offer_price_before = float(_.replace('R$','').replace(',','.'))
            self._logger.debug(f'offer_price_before = {offer_price_before}')
        except NoSuchElementException:
            offer_price_before = None
            self._logger.debug('Offer "before" price not found, '\
                               'offer_price_before set to None.')

        # Get discount rate
        try:
            self._logger.info('Getting offer discount rate...')
            _ = element.find_element(by=By.CLASS_NAME, value='savingsPercentage').text
            offer_discount_rate = float(_.replace('-','').replace('%',''))/100
            self._logger.debug(f'offer_discount_rate = {offer_discount_rate}')
        except NoSuchElementException:
            offer_discount_rate = None
            self._logger.debug('Offer discount not found, offer_discount_rate set to None.')

        # Quit web driver
        self._logger.info('Deleting webdriver...')
        self._delete_webdriver()

        # Return Offer object
        self._logger.info('Returning Offer object...')
        return Offer(url=offer_url,
                     title=offer_title,
                     thumbnail=offer_thumbnail,
                     price_now=offer_price_now,
                     price_before=offer_price_before,
                     discount_rate=offer_discount_rate)


    # --- Helper methods ---

    # Create webdriver
    def _create_webdriver(self):

        # Set Chrome webdriver options and start it
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_experimental_option(
            "prefs", {
                # block image loading
                "profile.managed_default_content_settings.images": 2,
            }
        )
        self.driver = webdriver.Chrome(options=options)

        # Return nothing
        return None


    # Delete webdriver
    def _delete_webdriver(self, 
                          driver:webdriver.Chrome|None = None):

        # If external driver passed, close it
        if driver:
            self._logger.debug(f'Quitting specified webdriver...')
            driver.quit()

        # Else, close self.webdriver
        else:
            self._logger.debug(f'Quitting scraper webdriver...')
            self.driver.quit()

        self._logger.debug('Quitted webdriver.')
        
        # Return nothing
        return None
