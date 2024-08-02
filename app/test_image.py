# Imports
from image import Generator


# Main Function
def main():

    # Generate a fake offer image
    Generator.create_instagram_offer_image(template_path='./resources/templates/story-720x1280-blue.png',
                                           offer_thumbnail_path='./resources/fake/offer-thumbnail-640x640.png',
                                           offer_title='Cool shoes',
                                           offer_price_from=399.99,
                                           offer_price_for=299.99,
                                           dest_path='./temp/test-offer-image.png')


# Test new image from template
def test_new_image_from_template(file_path:str):
    
    # Create new image from template
    Generator._new_image_from_template(file_path=file_path)

    # Return nothing
    return None


# Test save image as
def test_save_image_as(file_path:str) -> str:
    
    # Save generator's current image and return file path
    return Generator._save_image_as(file_path=file_path)


# Call main function
if __name__=='__main__': main()