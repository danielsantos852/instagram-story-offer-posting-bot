# Imports
from android_device import get_android_device
import pyscreeze
import time


# The Main function
def main():

    test_find_on_screen()


# Get Android Device Test
def test_get_android_device():

    # Get AndroidDevice object
    phone = get_android_device()
    print(f'\n{phone}\n')
    return True


# Find On Screen test
def test_find_on_screen():

    # Get AndroidDevice object
    phone = get_android_device(device_name='Poco X3 NFC')

    # Launch Instagram app
    phone.launch_instagram_app(force_restart=True)

    # Find "Add to story" button on screen
    box = phone.find_on_screen(subset_image='./resources/00a_btn_addtostory.png',
                               subset_image_name='"Add to story" button',
                               confidence_lvl=0.9,
                               max_attempts=5,
                               time_between_attempts=3)


# Screen Drag-And-Drop test
def test_input_screen_drag_and_drop():
    
    # Get an Android device
    phone = get_android_device(device_name='Poco X3 NFC')

    # Find link sticker icon on device screen
    sticker_box = phone.find_on_screen(image_subset='./resources/08a_ico_linksticker_blue.png')

    # Drag sticker down
    phone.input_screen_drag_and_drop(drag_box=sticker_box,
                                     dx=0,
                                     dy=920,
                                     duration=2000,
                                     centered_drag=False)


# Screen Tap test
def test_input_screen_tap():

    # Get AndroidDevice object
    phone = get_android_device()

    # Launch Instagram app and wait a bit
    phone.launch_instagram_app(force_restart=True)
    time.sleep(4)

    # Find "Add Story" button on screen
    add_story_button = phone.find_on_screen(image_subset='./resources/00a_btn_newstory.png')

    # Tap on button box
    phone.input_screen_tap(tap_box=add_story_button)


# Call main function
if __name__=='__main__':
    main()