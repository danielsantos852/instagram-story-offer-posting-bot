# --- Imports ---
# Standard
import logging
import os
import sys
# Local
from android import Device as AndroidDevice
from image import Generator as ImageGenerator
from scraping import Scraper as OfferScraper


# --- Global Configuration ---
# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)
# Global variables
DEFAULT_INPUT_TXT_FILE_NAME = 'input.txt'
DEFAULT_INPUT_TXT_FOLDER = './offers/'
DEFAULT_INPUT_TXT_TEXT = 'Paste a single offer url per line. '\
                         'No more, no less.\n'
DEFAULT_VALID_URL_PREFIXES = ['https://amzn.to/', 
                              'https://www.amazon.com.br/']
DEFAULT_POST_IMG_TEMPLATE_PATH = './resources/templates/'\
                                 'offer-post-720x1280.png'
DEFAULT_POST_IMG_OUTPUT_FILE_NAME = 'post-image.png'
DEFAULT_POST_IMG_OUTPUT_FOLDER = './temp/'
DEFAULT_IG_LINK_STICKER_TEXT = 'ver oferta'


# --- The Bot class ---
class Bot:
    # --- Magic methods ---
    # __init__
    def __init__(self,
                 input_txt_file_name:str,
                 input_txt_folder:str,
                 input_txt_default_content:str,
                 valid_url_prefixes:list,
                 post_img_template_path:str,
                 post_img_output_file_name:str,
                 post_img_output_folder:str,
                 ig_link_sticker_text:str,
                 ):

        # Instance logger setup
        self._logger = logging.getLogger(__name__)\
                              .getChild(self.__class__.__name__)\

        # Validate input.txt file name
        if not input_txt_file_name:
            raise ValueError('Missing input.txt file name.')

        # Validate input.txt folder
        if not input_txt_folder:
            raise ValueError('Missing input.txt folder path.')

        # Validate input.txt default content
        if not input_txt_default_content:
            raise ValueError('Missing input.txt default content.')

        # Validate valid url prefixes list
        if not valid_url_prefixes:
            raise ValueError('Missing valid url prefixes list.')

        # Validate post image template path
        if not post_img_template_path:
            raise ValueError('Missing post image template path.')

        # Validate post image output file name
        if not post_img_output_file_name:
            raise ValueError('Missing post image output file name.')

        # Validate post image output folder
        if not post_img_output_folder:
            raise ValueError('Missing post image output folder path.')
        
        # Validate Instagram link sticker text
        if not ig_link_sticker_text:
            raise ValueError('Missing Instagram link sticker text.')

        # Set object variables
        self.input_txt_file_name = input_txt_file_name
        self.input_txt_folder = input_txt_folder
        self.input_txt_file_path = f'{input_txt_folder}{input_txt_file_name}'
        self.input_txt_default_content = input_txt_default_content
        self.valid_url_prefixes = valid_url_prefixes
        self.post_img_template_path = post_img_template_path
        self.post_img_output_file_name = post_img_output_file_name
        self.post_img_output_folder = post_img_output_folder
        self.ig_link_sticker_text = ig_link_sticker_text


    # --- Public methods ---
    # Get Bot
    @classmethod
    def get(cls,
            input_txt_file_name:str = DEFAULT_INPUT_TXT_FILE_NAME,
            input_txt_folder:str = DEFAULT_INPUT_TXT_FOLDER,
            input_txt_default_content:str = DEFAULT_INPUT_TXT_TEXT,
            valid_url_prefixes:list = DEFAULT_VALID_URL_PREFIXES,
            post_img_template_path:str = DEFAULT_POST_IMG_TEMPLATE_PATH,
            post_img_output_file_name:str = DEFAULT_POST_IMG_OUTPUT_FILE_NAME,
            post_img_output_folder:str = DEFAULT_POST_IMG_OUTPUT_FOLDER,
            ig_link_sticker_text:str = DEFAULT_IG_LINK_STICKER_TEXT
            ):
        # TODO Add a docstring

        # Return Bot object
        logger.info('Getting Bot object...')
        return Bot(input_txt_file_name=input_txt_file_name,
                   input_txt_folder=input_txt_folder,
                   input_txt_default_content=input_txt_default_content,
                   valid_url_prefixes=valid_url_prefixes,
                   post_img_template_path=post_img_template_path,
                   post_img_output_file_name=post_img_output_file_name,
                   post_img_output_folder=post_img_output_folder,
                   ig_link_sticker_text=ig_link_sticker_text)


    # Run bot
    def run(self):
        # TODO Add a docstring     
        self._logger.info('Starting bot...')

        # Check input.txt status, stop bot if file not found
        self._logger.info(f'Checking input.txt status...')
        status = self._check_input_txt_status(
            create_if_not_found=True,
            input_txt_default_content=DEFAULT_INPUT_TXT_TEXT)
        if status == 1:
            sys.exit(f'File "{self.input_txt_file_path}" not found. '\
                     f'Create file and run bot again. Stopping...')

        # Parse input.txt
        self._logger.info(f'Parsing input.txt...')
        offer_urls = self._parse_input_txt()

        # If no valid urls parsed, stop bot
        if len(offer_urls) == 0:
            sys.exit(f'File "{self.input_txt_file_path}" '\
                     f'has no valid urls for parsing. '\
                     f'Add valid urls to the file and '\
                     f'run bot again.')

        # Get offer scraper object
        self._logger.info('Creating offer scraper...')
        scraper = OfferScraper.get()

        # Get image generator object
        self._logger.info('Creating offer image generator...')
        generator = ImageGenerator.get(
            post_img_template=self.post_img_template_path)

        # Get android device object
        self._logger.info('Connecting to android device...')
        device = AndroidDevice.get(device_name='device')

        # Do this (len(offer_urls)+1) times
        for i in range(len(offer_urls)):

            # Scrape first url on offer urls list
            offer = scraper.scrape_amazon_offer(offer_urls[0])

            # Create Instagram post image
            post_img = generator.create_offer_post_image(
                offer=offer,
                output_img_folder=self.post_img_output_folder,
                output_img_name=self.post_img_output_file_name)

            # Post Instagram story
            device.post_instagram_story(
                post_image=post_img,
                linksticker_url=offer.url,
                linksticker_custom_text=self.ig_link_sticker_text,
                close_friends_only=True)

            # Remove first url from offer urls list
            offer_urls.pop(0)

            # Re-create input.txt
            self._create_input_txt(content=self.input_txt_default_content,
                                   urls=offer_urls)

        self._logger.info('Bot run complete.')


    # --- Helper methods ---
    # Check input.txt status
    def _check_input_txt_status(
            self,
            create_if_not_found:bool = True,
            input_txt_default_content:str = ''
        ) -> int:
        # TODO Add a docstring
        # If file exists, return status 0
        if os.path.exists(self.input_txt_file_path):
            self._logger.debug(f'File "{self.input_txt_file_path}" exists. '
                               f'Return status 0.')
            return 0
        # If absent file:
        else:
            # If create_if_not_found, create file, return status 0
            if create_if_not_found:
                self._logger.debug(f'File "{self.input_txt_file_path}" '\
                                   f'does not exist. Creating...')
                self._create_input_txt(content=input_txt_default_content)
                self._logger.debug(f'Created file '\
                                   f'"{self.input_txt_file_path}". '\
                                   f'Return status 0.')
                return 0
            # Else, return status 1
            else:
                self._logger.debug(f'File "{self.input_txt_file_path}" '\
                                   f'does not exist. Return status 1.')
                return 1


    # Create input.txt
    def _create_input_txt(
            self,
            content:str = '',
            urls:list = []
        ) -> str:
        # TODO Add a docstring
        # If urls list provided, add urls to content
        if len(urls) > 0:
            self._logger.debug(f'Adding urls to input.txt content...')
            for url in urls:
                content = f'{content}{url}\n'
            self._logger.debug(f'Added urls.')

        # Create text file and write content
        self._logger.debug(f'Creating "{self.input_txt_file_path}"...')
        with open(self.input_txt_file_path, 'w') as file:
            file.write(content)
        self._logger.debug(f'Created file.')

        # Return nothing
        return None


    # Parse input.txt
    def _parse_input_txt(self) -> list:
        # TODO Add a docstring
        # Read input.txt lines to memory
        with open(self.input_txt_file_path, 'r') as file:
            lines = file.readlines()

        # Check each line for a valid url prefix, if found, save line
        valid_lines = []
        for line in lines:
            for valid_url_prefix in self.valid_url_prefixes:
                if valid_url_prefix in line:
                    valid_lines.append(line)
                    break

        # Clean saved lines for valid urls
        valid_urls = []
        for line in valid_lines:
            valid_url = line.replace('\n','').strip()
            valid_urls.append(valid_url)
        self._logger.debug(f'Parsed {self.input_txt_file_path}. '\
                           f'Valid URLs found: {len(valid_urls)}.')

        # Return valid urls list
        return valid_urls

