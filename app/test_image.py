# Imports
from image import Generator


# Main Function
def main():

    # Create new image from template
    test_new_image_from_template('./resources/templates/story_image_720x1280_base.png')

    # Save image to temp folder
    test_save_image_as(file_path='./temp/test-image.png')


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