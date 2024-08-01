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
    # Create image from template
    @classmethod
    def _create_image_from_template(cls):
        ...


    # Insert image
    @classmethod
    def _insert_image(cls):
        ...


    # Insert textbox
    @classmethod
    def _insert_textbox(cls):
        ...


    # Save image as
    @classmethod
    def _save_image_as(cls):
        ...

