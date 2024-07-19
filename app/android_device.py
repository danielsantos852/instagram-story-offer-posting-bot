# Imports
from ppadb.client import Client as AdbClient


# Global variables
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5037


# The Android Device class
class AndroidDevice:
    
    # The initialization method
    def __init__(self,
                 device_id,
                 device_name,
                 device_host,
                 device_port,
                 device_status,
                 device_screen_width,
                 device_screen_height
                 ):
        
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
        self.device_id = device_id
        self.device_name = device_name
        self.device_screen_width = device_screen_width
        self.device_screen_height = device_screen_height
        self.device_host = device_host
        self.device_port = device_port
        self.device_status = device_status


    # The string method
    def __str__(self):
        return f'============ DEVICE INFO ============\n'\
            f'device_id:       {self.device_id}\n'\
            f'device_name:     {self.device_name}\n'\
            f'device_scrn_res: {self.device_screen_width} x {self.device_screen_height} pixels\n'\
            f'device_address:  {self.device_host}:{self.device_port}\n'\
            f'device_status:   {self.device_status}\n'\
            f'====================================='


# Get android device function
def get_android_device():

    # Connect to adb server
    print("Connecting to adb client...")
    client = AdbClient(host="127.0.0.1", port=5037)
    print(f"AdbClient connected (version {client.version()}).")

    # Return AndroidDevice object
    return AndroidDevice(device_id=1,
                         device_name="Poco X3 NFC",
                         device_host=DEFAULT_HOST,
                         device_port=DEFAULT_PORT,
                         device_status="Connected",
                         device_screen_width=1080,
                         device_screen_height=2400)


# Main function
def main():

    # Connect to phone
    phone = get_android_device()
    print(f'\n{phone}\n')


# Call main function
if __name__=="__main__":
    main()