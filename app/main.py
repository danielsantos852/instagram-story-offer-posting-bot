# --- Imports ---

# Local
from android import Device as AndroidDevice
from image import Generator as ImageGenerator


# --- Main Function ---
def main():
    
    # Connect phone to host machine
    phone = AndroidDevice.get(device_name='Poco X3 NFC')

    # Do this 50 times
    for i in range(50):

        # Generate Instagram offer image
        ImageGenerator.create_instagram_offer_image(template_path='./resources/templates/story-720x1280-gray-white.png',
                                                    offer_thumbnail_path='./resources/fake/offer-thumbnail-640x640.png',
                                                    offer_title=f'Cool Shoes V{i}',
                                                    offer_price_from=1000,
                                                    offer_price_for=i,
                                                    dest_path=f'./temp/test-instagram-offer-image-{i}.png')

        # Post offer image on Instagram
        phone.post_instagram_story(post_image=f'./temp/test-instagram-offer-image-{i}.png',
                                   linksticker_url='www.google.com',
                                   linksticker_custom_text=f'ver oferta #{i}',
                                   close_friends_only=True)


# Call main()
if __name__=='__main__': main()