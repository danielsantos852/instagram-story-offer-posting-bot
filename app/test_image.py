# Imports
from image import Generator as ImageGenerator


# Main function
def main():

    # Generate a fake offer image
    ImageGenerator.create_instagram_offer_image(
        template_path='./resources/templates/story-720x1280-gray-white.png',
        offer_thumbnail_path='./resources/fake/offer-thumbnail-640x640.png',
        offer_title='Cool shoes',
        offer_price_from=1000.00,
        offer_price_for=500.00,
        dest_path='./temp/test-offer-image.png'
    )


# Call main function
if __name__=='__main__': main()