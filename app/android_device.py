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
                 device:AdbDevice|None,
                 device_id,
                 device_name,
                 device_host,
                 device_port,
                 device_status,
                 device_screen_width,
                 device_screen_height
                 ):
        
        # Validate adb device
        if not device:
            raise ValueError("Missing adb device.")

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
        self.device = device
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
            f'device:          {self.device}\n'\
            f'device_id:       {self.device_id}\n'\
            f'device_name:     {self.device_name}\n'\
            f'device_scrn_res: {self.device_screen_width} x {self.device_screen_height} pixels\n'\
            f'device_address:  {self.device_host}:{self.device_port}\n'\
            f'device_status:   {self.device_status}\n'\
            f'============================================================='


    # Delete File In SD Card
    def delete_file_in_sdcard():
        ...


    # Find On Screen
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
        print(f'Image subset found at {subset_image_box}')

        # Return subset image's pyscreeze.Box object
        return subset_image_box


    # Launch Instagram App
    def launch_instagram_app(self, force_restart:bool = False):

        # Force-stop Instagram app if force_restart required
        if force_restart==True:
            self.device.shell('am force-stop com.instagram.android')

        # (Re-)Start Instagram app
        self.device.shell('monkey -p com.instagram.android 1')

        # Return nothing
        return None


    # Push File To SD Card
    def push_file_to_sdcard():
        ...


    # Screen Tap
    def screen_tap(self, tap_box:Box, centered_tap:bool=False):

        # If centered tap, get tap box's center coordinates
        if centered_tap:
            x = box_center(tap_box).x
            y = box_center(tap_box).y

        # Else, get random coordinates inside tap box
        else:
            x = random.randint(tap_box.left, (tap_box.left + tap_box.width))
            y = random.randint(tap_box.top, (tap_box.top + tap_box.height))

        # Input tap on device's screen
        self.device.shell(f'input tap {x} {y}')
        print(f'Screen tapped at (x, y) = ({x}, {y})')

        # Return nothing
        return None


    # Take Screenshot
    def take_screenshot(self, output_path:str|None = None):
        
        # Take device screenshot
        print(f'Taking device screenshot ... ', end='')
        screenshot = self.device.screencap()
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
def get_android_device(device_name = 'android_device',
                       host = DEFAULT_ADB_HOST, 
                       port = DEFAULT_ADB_PORT):

    # Connect to adb server
    print(f'Connecting to adb client at {host}:{port}.')
    client = AdbClient(host=host, port=port)
    print(f"AdbClient connected (ver. {client.version()}).")

    # Connect to first available device
    print(f'Looking for available devices at {host}:{port}.')
    available_devices = client.devices()
    if len(available_devices) == 0:
        raise ConnectionAbortedError(f'No available devices found at {host}:{port}.')
    print(f'Available devices: {len(available_devices)}.')
    device = available_devices[0]
    print(f'Connected to first available device (id:{device.serial}).')
    device_status = "Connected"

    # Return AndroidDevice object
    return AndroidDevice(device=device,
                         device_id=device.serial,
                         device_name=device_name,
                         device_host=host,
                         device_port=port,
                         device_status=device_status,
                         device_screen_width=1080,
                         device_screen_height=2400)
