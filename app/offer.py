# --- Imports ---
# Standard
import logging


# --- Global Configuration ---
# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)


# --- The Offer class ---
class Offer:
    # --- Magic methods ---
    # __init__
    def __init__(
            self,
            url:str,
            name:str,
            thumbnail:str,
            price_now:float,
            price_before:float|None,
            discount:float|None,
        ):
        """"
        Initialize an Offer object.

        :param url: URL to the offer.

        :param name: Product name.

        :param thumbnail: File path to product thumbnail.

        :param price_now: Product price after discount.
        
        :param price_before: Product price before discount.

        :param discount: Discount rate as a float (1.0 = 100%).

        :returns: None.
        """
        # Instance logger setup
        self._logger = logging.getLogger(__name__)\
                              .getChild(self.__class__.__name__)

        # Validate url
        if not url:
            raise ValueError("Missing offer url.")

        # Validate name
        if not name:
            raise ValueError("Missing offer name.")

        # Validate thumbnail
        if not thumbnail:
            raise ValueError("Missing offer thumbnail.")

        # Set instance attributes
        self.url = url
        self.name = name
        self.thumbnail = thumbnail
        self.price_now = price_now
        self.price_before = price_before
        self.discount = discount

    # __str__
    def __str__(self) -> str:
        return f' --- Offer info ---\n'\
               f'url = {self.url}\n'\
               f'name = {self.name}\n'\
               f'thumbnail = {self.thumbnail}\n'\
               f'price_now = {self.price_now}\n'\
               f'price_before = {self.price_before}\n'\
               f'discount = {self.discount}\n'\
               f' ------------------'

    # --- Public methods ---
    # Get Offer
    @classmethod
    def get(
            cls,
            url:str,
            name:str,
            thumbnail:str,
            price_now:float,
            price_before:float|None,
            discount:float|None
        ):
        """"
        Get an Offer.

        :param url: URL to the offer.

        :param name: Product name.

        :param thumbnail: File path to product thumbnail.

        :param price_now: Product price after discount.
        
        :param price_before: Product price before discount.

        :param discount: Discount rate as a float (1.0 = 100%).

        :returns: An instance of Offer.
        """
        # Return Offer instance
        logger.debug('Getting Offer instance...')
        return Offer(url=url,
                     name=name,
                     thumbnail=thumbnail,
                     price_now=price_now,
                     price_before=price_before,
                     discount=discount)

    # Get discount (as float or str)
    def get_discount(self, as_str:bool = True) -> float|str:
        """
        Get offer's discount value (as float or as str).

        :param as_str: If set to True, return value will be like "100%" (str). 
            If set to False, return value will be like 1.0 (float).

        :returns: Offer's discount value (as float or as str).
        """
        if not as_str:
            return self.discount                    # 1.0
        else:
            return f'{(self.discount*100):.0f}%'    # "100%"

    # Get ("now" or "before") price (as float or str)
    def get_price(
            self, 
            now_or_before:str = 'now', 
            as_str:bool = True
        ) -> float|str:
        """
        Get offer's price value (as float or as str).

        :param now_or_before: If set to "now", offer's "now" price will be 
            returned. If set to "before", offer's "before" price will be 
            returned.

        :param as_str: If set to True, return value will be like "1.000,00" 
            (str). If set to False, return value will be like 1000.0 (float).

        :returns: Offer's "now" or "before" price value (as float or as str).
        """
        # Get specified price ("now" or "before")
        if now_or_before == 'now':
            price = self.price_now
        elif now_or_before == 'before':
            price = self.price_before
        else:
            raise ValueError(f'Invalid now_or_before value: '\
                             f'must be "now" or "before", '\
                             f'not {now_or_before}.')

        # Return price (as float or as str)
        if not as_str:
            return price                                # 0000.00
        else:
            price = f'{price:.2f}'.replace('.',',')     # "0000,00"
            if len(price.split(',')[0]) > 3:
                price = f'{price[:-6]}.{price[-6:]}'    # "0.000,00"
            return price
