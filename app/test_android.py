# Imports
from android import Device as AndroidDevice


# Main function
def main():
    
    # Get Android device
    phone = AndroidDevice.get('phone')
    
    # Post a test Instagram Story
    phone.post_instagram_story(post_image='./resources/templates/story-720x1280-gray-white.png',
                               linksticker_url='www.google.com',
                               linksticker_custom_text='ver oferta',
                               close_friends_only=True,
                               test_call=True)


# Call main function
if __name__=='__main__': main()