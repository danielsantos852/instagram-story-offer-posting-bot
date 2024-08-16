# Imports
from image import Generator
from offer import Offer
from test_offer import get_fake_offer


# Main function
def main():
    
    # Create a test offer post image
    test_create_offer_post_image()


# Test Generator.create_offer_post_image()
def test_create_offer_post_image():

    # Create fake offer
    offer = get_fake_offer()

    # Get a Generator object
    generator = Generator.get(offer_post_template='./resources/templates/offer-post-720x1280.png')

    # Create post image for fake offer
    generator.create_offer_post_image(offer=offer,
                                      output_img_name='test-offer-post-image-discount.png',
                                      output_img_folder='./temp/')

    # Remove offer's "before" price and discount rate
    offer.price_before = None
    offer.discount = None

    # Create post image for fake offer (without discount)
    generator.create_offer_post_image(offer=offer,
                                      output_img_name='test-offer-post-image-no-discount.png',
                                      output_img_folder='./temp/')


# Call main function
if __name__=='__main__': main()