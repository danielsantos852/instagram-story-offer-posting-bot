# --- Imports ---

# Standard
from io import BytesIO
import logging
import random
import sys
from time import sleep

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
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)

# Global Variables
DEFAULT_ADB_CLIENT_IP = '127.0.0.1'
DEFAULT_ADB_LISTEN_PORT = 5037
DEFAULT_ADB_PUSH_DEST_FILE_NAME = 'image.png'
DEFAULT_ADB_PUSH_DEST_FOLDER = '/sdcard/adb-push-files/'
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


# --- The Device class ---
class Device:

    # --- Magic methods ---

    # __init__
    def __init__(self,
                 client_ip:str,
                 client_port:int,
                 device_adb:AdbDevice|None,
                 device_id:str,
                 device_screen_width:int,
                 device_screen_height:int,
                 device_name:str
                 ):
        
        # Instance logger setup
        self._logger = logging.getLogger(__name__)\
                              .getChild(self.__class__.__name__)\
                              .getChild(str(device_id))

        # Validate client ip
        if not client_ip:
            raise ValueError("Missing client ip.")

        # Validate client port
        if not client_port:
            raise ValueError("Missing client port.")

        # Validate device adb object
        if not device_adb:
            raise ValueError("Missing adb device object.")

        # Validade device id
        if not device_id:
            raise ValueError("Missing device id.")
        
        # Validate screen width
        if not device_screen_width:
            raise ValueError("Missing device screen width.")
        
        # Validate screen height
        if not device_screen_height:
            raise ValueError("Missing device screen height")

        # Validade device name
        if not device_name:
            raise ValueError("Missing device name.")

        # Set object attributes
        self.client_ip = client_ip
        self.client_port = client_port
        self.device_adb = device_adb
        self.device_id = device_id
        self.device_screen_width = device_screen_width
        self.device_screen_height = device_screen_height
        self.device_name = device_name


    # __str__
    def __str__(self) -> str:
        return f'------------------------ Device Info ------------------------\n'\
               f'Name:              {self.device_name}\n'\
               f'Serial:            {self.device_id}\n'\
               f'Screen resolution: {self.device_screen_width} by {self.device_screen_height} pixels\n'\
               f'Client address:    {self.client_ip}:{self.client_port}\n'\
               f'ppadb object:      {self.device_adb}\n'\
               f'-------------------------------------------------------------'

    # --- Public methods ---

    # Get Device
    @classmethod
    def get(cls,
            device_name:str = 'Android phone',
            client_ip:str = DEFAULT_ADB_CLIENT_IP,
            listen_port:int = DEFAULT_ADB_LISTEN_PORT
            ):
        # TODO Add a docstring

        # Logger set up
        _get_logger = logging.getLogger(__name__).getChild(cls.__name__).getChild('get')

        _get_logger.info(f'Connecting to android device at {client_ip}:{listen_port}...')

        # Connect to adb client
        _get_logger.debug(f'Connecting to ADB client at {client_ip}:{listen_port}...')
        client = AdbClient(host=client_ip, port=listen_port)
        _get_logger.debug(f'Connected to ADB client (version: {client.version()}).')

        # Connect to first available adb device
        _get_logger.debug(f'Connecting to first available android device ...')
        try:
            device_adb = client.devices()[0]
        except IndexError:
            _get_logger.error(f'Failed. No devices found at {client_ip}:{listen_port}.', exc_info=False)
            sys.exit()
        else:
            device_id = device_adb.serial
            _get_logger.debug(f'Connected to device '\
                              f'with serial number "{device_id}". '\
                              f'Named device as "{device_name}".')

        # Get device's screen width and height
        _get_logger.debug(f"Getting device screen resolution ...")
        screen_size = device_adb.shell('wm size') # returns: 'Physical size: [width]x[height]'
        screen_size = screen_size.replace('Physical size: ', '') # returns: '[width]x[height]'
        screen_width, screen_height = screen_size.split(sep='x') # returns: ('[width]', '[height]')
        screen_width = int(screen_width)
        screen_height = int(screen_height)
        _get_logger.debug(f"Device screen resolution: {screen_width} by {screen_height} pixels.")

        _get_logger.info(f'Connected to android device "{device_name}" ("{device_id}") at {client_ip}:{listen_port}.')

        # Return Device object
        return cls(client_ip=client_ip,
                   client_port=listen_port,
                   device_adb=device_adb,
                   device_id=device_id,
                   device_screen_width=screen_width,
                   device_screen_height=screen_height,
                   device_name=device_name,
                   )


    # Post Instagram Story
    def post_instagram_story(self,
                             post_image:str,
                             linksticker_url:str|None = None,
                             linksticker_custom_text:str|None = None,
                             close_friends_only:bool = True,
                             test_call:bool = False,
                             adb_push_dest_file_name:str = DEFAULT_ADB_PUSH_DEST_FILE_NAME,
                             adb_push_dest_folder:str = DEFAULT_ADB_PUSH_DEST_FOLDER
                             ) -> None:
        # TODO Add a docstring

        # Push post image to device's sd card
        self._logger.info(f'Pushing post image to device SD card...')
        post_image = self._push_image_to_sdcard(src_file_path=post_image,
                                                dest_file_name=adb_push_dest_file_name,
                                                dest_folder=adb_push_dest_folder)
        self._logger.info(f'Pushed post image to device SD card.')

        # Launch Instagram app
        self._logger.info('Launching Instagram app on android device...')
        self._launch_instagram_app(2)
        self._logger.info('Launched Instagram app.')

        # Click on "Add to story" button (blue circle with white cross)
        self._logger.info('Creating new story post...')
        sprite_box = self._find_on_screen(SPRITE_ADDTOSTORY, '"Add to story" button', 3, 1)
        while sprite_box:
            self._input_screen_tap(sprite_box, 1)
            sprite_box = self._find_on_screen(SPRITE_ADDTOSTORY, '"Add to story" button', 1, 0)
        self._logger.info('Created new story post.')

        # Select post image from gallery
        self._logger.info('Selecting post image from gallery...')
        sprite_box = self._find_on_screen(SPRITE_RECENTS, '"Recents" header')
        self._input_screen_tap(sprite_box, 0.5, 0, 300)
        self._logger.info('Selected post image from gallery.')

        # If link sticker url provided:
        if linksticker_url:

            # Click on "Add a sticker"
            self._logger.info('Adding link sticker...')
            sprite_box = self._find_on_screen(SPRITE_ADDSTICKER, 
                                              '"Add sticker" button')
            self._input_screen_tap(sprite_box, 0.5)

            # Search for link sticker
            sprite_box = self._find_on_screen(SPRITE_SEARCHFIELD, 
                                              '"Search" field')
            self._input_screen_tap(sprite_box, 0.2)
            self._input_text('link')

            # Select link sticker
            sprite_box = self._find_on_screen(SPRITE_LINKSTICKER, 
                                              '"LINK" sticker')
            self._input_screen_tap(sprite_box, 0.1)

            # Input link sticker url
            self._input_text(linksticker_url)

            # If link sticker custom text provided, use it:
            if linksticker_custom_text:
                sprite_box = self._find_on_screen(SPRITE_CUSTOMIZESTICKERTEXT, 
                                                  '"Customize sticker text" button')
                self._input_screen_tap(sprite_box, 0.1)
                self._input_text(linksticker_custom_text)

            # Click on "Done"
            sprite_box = self._find_on_screen(SPRITE_DONE, 
                                              '"Done" button')
            self._input_screen_tap(sprite_box, 0.5)

            # Change link sticker color
            sprite_box = self._find_on_screen(SPRITE_LINKSTICKER_BLUE, 
                                              'blue link sticker')
            for _ in range(3):
                self._input_screen_tap(sprite_box, 0.4)

            # Drag link sticker to final position (bottom, center)
            self._input_screen_drag_and_drop(sprite_box, 0, 920, 2000, 1)
            self._logger.info('Added link sticker.')

        # If not a test call, post story to specified public
        if not test_call:
            if close_friends_only:
                self._logger.info('Posting story to Close Friends...')
                sprite_box = self._find_on_screen(SPRITE_CLOSEFRIENDS, 
                                                  '"Close Friends" button')
            else:
                self._logger.info('Posting story to all followers...')
                sprite_box = self._find_on_screen(SPRITE_YOURSTORY, 
                                                  '"Your Story" button')
            self._input_screen_tap(sprite_box, 0)
            self._logger.info('Posted Instagram story.')
        else:
            self._logger.info('This is a test, story will not be posted.')

        # Delete post image from device's sd card
        self._logger.info('Deleting post image from device sd card...')
        self._delete_image_from_sdcard(post_image)
        self._logger.info('Deleted post image from device sd card.')

        # Return nothing
        return None


    # --- Helper methods ---
    
    # Delete image from SD card
    def _delete_image_from_sdcard(self, file_path:str) -> None:
        # TODO Add a docstring
        
        # Delete file from device's SD card
        self._logger.debug(f'Deleting "{file_path}"...')
        self.device_adb.shell(f'rm {file_path}')
        self._logger.debug(f'Deleted "{file_path}".')

        # Return nothing
        return None


    # Find on screen
    def _find_on_screen(self,
                        search_image:str,
                        search_image_name:str = 'search_image',
                        max_attempts:int = 3,
                        time_between_attempts:int = 3,
                        confidence_lvl:float = 0.9
                        ) -> Box|None:
        # TODO Improve this docstring
        """
        Locates an image on device screen.
        Returns a pyscreeze.Box object with image location; or None, if not found.
        """

        # Start attempts to find search image
        search_image_box = None
        attempt_counter = 0
        while True:

            # Take device screencap
            device_screencap = Image.open(fp=BytesIO(self._take_screencap()),
                                          mode='r')

            # Attempt to locate search image in screencap
            attempt_counter += 1
            self._logger.debug(f"Locating {search_image_name} "\
                               f"on device screen "\
                               f"(attempt {attempt_counter} "\
                               f"of {max_attempts})...")
            try:
                search_image_box = pyautogui.locate(needleImage=search_image,
                                                    haystackImage=device_screencap,
                                                    confidence=confidence_lvl)

            # If search image not found:
            except pyautogui.ImageNotFoundException:

                # If more attempts left, wait, move to next attempt
                if attempt_counter < max_attempts:
                    self._logger.debug(f'Failed. Next attempt in '\
                                       f'{time_between_attempts} seconds.')
                    self._sleep(time_between_attempts)
                    continue

                # If no attempts left, stop, return nothing
                else:
                    self._logger.debug(f'Failed. No attempts left.')
                    return None

            # If search image found, return its pyscreeze.Box object
            else:
                self._logger.debug(f'Located image at {search_image_box}')
                return search_image_box


    # Input screen drag-and-drop
    def _input_screen_drag_and_drop(self,
                                    drag_box:Box,
                                    dx:int,
                                    dy:int,
                                    duration:int,
                                    wait_time:float = 1,
                                    centered_drag:bool=False
                                    ) -> None:
        # TODO Add a docstring

        # If centered drag, get drag box's center coordinates
        if centered_drag:
            x_0 = center(drag_box).x
            y_0 = center(drag_box).y

        # Else, get random coordinates inside drag box
        else:
            x_0 = random.randint(drag_box.left,(drag_box.left+drag_box.width))
            y_0 = random.randint(drag_box.top,(drag_box.top+drag_box.height))

        # Input drag and drop on device's screen
        self._logger.debug(f'Drag-and-dropping '\
                           f'from (x,y)=({x_0},{y_0}) '\
                           f'to (x,y)=({x_0+dx},{y_0+dy}) '\
                           f'with duration={duration}...')
        self.device_adb.shell(f'input draganddrop {x_0} {y_0} '\
                              f'{x_0+dx} {y_0+dy} {duration}')
        self._logger.debug(f'Drag-and-dropped '\
                           f'from (x,y)=({x_0},{y_0}) '\
                           f'to (x,y)=({x_0+dx},{y_0+dy}) '\
                           f'with duration={duration}.')

        # Wait some time (for convenience)
        self._sleep(wait_time)

        # Return nothing
        return None


    # Input screen tap
    def _input_screen_tap(self,
                          tap_box:Box,
                          wait_time:float = 1,
                          x_offset:int = 0,
                          y_offset:int = 0,
                          centered_tap:bool = False
                          ) -> None:
        # TODO Add a docstring

        # If centered tap, get tap box's center coordinates
        if centered_tap:
            x = center(tap_box).x + x_offset
            y = center(tap_box).y + y_offset

        # Else, get random coordinates inside tap box area
        else:
            x = random.randint(tap_box.left,(tap_box.left+tap_box.width))+x_offset
            y = random.randint(tap_box.top,(tap_box.top+tap_box.height))+y_offset

        # Input tap on device's screen
        self._logger.debug(f'Tapping on (x,y)=({x},{y})...')
        self.device_adb.shell(f'input tap {x} {y}')
        self._logger.debug(f'Tapped on (x,y)=({x},{y}).')

        # Wait some time (for convenience)
        self._sleep(wait_time)

        # Return nothing
        return None


    # Input text
    def _input_text(self, text:str='') -> None:
        # TODO Add a docstring

        # Input text
        self._logger.debug(f'Inputting "{text}"...')
        self.device_adb.input_text(text)
        self._logger.debug(f'Inputted "{text}".')

        # Return nothing
        return None


    # Launch Instagram app
    def _launch_instagram_app(self,
                              wait_time:float = 3,
                              force_restart:bool = True
                              ) -> None:
        # TODO Add a docstring

        # Force-stop Instagram app if required
        if force_restart==True:
            self._logger.debug('Force-stopping Instagram app...')
            self.device_adb.shell('am force-stop com.instagram.android')
            self._logger.debug('Force-stopped Instagram app.')

        # Launch Instagram app
        self._logger.debug('Launching Instagram app...')
        self.device_adb.shell('monkey -p com.instagram.android 1')
        self._logger.debug('Launched Instagram app.')

        # Wait some time (for convenience)
        self._sleep(wait_time)

        # Return nothing
        return None


    # Push image to SD card
    def _push_image_to_sdcard(self,
                              src_file_path:str,
                              dest_file_name:str,
                              dest_folder:str
                              ) -> str:
        # TODO Add a docstring
        
        # Set destination file path
        dest_file_path = f'{dest_folder}{dest_file_name}'

        # Push file from host machine to android device
        self._logger.debug(f'Pushing file "{src_file_path}" to "{dest_file_path}"...')
        self.device_adb.push(src=src_file_path, dest=dest_file_path)
        self._logger.debug(f'Pushed file "{src_file_path}" to "{dest_file_path}".')

        # Make Android device "recognize" JPG file as a media file
        self._logger.debug(f'Scanning file "{dest_file_path}" with media scanner...')
        self.device_adb.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{dest_file_path}')
        self._logger.debug(f'Scanned file "{dest_file_path}" with media scanner.')

        # Return destination file path
        return dest_file_path


    # Sleep
    def _sleep(self, wait_time:float) -> None:
        # TODO Add a docstring
        
        # Sleep for some time
        self._logger.debug(f'Sleeping for {wait_time} seconds...')
        sleep(wait_time)
        self._logger.debug(f'Slept for {wait_time} seconds.')

        # Return nothing
        return None


    # Take screencap
    def _take_screencap(self, output_path:str|None = None) -> bytearray:
        # TODO Add a docstring
        
        # Take device screencap
        self._logger.debug('Taking device screencap...')
        screencap = self.device_adb.screencap()
        self._logger.debug('Took device screencap.')

        # If specified output path, save screencap to it
        if output_path:
            self._logger.debug(f'Saving screencap to "{output_path}"...')
            with open(output_path, 'wb') as file:
                file.write(screencap)
            self._logger.debug(f'Saved screencap to "{output_path}".')

        # Return screencap as bytearray
        return screencap

