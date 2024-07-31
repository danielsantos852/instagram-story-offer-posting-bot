# Imports
import logging


# Logger configuration
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(filename='./logs/android_device.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)


# Global configuration


# The Generator class:
class Generator:

    # __init__ method
    def __init__(self):
        ...

    # __str__ method
    def __str__(self) -> str:
        ...


# Get Generator function:
def get_generator():
    ...

