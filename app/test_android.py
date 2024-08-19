# Imports
from android import Device
from image import Generator
from test_offer import get_fake_offer


# Main function
def main():
    
    # Post a test story to Instagram
    test_post_instagram_story()


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
    test_phone = Device.get(device_name='test phone')

    # Post Instagram story
    test_phone.post_instagram_story(post_image=post_img,
                                    linksticker_url='www.google.com',
                                    linksticker_custom_text='ver oferta',
                                    close_friends_only=True,
                                    test_call=False)


# Call main function
if __name__=='__main__': main()