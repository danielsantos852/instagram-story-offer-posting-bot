# Imports
from android_device import get_android_device
import time


# The Main function
def main():

    test_find_on_screen()


# Test find_on_screen() function
def test_find_on_screen():

    # Get AndroidDevice object
    phone = get_android_device()
    print(f'{phone}')

    # Find some image
    phone.find_on_screen(image_subset='./resources/00a_btn_newstory.png',
                         image_set=None,
                         confidence_lvl=0.9)


# Test pyautogui.locate() function
def test_pyautogui_locate():
    from pyautogui import locate
    box = locate(needleImage='./resources/00a_btn_newstory.png',
                 haystackImage='./resources/00_ss.png',
                 confidence=0.9)
    print(f'Image subset found at {box}')


# Call main function
if __name__=='__main__':
    main()