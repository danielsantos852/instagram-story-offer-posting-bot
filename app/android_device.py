# Imports
from io import BytesIO
import PIL
from ppadb.client import Client as AdbClient
from ppadb.device import Device as AdbDevice
import pyautogui
from pyscreeze import Box, center as box_center
import random
import time


# GLOBAL VARIABLES

# Default values
DEFAULT_ADB_HOST = '127.0.0.1'
DEFAULT_ADB_PORT = 5037
DEFAULT_ADB_PUSH_DESTINATION_FOLDER = '/sdcard/adb-push-files/'
DEFAULT_ADB_PUSH_DESTINATION_FILE_NAME = 'image.png'

# Sprites
SPRITE_ADDSTICKER = './resources/sprites/addsticker.png'
SPRITE_ADDTOSTORY = './resources/sprites/addtostory.png'
SPRITE_CLOSEFRIENDS = './resources/sprites/closefriends.png'
SPRITE_CUSTOMIZESTICKERTEXT = './resources/sprites/customizestickertext.png'
SPRITE_DONE = './resources/sprites/done.png'
SPRITE_LINKSTICKER_BLACK = './resources/sprites/linksticker_black.png'
SPRITE_LINKSTICKER_BLUE = './resources/sprites/linksticker_blue.png'
SPRITE_LINKSTICKER_COLOURED = './resources/sprites/linksticker_coloured.png'
SPRITE_LINKSTICKER_WHITE = './resources/sprites/linksticker_white.png'
SPRITE_LINKSTICKER = './resources/sprites/linksticker.png'
SPRITE_RECENTS = './resources/sprites/recents.png'
SPRITE_SEARCHFIELD = './resources/sprites/searchfield.png'
SPRITE_URLFIELD = './resources/sprites/urlfield.png'
SPRITE_YOURSTORY = './resources/sprites/yourstory.png'


# The Android Device class
class AndroidDevice:
    
    # __init__ method
    def __init__(self,
                 device_adb:AdbDevice|None,
                 device_id:str,
                 device_name:str,
                 device_host:str,
                 device_port:int,
                 device_status:str,
                 device_screen_width:int,
                 device_screen_height:int
                 ) -> None:
        
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

        # Validate device status
        if not device_status:
            raise ValueError("Missing device status.")

        # Set object attributes
        self.device_adb = device_adb
        self.device_id = device_id
        self.device_name = device_name
        self.device_screen_width = device_screen_width
        self.device_screen_height = device_screen_height
        self.device_host = device_host
        self.device_port = device_port
        self.device_status = device_status

        # Return nothing
        return None


    # __str__ method
    def __str__(self) -> str:
        return f'======================== DEVICE INFO ========================\n'\
            f'device_adb:      {self.device_adb}\n'\
            f'device_id:       {self.device_id}\n'\
            f'device_name:     {self.device_name}\n'\
            f'device_scrn_res: {self.device_screen_width} x {self.device_screen_height} pixels\n'\
            f'device_address:  {self.device_host}:{self.device_port}\n'\
            f'device_status:   {self.device_status}\n'\
            f'============================================================='


    # Delete File From SD Card method
    def delete_image_from_sdcard(self, file_path:str) -> None:
        
        # Delete file from device's SD card
        print(f'Deleting {file_path} ...', end='')
        self.device_adb.shell(f'rm {file_path}')
        print('Done.')

        # Return nothing
        return None


    # Find On Screen method
    def find_on_screen(self, 
                       subset_image:str, 
                       subset_image_name:str = 'subset_image', 
                       max_attempts:int = 3, 
                       time_between_attempts:int = 2,
                       confidence_lvl:float = 0.9 
                       ) -> Box|None:

        # Start attempts to find image subset in image set
        pyautogui.useImageNotFoundException(True)
        subset_image_box = None
        attempt_counter = 0
        while True:

            # Use device screencap as set image
            set_image = PIL.Image.open(fp=BytesIO(self.take_screencap()),
                                       mode='r')

            # Attempt to locate subset image in set image
            attempt_counter += 1
            print(f'Attempting to locate {subset_image_name} (attempt #{attempt_counter}) ... ', end='')
            try:
                subset_image_box = pyautogui.locate(needleImage=subset_image,
                                                    haystackImage=set_image,
                                                    confidence=confidence_lvl)

            # If subset image not found:
            except pyautogui.ImageNotFoundException:

                # If more attempts left, wait some time and move to next attempt
                if attempt_counter < max_attempts:
                    print(f'Not found (next attempt in {time_between_attempts} seconds).')
                    time.sleep(time_between_attempts)
                    continue

                # Else (no attempts left), stop attempting, return nothing
                else:
                    print(f'Not found (no attempts left).')
                    return None

            # Else (subset image found), return subset image box
            else:
                print(f'Found at {subset_image_box}. ')
                return subset_image_box


    # Input Screen Drag-And-Drop method
    def input_screen_drag_and_drop(self, 
                                   drag_box:Box, 
                                   dx:int, 
                                   dy:int, 
                                   duration:int, 
                                   centered_drag:bool=False,
                                   wait_time:float = 1
                                   ) -> None:

        # If centered drag, get drag box's center coordinates
        if centered_drag:
            x_0 = box_center(drag_box).x
            y_0 = box_center(drag_box).y

        # Else, get random coordinates inside drag box
        else:
            x_0 = random.randint(drag_box.left, (drag_box.left + drag_box.width))
            y_0 = random.randint(drag_box.top, (drag_box.top + drag_box.height))

        # Input drag and drop on device's screen
        self.device_adb.shell(f'input draganddrop {x_0} {y_0} {x_0+dx} {y_0+dy} {duration}')
        print(f'Drag-and-drop from (x,y)=({x_0}, {y_0}) to (x,y)=({x_0+dx}, {y_0+dy}).')

        # Wait some time (for convenience)
        time.sleep(wait_time)

        # Return nothing
        return None


    # Input Screen Tap method
    def input_screen_tap(self, 
                         tap_box:Box, 
                         wait_time:float = 1, 
                         centered_tap:bool = False,
                         x_offset:int = 0,
                         y_offset:int = 0
                         ) -> None:

        # If centered tap, get tap box's center coordinates
        if centered_tap:
            x = box_center(tap_box).x + x_offset
            y = box_center(tap_box).y + y_offset

        # Else, get random coordinates inside tap box
        else:
            x = random.randint(tap_box.left, (tap_box.left + tap_box.width)) + x_offset
            y = random.randint(tap_box.top, (tap_box.top + tap_box.height)) + y_offset

        # Input tap on device's screen
        self.device_adb.shell(f'input tap {x} {y}')
        print(f'Screen tapped at (x, y) = ({x}, {y})')

        # Wait some time (for convenience)
        time.sleep(wait_time)

        # Return nothing
        return None


    # Input Text method
    def input_text(self, text:str='') -> None:

        # Input text
        self.device_adb.input_text(text)

        # Return nothing
        return None


    # Launch Instagram App method
    def launch_instagram_app(self,
                             wait_time:float = 3,
                             force_restart:bool = True
                             ) -> None:

        # Force-stop Instagram app if force restart required
        if force_restart==True:
            self.device_adb.shell('am force-stop com.instagram.android')

        # (Re-)Start Instagram app
        self.device_adb.shell('monkey -p com.instagram.android 1')

        # Wait some time (for convenience)
        time.sleep(wait_time)

        # Return nothing
        return None


    # Post Instagram Story method
    def post_instagram_story(self,
                             post_image:str,
                             add_linksticker:bool = False,
                             linksticker_url='www.google.com'
                             ) -> None:

        # Push post image to device sd card
        self.push_image_to_sdcard(post_image)

        # Launch Instagram app
        self.launch_instagram_app(2)

        # Click on "Add to story" button (blue circle with white cross)
        sprite_box = self.find_on_screen(SPRITE_ADDTOSTORY, '"Add to story" button')
        self.input_screen_tap(sprite_box, 2)

        # Select post image from gallery
        sprite_box = self.find_on_screen(SPRITE_RECENTS, '"Recents" header')
        self.input_screen_tap(sprite_box, 1, False, 0, 300)

        # Click on "Add a sticker"
        sprite_box = self.find_on_screen(SPRITE_ADDSTICKER, '"Add sticker" button')
        self.input_screen_tap(sprite_box, 1)

        # Click on "Search" field and type "link"
        sprite_box = self.find_on_screen(SPRITE_SEARCHFIELD, '"Search" field')
        self.input_screen_tap(sprite_box, 1)
        self.input_text('link')

        # Position link sticker

        # Post story

        # Delete post image from device's sd card

        # Return nothing
        print('Instagram story posted.')
        return None


    # Push Image To SD Card method
    def push_image_to_sdcard(self, 
                             src_file_path:str, 
                             dest_folder_path:str = DEFAULT_ADB_PUSH_DESTINATION_FOLDER,
                             dest_file_name:str = DEFAULT_ADB_PUSH_DESTINATION_FILE_NAME 
                             ) -> None:
        
        # Set destination file path
        dest_file_path = f'{dest_folder_path}{dest_file_name}'

        # Push file from host machine to android device
        print('Pushing image file to sdcard ...', end='')
        self.device_adb.push(src=src_file_path,
                             dest=dest_file_path)
        print('Done.')

        # Make Android device "recognize" JPG file as a media file
        print('Making image file recognizable as media file ...', end='')
        self.device_adb.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{dest_file_path}')
        print('Done.')

        # Return nothing
        return None


    # Take Screencap method
    def take_screencap(self, output_path:str|None = None) -> bytearray:
        
        # Take device screencap
        print(f'Taking device screencap ... ', end='')
        screencap = self.device_adb.screencap()
        print('Done.')

        # If specified output path, save screencap to it
        if output_path:
            print(f'Saving screencap to {output_path} ...', end='')
            with open(output_path, 'wb') as file:
                file.write(screencap)
            print('Done.')

        # Return screencap as bytearray
        return screencap


# Get Android Device function
def get_android_device(device_name:str = 'Generic Android Device',
                       host:str = DEFAULT_ADB_HOST, 
                       port:int = DEFAULT_ADB_PORT
                       ) -> AndroidDevice:

    # Connect to adb server
    print(f'Connecting to adb client at {host}:{port} ... ', end='')
    client = AdbClient(host=host, port=port)
    print(f"Connected (ver. {client.version()}).")

    # Look for available devices
    print(f'Looking for available devices ... ', end='')
    available_devices = client.devices()
    if len(available_devices) == 0:
        raise ConnectionAbortedError(f'No available devices found at {host}:{port}.')
    print(f'Found {len(available_devices)}.')
    
    # Connect to first available device and get its id/serial
    print(f'Connecting to first available device ... ', end='')
    device_adb = available_devices[0]
    device_id = device_adb.serial
    device_status = "Connected"
    print(f'{device_status} (device_id: {device_id}).')

    # Get device's screen width and height
    screen_size = device_adb.shell('wm size') # e.g.: 'Physical size: [width]x[height]'
    screen_size = screen_size.replace('Physical size: ', '') # e.g.: '[width]x[height]'
    screen_width, screen_height = screen_size.split(sep='x') # e.g.: ('[width]', '[height]')
    screen_width = int(screen_width)
    screen_height = int(screen_height)

    # Return AndroidDevice object
    return AndroidDevice(device_adb=device_adb,
                         device_id=device_id,
                         device_name=device_name,
                         device_host=host,
                         device_port=port,
                         device_status=device_status,
                         device_screen_width=screen_width,
                         device_screen_height=screen_height)
