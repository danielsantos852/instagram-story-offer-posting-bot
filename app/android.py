# --- Imports ---

# Standard
from io import BytesIO
import logging
import random
import sys
import time

# Third party
from PIL import Image
from ppadb.client import Client as AdbClient
from ppadb.device import Device as AdbDevice
import pyautogui
from pyscreeze import Box, center


# --- Global Configuration ---

# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(filename='./logs/android_device.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)

# Global Variables
DEFAULT_ADB_HOST = '127.0.0.1'
DEFAULT_ADB_PORT = 5037
DEFAULT_ADB_PUSH_DESTINATION_FOLDER = '/sdcard/adb-push-files/'
DEFAULT_ADB_PUSH_DESTINATION_FILE_NAME = 'image.png'
SPRITE_ADDSTICKER = './resources/sprites/addsticker.png'
SPRITE_ADDTOSTORY = './resources/sprites/addtostory.png'
SPRITE_CLOSEFRIENDS = './resources/sprites/closefriends.png'
SPRITE_CUSTOMIZESTICKERTEXT = './resources/sprites/customizestickertext.png'
SPRITE_DONE = './resources/sprites/done.png'
SPRITE_LINKSTICKER_BLACK = './resources/sprites/linksticker-black.png'
SPRITE_LINKSTICKER_BLUE = './resources/sprites/linksticker-blue.png'
SPRITE_LINKSTICKER_COLOURED = './resources/sprites/linksticker-coloured.png'
SPRITE_LINKSTICKER_WHITE = './resources/sprites/linksticker-white.png'
SPRITE_LINKSTICKER = './resources/sprites/linksticker.png'
SPRITE_RECENTS = './resources/sprites/recents.png'
SPRITE_SEARCHFIELD = './resources/sprites/searchfield.png'
SPRITE_URLFIELD = './resources/sprites/urlfield.png'
SPRITE_YOURSTORY = './resources/sprites/yourstory.png'

# Pyautogui's setup
pyautogui.useImageNotFoundException(True)


# The Device class
class Device:

    # --- Magic Methods ---

    # __init__
    def __init__(self,
                 device_adb:AdbDevice|None,
                 device_id:str,
                 device_name:str,
                 device_host:str,
                 device_port:int,
                 device_screen_width:int,
                 device_screen_height:int
                 ) -> None:
        
        # Instance logger setup
        self._instance_logger = logging.getLogger(__name__).getChild(self.__class__.__name__).getChild(str(device_id))

        # Validate device adb object
        if not device_adb:
            raise ValueError("Missing adb device object.")

        # Validade device id
        if not device_id:
            raise ValueError("Missing device id.")

        # Validade device name
        if not device_name:
            raise ValueError("Missing device name.")

        # Validate screen width
        if not device_screen_width:
            raise ValueError("Missing device screen width.")
        
        # Validate screen height
        if not device_screen_height:
            raise ValueError("Missing device screen height")

        # Validade device host
        if not device_host:
            raise ValueError("Missing device host ip.")
        
        # Validade device port
        if not device_port:
            raise ValueError("Missing device port.")

        # Set object attributes
        self.device_adb = device_adb
        self.device_id = device_id
        self.device_name = device_name
        self.device_screen_width = device_screen_width
        self.device_screen_height = device_screen_height
        self.device_host = device_host
        self.device_port = device_port

        # Return nothing
        return None


    # __str__
    def __str__(self) -> str:
        return f'======================== DEVICE INFO ========================\n'\
               f'device_adb:      {self.device_adb}\n'\
               f'device_id:       {self.device_id}\n'\
               f'device_name:     {self.device_name}\n'\
               f'device_scrn_res: {self.device_screen_width} x {self.device_screen_height} pixels\n'\
               f'device_address:  {self.device_host}:{self.device_port}\n'\
               f'============================================================='


    # --- Public Methods ---

    # Get Device
    @classmethod
    def get(cls,
            device_name:str = 'Generic Android Device',
            host:str = DEFAULT_ADB_HOST, 
            port:int = DEFAULT_ADB_PORT
            ):

        # Logger set up
        _get_logger = logging.getLogger(__name__).getChild(cls.__name__).getChild('get')

        _get_logger.info(f'Connecting to "{device_name}" at {host}:{port}...')

        # Connect to adb client
        _get_logger.debug(f'Connect to ADB client at {host}:{port} ...')
        client = AdbClient(host=host, port=port)
        _get_logger.debug(f'Done. (Client version: {client.version()})')

        # Connect to first available adb device
        _get_logger.debug(f'Connect to first available ADB device ...')
        try:
            device_adb = client.devices()[0]
        except IndexError:
            _get_logger.error(f'No available devices found at {host}:{port}.', exc_info=False)
            sys.exit()
        else:
            device_id = device_adb.serial
            _get_logger.debug(f'Done. (Device id: {device_id})')

        # Get device's screen width and height
        _get_logger.debug(f"Get device's screen resolution ...")
        screen_size = device_adb.shell('wm size') # e.g.: 'Physical size: [width]x[height]'
        screen_size = screen_size.replace('Physical size: ', '') # e.g.: '[width]x[height]'
        screen_width, screen_height = screen_size.split(sep='x') # e.g.: ('[width]', '[height]')
        screen_width = int(screen_width)
        screen_height = int(screen_height)
        _get_logger.debug(f'Done. (Screen resolution: {screen_width} x {screen_height} pixels)')

        _get_logger.info(f'"{device_name}" connected.')

        # Return Device object
        return cls(device_adb=device_adb,
                   device_id=device_id,
                   device_name=device_name,
                   device_host=host,
                   device_port=port,
                   device_screen_width=screen_width,
                   device_screen_height=screen_height)


    # Post Instagram Story
    def post_instagram_story(self,
                             post_image:str,
                             linksticker_url:str|None = None,
                             linksticker_custom_text:str|None = None,
                             close_friends_only:bool = True
                             ) -> None:

        self._instance_logger.info('Posting Instagram story:')

        # Push post image to device's sd card
        self._instance_logger.info(f"Pushing post image to device's sd card...")
        post_image = self._push_image_to_sdcard(post_image)

        # Launch Instagram app
        self._instance_logger.info("Launching Instagram App...")
        self._launch_instagram_app(2)

        # Click on "Add to story" button (blue circle with white cross)
        self._instance_logger.info('Creating new Instagram story post...')
        sprite_box = self._find_on_screen(SPRITE_ADDTOSTORY, '"Add to story" button', 3, 1)
        while sprite_box:
            self._input_screen_tap(sprite_box, 1)
            sprite_box = self._find_on_screen(SPRITE_ADDTOSTORY, '"Add to story" button', 1, 0)

        # Select post image from gallery
        self._instance_logger.info('Selecting post image from gallery...')
        sprite_box = self._find_on_screen(SPRITE_RECENTS, '"Recents" header')
        self._input_screen_tap(sprite_box, 0.5, 0, 300)

        # If link sticker URL provided:
        if linksticker_url:
            self._instance_logger.info('Adding link sticker...')

            # Click on "Add a sticker"
            sprite_box = self._find_on_screen(SPRITE_ADDSTICKER, '"Add sticker" button')
            self._input_screen_tap(sprite_box, 0.5)

            # Click on "Search" field and type "link"
            sprite_box = self._find_on_screen(SPRITE_SEARCHFIELD, '"Search" field')
            self._input_screen_tap(sprite_box, 0.2)
            self._input_text('link')

            # Select "LINK" sticker
            sprite_box = self._find_on_screen(SPRITE_LINKSTICKER, '"LINK" sticker')
            self._input_screen_tap(sprite_box, 0.1)

            # Input link sticker url
            self._input_text(linksticker_url)

            # If link sticker customized text provided:
            if linksticker_custom_text:

                # Click on "Customize sticker text" and input customized text
                sprite_box = self._find_on_screen(SPRITE_CUSTOMIZESTICKERTEXT, '"Customize sticker text" button')
                self._input_screen_tap(sprite_box, 0.1)
                self._input_text(linksticker_custom_text)

            # Click on "Done"
            sprite_box = self._find_on_screen(SPRITE_DONE, '"Done" button')
            self._input_screen_tap(sprite_box, 0.5)

            # Change link sticker color
            sprite_box = self._find_on_screen(SPRITE_LINKSTICKER_BLUE, 'blue link sticker')
            for _ in range(3):
                self._input_screen_tap(sprite_box, 0.4)

            # Drag link sticker to final position (bottom, center)
            self._input_screen_drag_and_drop(sprite_box, 0, 920, 2000, 1)

        # Post story to designated group
        if close_friends_only:
            self._instance_logger.info('Posting story (to Close Friends only)...')
            sprite_box = self._find_on_screen(SPRITE_CLOSEFRIENDS, '"Close Friends" button')
        else:
            self._instance_logger.info('Posting story (to all followers)...')
            sprite_box = self._find_on_screen(SPRITE_YOURSTORY, '"Your Story" button')
        self._input_screen_tap(sprite_box, 0)

        # Delete post image from device's sd card
        self._instance_logger.info("Deleting post image from device's sd card...")
        self._delete_image_from_sdcard(post_image)

        self._instance_logger.info('Instagram story posted.')

        # Return nothing
        return None


    # --- Helper Methods ---
    
    # Delete Image From SD Card
    def _delete_image_from_sdcard(self, file_path:str) -> None:
        
        # Delete file from device's SD card
        self._instance_logger.debug(f'Delete "{file_path}" ...')
        self.device_adb.shell(f'rm {file_path}')
        self._instance_logger.debug(f'Done.')

        # Return nothing
        return None


    # Find On Screen
    def _find_on_screen(self, 
                        subset_image:str, 
                        subset_image_name:str = 'subset_image', 
                        max_attempts:int = 3, 
                        time_between_attempts:int = 3,
                        confidence_lvl:float = 0.9 
                        ) -> Box|None:

        # Start attempts to find image subset in image set
        subset_image_box = None
        attempt_counter = 0
        while True:

            # Use device screencap as set image
            set_image = Image.open(fp=BytesIO(self._take_screencap()),
                                   mode='r')

            # Attempt to locate subset image in set image
            attempt_counter += 1
            self._instance_logger.debug(f"Find {subset_image_name} on screen (attempt {attempt_counter} of {max_attempts}) ...")
            try:
                subset_image_box = pyautogui.locate(needleImage=subset_image,
                                                    haystackImage=set_image,
                                                    confidence=confidence_lvl)

            # If subset image not found:
            except pyautogui.ImageNotFoundException:

                # If more attempts left, wait some time and move to next attempt
                if attempt_counter < max_attempts:
                    self._instance_logger.debug(f'Not found. (Next attempt in {time_between_attempts} seconds.)')
                    time.sleep(time_between_attempts)
                    continue

                # Else (no attempts left), stop attempting, return nothing
                else:
                    self._instance_logger.debug(f'Not found. (No attempts left.)')
                    return None

            # Else (subset image found), return subset image box
            else:
                self._instance_logger.debug(f'Found. ({subset_image_box})')
                return subset_image_box


    # Input Screen Drag-And-Drop
    def _input_screen_drag_and_drop(self, 
                                    drag_box:Box, 
                                    dx:int, 
                                    dy:int, 
                                    duration:int, 
                                    wait_time:float = 1,
                                    centered_drag:bool=False
                                    ) -> None:

        # If centered drag, get drag box's center coordinates
        if centered_drag:
            x_0 = center(drag_box).x
            y_0 = center(drag_box).y

        # Else, get random coordinates inside drag box
        else:
            x_0 = random.randint(drag_box.left, (drag_box.left + drag_box.width))
            y_0 = random.randint(drag_box.top, (drag_box.top + drag_box.height))

        # Input drag and drop on device's screen
        self._instance_logger.debug(f'Input drag-and-drop from ({x_0}, {y_0}) to ({x_0+dx}, {y_0+dy}), duration {duration} ...')
        self.device_adb.shell(f'input draganddrop {x_0} {y_0} {x_0+dx} {y_0+dy} {duration}')
        self._instance_logger.debug(f'Done.')
        
        # Wait some time (for convenience)
        time.sleep(wait_time)

        # Return nothing
        return None


    # Input Screen Tap
    def _input_screen_tap(self, 
                         tap_box:Box, 
                         wait_time:float = 1, 
                         x_offset:int = 0,
                         y_offset:int = 0,
                         centered_tap:bool = False
                         ) -> None:

        # If centered tap, get tap box's center coordinates
        if centered_tap:
            x = center(tap_box).x + x_offset
            y = center(tap_box).y + y_offset

        # Else, get random coordinates inside tap box
        else:
            x = random.randint(tap_box.left, (tap_box.left + tap_box.width)) + x_offset
            y = random.randint(tap_box.top, (tap_box.top + tap_box.height)) + y_offset

        # Input tap on device's screen
        self._instance_logger.debug(f'Input tap on ({x}, {y}) ...')
        self.device_adb.shell(f'input tap {x} {y}')
        self._instance_logger.debug('Done.')

        # Wait some time (for convenience)
        time.sleep(wait_time)

        # Return nothing
        return None


    # Input Text
    def _input_text(self, text:str='') -> None:

        # Input text
        self._instance_logger.debug(f'Input text "{text}" ...')
        self.device_adb.input_text(text)
        self._instance_logger.debug('Done.')

        # Return nothing
        return None


    # Launch Instagram App
    def _launch_instagram_app(self,
                              wait_time:float = 3,
                              force_restart:bool = True
                              ) -> None:

        # Force-stop Instagram app if force restart required
        if force_restart==True:
            self._instance_logger.debug('Force-stop Instagram app ...')
            self.device_adb.shell('am force-stop com.instagram.android')
            self._instance_logger.debug('Done.')

        # (Re-)Start Instagram app
        self._instance_logger.debug('(Re-)Start Instagram app ...')
        self.device_adb.shell('monkey -p com.instagram.android 1')
        self._instance_logger.debug('Done.')

        # Wait some time (for convenience)
        time.sleep(wait_time)

        # Return nothing
        return None


    # Push Image To SD Card
    def _push_image_to_sdcard(self, 
                              src_file_path:str, 
                              dest_folder_path:str = DEFAULT_ADB_PUSH_DESTINATION_FOLDER,
                              dest_file_name:str = DEFAULT_ADB_PUSH_DESTINATION_FILE_NAME 
                              ) -> str:
        
        # Set destination file path
        dest_file_path = f'{dest_folder_path}{dest_file_name}'

        # Push file from host machine to android device
        self._instance_logger.debug(f'Push file "{src_file_path}" to "{dest_file_path}" ...')
        self.device_adb.push(src=src_file_path, dest=dest_file_path)
        self._instance_logger.debug('Done.')

        # Make Android device "recognize" JPG file as a media file
        self._instance_logger.debug(f'Scan file "{dest_file_path}" with media scanner ...')
        self.device_adb.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{dest_file_path}')
        self._instance_logger.debug('Done.')

        # Return destination file path
        return dest_file_path


    # Take Screencap
    def _take_screencap(self, output_path:str|None = None) -> bytearray:
        
        # Take device screencap
        self._instance_logger.debug('Take device screencap ...')
        screencap = self.device_adb.screencap()
        self._instance_logger.debug('Done.')

        # If specified output path, save screencap to it
        if output_path:
            self._instance_logger.debug(f'Save screencap to {output_path} ...')
            with open(output_path, 'wb') as file:
                file.write(screencap)
            self._instance_logger.debug('Done. ')

        # Return screencap as bytearray
        return screencap

