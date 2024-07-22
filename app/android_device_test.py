# Imports
from android_device import get_android_device
import pyscreeze
import time


# The Main function
def main():

    test_get_android_device()


# Get Android Device Test
def test_get_android_device():

    # Get AndroidDevice object
    phone = get_android_device()
    print(f'\n{phone}\n')
    return True


# Test Find On Screen
def test_find_on_screen():

    # Get AndroidDevice object
    phone = get_android_device()

    # Find some image
    box = phone.find_on_screen(image_subset='./resources/00a_btn_newstory.png',
                               image_set=None,
                               confidence_lvl=0.9)

    print(box)
    print(type(box))


# Test Screen Tap
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


# Test pyautogui.locate()
def test_pyautogui_locate():
    from pyautogui import locate
    box = locate(needleImage='./resources/00a_btn_newstory.png',
                 haystackImage='./resources/00_ss.png',
                 confidence=0.9)
    print(f'Image subset found at {box}')


# Call main function
if __name__=='__main__':
    main()