# --- Imports ---
# Standard
from io import BytesIO
import logging
import os
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
formatter = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)
# Global Variables
DEFAULT_ADB_SERVER_IP = '127.0.0.1'
DEFAULT_ADB_SERVER_PORT = 5037
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
    def __init__(
            self,
            adb_server_ip:str,
            adb_server_port:int,
            device_adb:AdbDevice|None,
            device_serial:str,
            device_screen_width:int,
            device_screen_height:int,
            device_name:str
        ):
        """
        Initialize a Device object.

        :param adb_server_ip: ADB server IP.

        :param adb_server_port: ADB server port.

        :param device_adb: ppadb.device Device object.

        :param device_serial: Device's serial number.

        :param device_screen_width: Device's screen width (in pixels).

        :param device_screen_height: Device's screen height (in pixels).

        :param device_name: Device's name (for logging purposes only).

        :returns: None.
        """
        # Instance logger setup
        self._logger = logging.getLogger(__name__)\
                              .getChild(self.__class__.__name__)\
                              .getChild(str(device_serial))

        # Validate client ip
        if not adb_server_ip:
            raise ValueError("Missing ADB server IP.")

        # Validate client port
        if not adb_server_port:
            raise ValueError("Missing ADB server port.")

        # Validate device adb object
        if not device_adb:
            raise ValueError("Missing ADB device object.")

        # Validate device serial
        if not device_serial:
            raise ValueError("Missing device serial.")
        
        # Validate screen width
        if not device_screen_width:
            raise ValueError("Missing device screen width.")
        
        # Validate screen height
        if not device_screen_height:
            raise ValueError("Missing device screen height")

        # Validate device name
        if not device_name:
            raise ValueError("Missing device name.")

        # Set object attributes
        self.adb_server_ip = adb_server_ip
        self.adb_server_port = adb_server_port
        self.device_adb = device_adb
        self.device_serial = device_serial
        self.device_screen_width = device_screen_width
        self.device_screen_height = device_screen_height
        self.device_name = device_name


    # __str__
    def __str__(self) -> str:
        return f'---------------------- Device Info ----------------------\n'\
               f'Name: {self.device_name}\n'\
               f'Serial: {self.device_serial}\n'\
               f'Screen resolution: {self.device_screen_width} '\
                               f'by {self.device_screen_height} pixels\n'\
               f'Server address: {self.adb_server_ip}:'\
                               f'{self.adb_server_port}\n'\
               f'ppadb object: {self.device_adb}\n'\
               f'---------------------------------------------------------'


    # --- Public methods ---
    # Get Device
    @classmethod
    def get(
            cls,
            device_name:str = 'Android phone',
            adb_server_ip:str = DEFAULT_ADB_SERVER_IP,
            adb_server_port:int = DEFAULT_ADB_SERVER_PORT
        ):
        """
        Get an Android device.

        :param device_name: Device name (for human identification purposes 
            only).

        :param adb_server_ip: Host's ADB server ip.

        :param adb_server_port: Host's ADB server port.

        :returns: A Device object.
        """
        # Logger set up
        _get_logger = logging.getLogger(__name__)\
                             .getChild(cls.__name__)\
                             .getChild('get')

        _get_logger.info(f'Connecting to android device '\
                         f'at {adb_server_ip}:{adb_server_port}...')

        # Get adb client with connection to adb server
        _get_logger.debug(f'Connecting to ADB server '\
                          f'at {adb_server_ip}:{adb_server_port}...')
        client = AdbClient(host=adb_server_ip, port=adb_server_port)
        _get_logger.debug(f'Connected to ADB server.')

        # Connect to first available adb device
        _get_logger.debug(f'Connecting to first available android device ...')
        try:
            device_adb = client.devices()[0]
        except IndexError:
            _get_logger.error(
                f'Failed. No devices found '\
                f'at {adb_server_ip}:{adb_server_port}.',
                exc_info=False)
            sys.exit()
        else:
            device_serial = device_adb.serial
            _get_logger.debug(f'Connected to device '\
                              f'with serial number "{device_serial}". '\
                              f'Named device as "{device_name}".')

        # Get device's screen width and height as integers
        _get_logger.debug(f"Getting device screen resolution ...")
        screen_size = device_adb.shell('wm size')\
                                .replace('Physical size: ', '')
        screen_width, screen_height = screen_size.split(sep='x')
        screen_width = int(screen_width)
        screen_height = int(screen_height)
        _get_logger.debug(f"Device screen resolution: {screen_width} "\
                          f"by {screen_height} pixels.")
        
        _get_logger.info(f'Connected to '\
                         f'device "{device_name}" ("{device_serial}") '\
                         f'at {adb_server_ip}:{adb_server_port}.')
        
        # Return Device object
        return cls(adb_server_ip=adb_server_ip,
                   adb_server_port=adb_server_port,
                   device_adb=device_adb,
                   device_serial=device_serial,
                   device_screen_width=screen_width,
                   device_screen_height=screen_height,
                   device_name=device_name)


    # Post Instagram Story
    def post_instagram_story(
            self,
            post_image:str,
            linksticker_url:str|None = None,
            linksticker_custom_text:str|None = None,
            close_friends_only:bool = True,
            adb_push_dest_folder:str = DEFAULT_ADB_PUSH_DEST_FOLDER,
            adb_push_dest_file_name:str = DEFAULT_ADB_PUSH_DEST_FILE_NAME,
            test_call:bool = False
        ) -> None:
        """
        Post an Instagram Story with (optional) link sticker.

        :param post_image: Path to the image to be posted.

        :param linksticker_url: URL to be inserted in the link sticker. 
            If set to None, link sticker will not be added to post.

        :param linksticker_custom_text: Text to be displayed on the link 
            sticker. If set to None, default "LINK" will be displayed.

        :param close_friends_only: Whether to post to Close Friends only or 
            to all followers.

        :param adb_push_dest_folder: Folder path (inside device memory) 
            where post image file will be stored.

        :param adb_push_dest_file_name: Post image file name (inside device 
            memory).

        :param test_call: If set to True, function will do everything but 
            actually posting the story. Useful for testing.

        :returns: Nothing.
        """
        # Push post image to device's sd card
        self._logger.info(f'Pushing post image to device SD card...')
        post_image = self._push_image_to_sdcard(
            src_file_path=post_image,
            dest_file_name=adb_push_dest_file_name,
            dest_folder=adb_push_dest_folder)
        self._logger.info(f'Pushed post image to device SD card.')

        # Launch Instagram app
        self._logger.info('Launching Instagram app on android device...')
        self._launch_instagram_app(2)
        self._logger.info('Launched Instagram app.')

        # Click on "Add to story" button (blue circle with white cross)
        self._logger.info('Creating new story post...')
        sprite_box = self._find_on_screen(SPRITE_ADDTOSTORY, 
                                          '"Add to story" button', 3, 1)
        while sprite_box:
            self._input_screen_tap(sprite_box, 1)
            sprite_box = self._find_on_screen(SPRITE_ADDTOSTORY, 
                                              '"Add to story" button', 1, 0)
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
                sprite_box = self\
                    ._find_on_screen(SPRITE_CUSTOMIZESTICKERTEXT, 
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
        """
        Delete a file inside device memory.

        :param file_path: File path to be deleted.

        :returns: Nothing.
        """
        # Delete file from device's SD card
        self._logger.debug(f'Deleting "{file_path}"...')
        self.device_adb.shell(f'rm {file_path}')
        self._logger.debug(f'Deleted "{file_path}".')

        # Return nothing
        return None


    # Find on screen
    def _find_on_screen(
            self,
            search_image:str,
            search_image_name:str = 'search_image',
            max_attempts:int = 3,
            time_between_attempts:int = 3,
            confidence_lvl:float = 0.9
        ) -> Box|None:
        """
        Locate an image on device screen.

        :param search_image: File path of the image to be searched.

        :param search_image_name: Search image name (for logging purposes 
            only).

        :param max_attempts: Max search attempts.

        :param time_between_attempts: Time (in seconds) between search 
            attempts.

        :confidence_lvl: pyautogui's locate() confidence level. Leave 
            untouched if not sure.

        :returns: A pyscreeze.Box object with search image location on 
            device screen; or None, if search image not found.
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
                search_image_box = pyautogui.locate(
                    needleImage=search_image,
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
    def _input_screen_drag_and_drop(
            self,
            dnd_box:Box,
            centered_drag:bool=False,
            dx:int = 0,
            dy:int = 0,
            duration:int = 0,
            wait_time:float = 1,
        ) -> None:
        """
        Perform a screen drag-and-drop (in a straight line) on device screen.

        :param dnd_box: A pyscreeze Box object of the device screen area where
            to drag-and-drop.
        
        :param centered_drag: If set to True, drag-and-drop will start at dnd 
            box's center pixel. If set to False, drag-and-drop will start at a 
            random pixel inside dnd box area.

        :param dx: Horizontal drag (in pixels). Use positive values to drag 
            rightwards, and negative values to drag leftwards.

        :param dy: Vertical drag (in pixels). Use positive values do drag 
            downwards, and negative values to drag upwards.

        :param duration: Duration (in seconds) of the drag-and-drop action.

        :param wait_time: Idle time (in seconds) after the drag-and-drop 
            action.

        :returns: None.
        """
        # If centered drag, get drag box's center coordinates
        if centered_drag:
            x_0 = center(dnd_box).x
            y_0 = center(dnd_box).y

        # Else, get random coordinates inside drag box
        else:
            x_0 = random.randint(dnd_box.left,(dnd_box.left+dnd_box.width))
            y_0 = random.randint(dnd_box.top,(dnd_box.top+dnd_box.height))

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
    def _input_screen_tap(
            self,
            tap_box:Box,
            centered_tap:bool = False,
            xy_offset:tuple = (0, 0),
            wait_time:float = 1,
        ) -> None:
        """
        Perform a screen tap on device screen.

        :param tap_box: A pyscreeze Box object of the device screen area where
            to tap.

        :param centered_tap: If set to True, tap will occur at tap box's 
            center pixel. If set to False, tap will happen at a random pixel 
            inside tap box area.

        :param xy_offset: A tuple of ints containing offset values for X and Y 
            axes. Useful for tapping an area external but relative to the tap 
            box.

        :param wait_time: Idle time (in seconds) after the tap.

        :returns: None.
        """
        # If centered tap, get tap box's center coordinates, add offsets
        if centered_tap:
            x = center(tap_box).x + xy_offset[0]
            y = center(tap_box).y + xy_offset[1]
        # Else, get random coordinates inside tap box area, add offsets
        else:
            x = random.randint(tap_box.left,(tap_box.left+tap_box.width))\
                + xy_offset[0]
            y = random.randint(tap_box.top,(tap_box.top+tap_box.height))\
                + xy_offset[1]

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
        """"
        Input text on device.

        :param text: String of text to be inputted.

        :returns: None.
        """
        # Input text
        self._logger.debug(f'Inputting "{text}"...')
        self.device_adb.input_text(text)
        self._logger.debug(f'Inputted "{text}".')

        # Return nothing
        return None


    # Launch Instagram app
    def _launch_instagram_app(
            self,
            force_restart:bool = True,
            wait_time:float = 10
        ) -> None:
        """
        Launch Instagram App on device.

        :param force_restart: If set to True, app will be force-stopped before 
            launching.

        :param wait_time: Idle time (in seconds) after launching the app.

        :returns: None.
        """
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
    def _push_image_to_sdcard(
            self,
            src_file_path:str,
            dest_folder:str,
            dest_file_name:str,
            delete_src:bool = False
        ) -> str:
        """
        Push an image to device's SD card.

        :param src_file_path: Source file path.

        :param dest_folder: Destination folder path (in SD card).

        :param dest_file_name: Destination file name (in SD card).

        :param delete_src: If set to True, source file will be deleted after 
            push.

        :returns: Destination file path.
        """
        # Set destination file path
        dest_file_path = f'{dest_folder}{dest_file_name}'

        # Push file from host machine to android device
        self._logger.debug(f'Pushing file "{src_file_path}" '\
                           f'to "{dest_file_path}"...')
        self.device_adb.push(src=src_file_path, dest=dest_file_path)
        self._logger.debug(f'Pushed file "{src_file_path}" '\
                           f'to "{dest_file_path}".')

        # Make Android device "recognize" JPG file as a media file
        self._logger.debug(f'Scanning file "{dest_file_path}" '\
                           f'with media scanner...')
        self.device_adb.shell(f'am broadcast -a '\
                              f'android.intent.action.MEDIA_SCANNER_SCAN_FILE'\
                              f' -d file://{dest_file_path}')
        self._logger.debug(f'Scanned file "{dest_file_path}" '
                           f'with media scanner.')

        # If requested, delete source file
        if delete_src:
            os.remove(path=src_file_path)

        # Return destination file path
        return dest_file_path


    # Sleep
    def _sleep(self, wait_time:float) -> None:
        """
        Halt the execution for a specified amount of time.

        :param wait_time: Idle time (in seconds).
        """
        # Sleep for some time
        self._logger.debug(f'Sleeping for {wait_time} seconds...')
        sleep(wait_time)
        self._logger.debug(f'Slept for {wait_time} seconds.')

        # Return nothing
        return None


    # Take screencap
    def _take_screencap(self, output_path:str|None = None) -> bytearray:
        """
        Take a screencap of device's screen.

        :param output_path: Output file path. If provided, a copy of the 
            screencap will be saved to this file.

        :returns: Screencap as a bytearray object.
        """
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

