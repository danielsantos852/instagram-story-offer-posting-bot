# Imports
from io import BytesIO
import PIL
from ppadb.client import Client as AdbClient
from ppadb.device import Device as AdbDevice
import pyautogui
from pyscreeze import Box, center as box_center
import random


# Global variables
DEFAULT_ADB_HOST = "127.0.0.1"
DEFAULT_ADB_PORT = 5037


# The Android Device class
class AndroidDevice:
    
    # __init__ method
    def __init__(self,
                 device_adb:AdbDevice|None,
                 device_id,
                 device_name,
                 device_host,
                 device_port,
                 device_status,
                 device_screen_width,
                 device_screen_height
                 ):
        
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


    # __str__ method
    def __str__(self):
        return f'======================== DEVICE INFO ========================\n'\
            f'device_adb:      {self.device_adb}\n'\
            f'device_id:       {self.device_id}\n'\
            f'device_name:     {self.device_name}\n'\
            f'device_scrn_res: {self.device_screen_width} x {self.device_screen_height} pixels\n'\
            f'device_address:  {self.device_host}:{self.device_port}\n'\
            f'device_status:   {self.device_status}\n'\
            f'============================================================='


    # Remove a file from SD card
    def delete_file_from_sdcard():
        ...


    # Find (image) on screen
    def find_on_screen(self, image_subset, image_set=None, confidence_lvl=0.9):

        # If no image set specified:
        if not image_set:

            # Use device screenshot as image set
            image_set = PIL.Image.open(fp=BytesIO(self.take_screenshot()),
                                       mode='r')

        # Locate image subset in image set
        try:
            pyautogui.useImageNotFoundException()
            subset_image_box = pyautogui.locate(needleImage=image_subset,
                                                haystackImage=image_set,
                                                confidence=confidence_lvl)
        except pyautogui.ImageNotFoundException:
            print('Subset image not found.')
            return None
        print(f'Subset image found at {subset_image_box}')

        # Return subset image's pyscreeze.Box object
        return subset_image_box


    # Input screen drag-and-drop
    def input_screen_drag_and_drop(self, drag_box, dx, dy, duration, centered_drag:bool=False):

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


    # Input screen tap
    def input_screen_tap(self, tap_box:Box, centered_tap:bool=False):

        # If centered tap, get tap box's center coordinates
        if centered_tap:
            x = box_center(tap_box).x
            y = box_center(tap_box).y

        # Else, get random coordinates inside tap box
        else:
            x = random.randint(tap_box.left, (tap_box.left + tap_box.width))
            y = random.randint(tap_box.top, (tap_box.top + tap_box.height))

        # Input tap on device's screen
        self.device_adb.shell(f'input tap {x} {y}')
        print(f'Screen tapped at (x, y) = ({x}, {y})')

        # Return nothing
        return None


    # Launch Instagram App
    def launch_instagram_app(self, force_restart:bool = False):

        # Force-stop Instagram app if force_restart required
        if force_restart==True:
            self.device_adb.shell('am force-stop com.instagram.android')

        # (Re-)Start Instagram app
        self.device_adb.shell('monkey -p com.instagram.android 1')

        # Return nothing
        return None


    # Push a file to SD card
    def push_file_to_sdcard():
        ...


    # Take Screenshot
    def take_screenshot(self, output_path:str|None = None):
        
        # Take device screenshot
        print(f'Taking device screenshot ... ', end='')
        screenshot = self.device_adb.screencap()
        print('Done.')

        # If specified output path
        if output_path:

            # Save screenshot to output path
            with open(output_path, 'wb') as file:
                file.write(screenshot)
            print(f'Screenshot saved at {output_path}.')

        # Return screenshot as bytearray
        return screenshot


# Get Android Device
def get_android_device(device_name = 'Generic Android Device',
                       host = DEFAULT_ADB_HOST, 
                       port = DEFAULT_ADB_PORT):

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
