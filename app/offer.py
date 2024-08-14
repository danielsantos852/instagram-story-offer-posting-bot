# --- Imports ---

# Standard
import logging

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
                 url:str,
                 title:str,
                 thumbnail:str,
                 price_now:float,
                 price_before:float|None,
                 discount_rate:float|None,
                 ):

        # Instance logger setup
        self._logger = logging.getLogger(__name__)\
                              .getChild(self.__class__.__name__)

        # Validate offer url
        if not url:
            raise ValueError("Missing offer url.")

        # Validate offer name
        if not title:
            raise ValueError("Missing offer title.")

        # Validate offer thumbnail
        if not thumbnail:
            raise ValueError("Missing offer thumbnail.")

        # Validate offer "now" price
        if not price_now:
            raise ValueError('Missing offer "now" price.')

        # Set object attributes
        self.url = url
        self.title = title
        self.thumbnail = thumbnail
        self.price_now = price_now
        self.price_before = price_before
        self.discount_rate = discount_rate


    # __str__
    def __str__(self) -> str:
        return f'------------------------ Offer Info ------------------------\n'\
               f'URL:            {self.url}\n'\
               f'Title:          {self.title}\n'\
               f'Thumbnail:      {self.thumbnail}\n'\
               f'"Now" price:    {self.price_now}\n'\
               f'"Before" price: {self.price_before}\n'\
               f'Discount rate:  {self.discount_rate}\n'\
               f'------------------------------------------------------------'


    # --- Public methods ---

    # Get Offer
    @classmethod
    def get(cls,
            url:str,
            title:str,
            thumbnail:str,
            price_now:float,
            price_before:float|None,
            discount_rate:float|None
            ):
        # TODO Add a docstring

        # Return Offer object
        logger.debug('Getting Offer object...')
        return Offer(url=url,
                     title=title,
                     thumbnail=thumbnail,
                     price_now=price_now,
                     price_before=price_before,
                     discount_rate=discount_rate)

