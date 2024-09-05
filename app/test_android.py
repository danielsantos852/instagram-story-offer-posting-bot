# Imports
from android import Device
from image import Generator
from test_offer import get_fake_offer


# Main function
def main():
    
    # Test take screencap
    # test_take_screencap()

    # Test get sprite box
    # test_get_sprite_box()

    # Test find on screen
    # test_find_on_screen()

    # Post a test story to Instagram
    test_post_instagram_story()


# Get test device
def get_test_device(device_name:str = 'test_device'):
    return Device.get(device_name=device_name)


# Test Device._find_on_screen()
def test_find_on_screen():

    # Get Device instance
    print('Getting device ...')
    phone = get_test_device()

    # Launch Instagram
    print('Launching Instagram ...')
    phone._launch_instagram_app(force_restart=True,
                                wait_time=5)
    
    # Locate "Add to story" sprite
    print('Locating sprite...')
    sprite_box = phone._find_on_screen(
        sprite='./resources/sprites/addtostory.png',
        max_attempts=3,
        time_between_attempts=3,
        confidence_lvl=0.9)

    # Print box
    if sprite_box:
        print(f'Sprite fount at: {sprite_box}')
    else:
        print(f'Sprite not found.')


# Test Device._get_sprite_box()
def test_get_sprite_box():
    
    # Get Device instance
    print('Getting device ...')
    phone = get_test_device()

    # Get sprite box
    print('Getting sprite box ...')
    sprite_box = phone._get_sprite_box(
        sprite='./resources/sprites/addtostory.png',
        screencap='./resources/screencaps/00.png',
    )

    # If sprite found, print sprite box
    if sprite_box:
        print(f'sprite_box = {sprite_box}')
    # Else, print "sprite not found"
    else:
        print('Sprite not found.')


# Test Device.post_instagram_story()
def test_post_instagram_story():

    # Get fake offer
    offer = get_fake_offer()

    # Get Generator instance
    generator = Generator.get(
        post_img_template='./resources/templates/offer-post-720x1280.png')

    # Create fake offer post image
    post_img = generator.create_offer_post_image(
        offer=offer,
        output_img_folder='./temp/',
        output_img_name='offer-post-image.png')

    # Get Device instance
    phone = Device.get(device_name='phone')

    # Post Instagram story
    phone.post_instagram_story(post_image=post_img,
                               linksticker_url='www.google.com',
                               linksticker_custom_text='ver oferta',
                               close_friends_only=True,
                               test_call=True)


# Test Device._take_screencap()
def test_take_screencap():

    # Get Device instance
    phone = Device.get(device_name='phone')

    # Take device screencap
    phone._take_screencap(output_path='./temp/test-screencap.png')


# Call main function
if __name__=='__main__': main()