# Imports
from ppadb.client import Client as AdbClient
from ppadb.device import Device as AdbDevice


# Global variables
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5037


# The Android Device class
class AndroidDevice:
    
    # The initialization method
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


    # The string method
    def __str__(self):
        return f'======================== DEVICE INFO ========================\n'\
            f'device:          {self.device}\n'\
            f'device_id:       {self.device_id}\n'\
            f'device_name:     {self.device_name}\n'\
            f'device_scrn_res: {self.device_screen_width} x {self.device_screen_height} pixels\n'\
            f'device_address:  {self.device_host}:{self.device_port}\n'\
            f'device_status:   {self.device_status}\n'\
            f'============================================================='


    # The Push File To SD Card method
    def push_file_to_sdcard():
        ...


    # The Launch Instagram App method
    def launch_instagram_app(self, force_restart:bool = False):

        # Force-stop Instagram app if force_restart required
        if force_restart==True:
            self.device.shell('am force-stop com.instagram.android')

        # (Re-)Start Instagram app
        self.device.shell('monkey -p com.instagram.android 1')

        # Return nothing
        return None


    # The Take Screenshot method
    def take_screenshot(self, output_path = './temp/device_screenshot.png'):
        
        # Take screenshot
        print(f'Taking device screenshot.')
        screenshot = self.device.screencap()

        # Save screenshot to output path
        with open(output_path, 'wb') as file:
            file.write(screenshot)
            f'Screenshot saved at {output_path}.'

        # Return path to output file
        return output_path


    # The Delete File In SD Card method
    def delete_file_in_sdcard():
        ...


# Get android device function
def get_android_device(device_name = 'android_device',
                       host = DEFAULT_HOST, 
                       port = DEFAULT_PORT):

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
