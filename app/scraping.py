# --- Imports ---

# Standard
import logging

# Third party
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException


# --- Global Configuration ---

# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)


# --- The Offer class ---
class Offer:
    
    # --- Magic methods ---

    # __init__
    def __init__(self,
                 offer_url:str,
                 offer_title:str,
                 offer_thumbnail:str,
                 offer_price_now:float,
                 offer_price_before:float|None,
                 offer_discount_rate:float|None,
                 ):

        # Validate offer url
        if not offer_url:
            raise ValueError("Missing offer url.")

        # Validate offer name
        if not offer_title:
            raise ValueError("Missing offer title.")

        # Validate offer thumbnail
        if not offer_thumbnail:
            raise ValueError("Missing offer thumbnail.")

        # Validate offer "now" price
        if not offer_price_now:
            raise ValueError('Missing offer "now" price.')

        # Set object attributes
        self.offer_url = offer_url
        self.offer_title = offer_title
        self.offer_thumbnail = offer_thumbnail
        self.offer_price_now = offer_price_now
        self.offer_price_before = offer_price_before
        self.offer_discount_rate = offer_discount_rate


    # __str__
    def __str__(self) -> str:
        return f'------------------------ Offer Info ------------------------\n'\
               f'URL:            {self.offer_url}\n'\
               f'Title:          {self.offer_title}\n'\
               f'Thumbnail:      {self.offer_thumbnail}\n'\
               f'"Now" price:    {self.offer_price_now}\n'\
               f'"Before" price: {self.offer_price_before}\n'\
               f'Discount rate:  {self.offer_discount_rate}\n'\
               f'------------------------------------------------------------'


    # --- Public methods ---

    # Get Offer
    @classmethod
    def get(cls,
            offer_url,
            offer_title,
            offer_thumbnail,
            offer_price_now,
            offer_price_before,
            offer_discount_rate
            ):
        
        # Return Offer object
        return Offer(offer_url=offer_url,
                     offer_title=offer_title,
                     offer_thumbnail=offer_thumbnail,
                     offer_price_now=offer_price_now,
                     offer_price_before=offer_price_before,
                     offer_discount_rate=offer_discount_rate)


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
        return Scraper()


    # Scrape an amazon.com.br offer
    def scrape_amazon_offer(self,
                            url:str
                            ) -> Offer:

        # Create a web driver
        self._create_webdriver()

        # Visit offer url
        offer_url = url
        print('GET-ing offer url...')
        self.driver.get(url=offer_url)
        print('GET-ed offer url.')

        # Get offer title
        print('Getting offer title...')
        offer_title = self.driver.find_element(by=By.ID, value='productTitle').text.strip()
        print(f'offer_title = "{offer_title}"')

        # Get offer thumbnail
        print('Getting offer thumnail...')
        _ = self.driver.find_element(by=By.ID, value='imgTagWrapperId')
        _ = _.find_element(by=By.TAG_NAME, value='img')
        offer_thumbnail = _.get_attribute(name='src')
        print(f'offer_thumbnail = "{offer_thumbnail}"')

        # Get "now" price
        print('Getting offer "now" price...')
        element = self.driver.find_element(by=By.ID, value='corePriceDisplay_desktop_feature_div')
        price_whole = element.find_element(by=By.CLASS_NAME, value='a-price-whole').text.strip()
        price_fraction = element.find_element(by=By.CLASS_NAME, value='a-price-fraction').text.strip()
        offer_price_now = float(f'{price_whole}.{price_fraction}')
        print(f'offer_price_now = {offer_price_now}')

        # Get "before" price
        try:
            print('Getting offer "before" price...')
            _ = element.find_element(by=By.CLASS_NAME, value='a-spacing-small')
            _ = _.find_element(by=By.CLASS_NAME, value='a-text-price').text
            offer_price_before = float(_.replace('R$','').replace(',','.'))
            print(f'offer_price_before = {offer_price_before}')
        except NoSuchElementException:
            print('Offer "before" price not found, set to None.')
            offer_price_before = None

        # Get discount rate
        try:
            print('Getting offer discount rate...')
            _ = element.find_element(by=By.CLASS_NAME, value='savingsPercentage').text
            offer_discount_rate = float(_.replace('-','').replace('%',''))/100
            print(f'offer_discount_rate = {offer_discount_rate}')
        except NoSuchElementException:
            print('Offer discount rate not found, set to None.')
            offer_discount_rate = None

        # Quit web driver
        self._delete_webdriver()

        # Return Offer object
        return Offer(offer_url=offer_url,
                     offer_title=offer_title,
                     offer_thumbnail=offer_thumbnail,
                     offer_price_now=offer_price_now,
                     offer_price_before=offer_price_before,
                     offer_discount_rate=offer_discount_rate)


    # --- Helper methods ---

    # Create webdriver
    def _create_webdriver(self):

        # Set Chrome webdriver options and start it
        print('Creating webdriver...')
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_experimental_option(
            "prefs", {
                # block image loading
                "profile.managed_default_content_settings.images": 2,
            }
        )
        self.driver = webdriver.Chrome(options=options)
        print('Created webdriver.')

        # Return nothing
        return None


    # Delete webdriver
    def _delete_webdriver(self, 
                          driver = None):

        # If external driver passed, close it
        if driver:
            print(f'Quitting specified web driver...')
            driver.quit()
        # Else, close self.webdriver
        else:
            print(f'Quitting object web driver...')
            self.driver.quit()
        print(f'Quitted web driver.')

        # Return nothing
        return None
