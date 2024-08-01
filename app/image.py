# Imports
import logging
from PIL import Image


# Logger configuration
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(filename='./logs/android_device.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)


# Global variables
DEFAULT_SAVE_IMAGE_AS_OUTPUT_FILE_PATH = './temp/image.png'
DEFAULT_SAVE_IMAGE_AS_FILE_NAME = 'image'
DEFAULT_SAVE_IMAGE_AS_FILE_FOLDER = './temp/'
DEFAULT_SAVE_IMAGE_AS_FILE_FORMAT = 'png'


# The Generator class:
class Generator:

    # Class logger setup
    _class_logger = logging.getLogger(__name__).getChild(__qualname__)
    _class_logger.info('Class logger set up.')


    # --- Public Methods ---
    # Generate offer image
    @classmethod
    def generate_offer_image(cls):
        ...


    # --- Helper Methods ---
    # New image from template
    @classmethod
    def _new_image_from_template(cls, file_path:str) -> None:
        
        # Create new image from template
        new_image = Image.open(fp=file_path)
        
        # Set new image as current image
        cls._current_image = new_image
        
        # Return nothing
        return None


    # Insert image
    @classmethod
    def _insert_image(cls, file_path:str) -> None:
        ...


    # Insert textbox
    @classmethod
    def _insert_textbox(cls, text, box) -> None:
        ...


    # Save image as
    @classmethod
    def _save_image_as(cls,
                       file_path = DEFAULT_SAVE_IMAGE_AS_OUTPUT_FILE_PATH
                       ) -> None:

        # Save current image to file path
        cls._current_image.save(fp=file_path)

        # Return file path
        return file_path

