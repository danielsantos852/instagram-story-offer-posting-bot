# Imports
from android_device import AndroidDevice, get_android_device


# The Main function
def main():

    # Get AndroidDevice object
    phone = test_get_android_device()

    # Push a file to device sd card
    test_push_image_to_sdcard(phone)

    input('Press any key to continue...')

    # Delete file from sd card
    test_delete_image_from_sdcard(phone)


# Get Android Device test
def test_get_android_device(device_name:str = 'test_android_device') -> AndroidDevice:

    # Get AndroidDevice object
    phone = get_android_device(device_name=device_name)
    print(f'{phone}')

    # Return AndroidDevice object
    return phone


# Delete Image From SD Card test
def test_delete_image_from_sdcard(device:AndroidDevice):

    # Delete test image file from default adb push destination folder
    device.delete_image_from_sdcard(file_path='/sdcard/adb-push-files/test-adb-push-image.png')

    # Return nothing
    return None


# Find On Screen test
def test_find_on_screen(device:AndroidDevice):

    # Launch Instagram app
    device.launch_instagram_app(force_restart=True)

    # Find "Add to story" button on screen
    box = device.find_on_screen(subset_image='./resources/00a_btn_addtostory.png',
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

    # Find "Add Story" button on screen
    add_story_button = phone.find_on_screen(image_subset='./resources/00a_btn_newstory.png')

    # Tap on button box
    phone.input_screen_tap(tap_box=add_story_button)


# Post Instagram Story test
def test_post_instagram_story(device:AndroidDevice):

    # Post Instagram story
    device.post_instagram_story()


# Push File To SD Card test
def test_push_image_to_sdcard(device:AndroidDevice):
    
    # Push test file to default adb push destination folder
    device.push_image_to_sdcard(src_file_path='./resources/templates/story_image_720x1280_blank.png',
                                dest_file_name='test-adb-push-image.png')

    # Return nothing
    return None


# Take Screenshot test
def test_take_screencap(device:AndroidDevice):

    # Take device screenshot
    device.take_screencap(output_path='./temp/test_screencap.png')


# Call main function
if __name__=='__main__':
    main()