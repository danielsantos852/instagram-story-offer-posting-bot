# --- Imports ---

# Local
from android import Device as AndroidDevice
from image import Generator as ImageGenerator


# --- Main Function ---
def main():
    
    # Connect to an Android device
    phone = AndroidDevice.get(device_name='Poco X3 NFC')

    # Generate Instagram offer image
    ImageGenerator.create_instagram_offer_image(template_path='./resources/templates/story-720x1280-gray-white.png',
                                                offer_thumbnail_path='./resources/fake/offer-thumbnail-640x640.png',
                                                offer_title=f'Cool Shoes',
                                                offer_price_from=399,
                                                offer_price_for=299,
                                                dest_path=f'./temp/test-instagram-offer-image.png')

    # Post offer image on Instagram
    phone.post_instagram_story(post_image=f'./temp/test-instagram-offer-image.png',
                               linksticker_url='www.google.com',
                               linksticker_custom_text=f'ver oferta',
                               close_friends_only=True)


# Call main()
if __name__=='__main__': main()