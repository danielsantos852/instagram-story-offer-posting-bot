# Imports
from android import Device


# Main function
def main():
    
    # Post a test story to Instagram
    test_post_instagram_story()


# Test Device.post_instagram_story()
def test_post_instagram_story():
    
    # Get a Device object
    phone = Device.get(device_name='phone')

    # Post a Story
    phone.post_instagram_story(post_image='./resources/testing/offer-post-720x1280.png',
                               linksticker_url='www.google.com',
                               linksticker_custom_text='ver oferta',
                               close_friends_only=True,
                               test_call=False
                               )


# Call main function
if __name__=='__main__': main()