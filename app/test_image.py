# Imports
from image import Generator
from offer import Offer


# Main function
def main():
    
    # Create a test offer post image
    test_create_offer_post_image()


# Test Generator.create_offer_post_image()
def test_create_offer_post_image():

    # Create fake Offer object
    offer = Offer(url='www.google.com',
                  title='Título do Produto',
                  thumbnail='./resources/testing/offer-thumbnail-640x640.png',
                  price_now=9999.99,
                  price_before=9999.99,
                  discount_rate=0.99)

    # Get a Generator object
    generator = Generator.get(ig_post_template_path='./resources/templates/offer-post-template-720x1280.png')

    # Create post image for fake offer
    generator.create_offer_post_image(offer=offer,
                                      output_file_name='test-offer-post-image-discount.png',
                                      output_file_folder='./temp/')

    # Remove offer's "before" price and discount rate
    offer.price_before = None
    offer.discount_rate = None

    # Create post image for fake offer (without discount)
    generator.create_offer_post_image(offer=offer,
                                      output_file_name='test-offer-post-image-no-discount.png',
                                      output_file_folder='./temp/')


# Call main function
if __name__=='__main__': main()