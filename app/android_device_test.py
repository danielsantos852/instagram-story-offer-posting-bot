# Imports
from android_device import get_android_device
import time


# The Main function
def main():
    
    # Connect to phone
    phone = get_android_device(device_name='Poco X3 NFC')
    print(f'\n{phone}\n')

    # Launch Instagram app
    phone.launch_instagram_app(force_restart=True)
    time.sleep(4)

    # Take a screenshot
    print(phone.take_screenshot())


# Call main function
if __name__=='__main__':
    main()