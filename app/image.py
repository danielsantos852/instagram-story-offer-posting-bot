# --- Imports ---

# Standard
import logging
from textwrap import wrap

# Third party
from PIL import Image, ImageDraw, ImageFont

# Local
from offer import Offer


# --- Global configuration ---

# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)


# Global variables
DEFAULT_FONT_PATH = './resources/fonts/open_sans.ttf'
DEFAULT_FONT_SIZE = 10
DEFAULT_OFFER_TITLE_MAX_LENGTH = 50
DEFAULT_OUTPUT_FILE_NAME = 'image.png'
DEFAULT_OUTPUT_FILE_FOLDER = './temp/'
DEFAULT_IG_POST_TEMPLATE_PATH = './resources/templates/story-720x1280-blue.png'


# --- The Generator class ---
class Generator:

    # --- Magic methods ---

    # __init__
    def __init__(self,
                 ig_post_template_path:str):

        # Instance logger setup
        self._logger = logging.getLogger(__name__)\
                              .getChild(self.__class__.__name__)\

        # Validade story template
        if not ig_post_template_path:
            raise ValueError('Missing Instagram post template path.')

        # Set object variables
        self.ig_post_template_path = ig_post_template_path
    
    
    # --- Public methods ---

    # Get Generator
    @classmethod
    def get(cls, 
            ig_post_template_path:str = DEFAULT_IG_POST_TEMPLATE_PATH
            ):
        # TODO Add a docstring

        # Return Generator object
        logger.info('Getting Generator object...')
        return Generator(ig_post_template_path=ig_post_template_path)


    # Create Instagram post image
    def create_ig_post_image(self,
                             offer:Offer,
                             output_file_name:str = DEFAULT_OUTPUT_FILE_NAME,
                             output_file_folder:str = DEFAULT_OUTPUT_FILE_FOLDER
                             ) -> str:
        # TODO Add a docstring

        # Create new offer image from template
        self._logger.info('Creating new post image from template...')
        self._new_image_from_template()

        # Add offer thumbnail to post image
        # FIXME Make this resize thumbnails while keeping aspect ratio
        self._logger.info('Adding offer thumbnail to post image...')
        self._paste(source_path=offer.thumbnail,
                    x=40,
                    y=130,
                    width=640,
                    heigth=640)

        # Add offer title to post image
        self._logger.info('Adding offer title to post image...')
        self._add_offer_title(x=27.5, # (10 + 17.5)
                              y=827.5, # (100 + 700 + 20 + 7.5)
                              title=offer.title,
                              title_max_length=50,
                              font_size=40,
                              text_align='left')

        # Add offer price to post image
        self._logger.info('Adding offer price to post image...')
        self._add_offer_price(x=27.5, # (10 + 17.5)
                              y=982.5, # (100 + 700 + 15 + 140 + 15 + 12.5))
                              price_now=offer.price_now,
                              price_before=offer.price_before,
                              font_size=40,
                              text_align='left')

        # Save offer image as PNG file
        self._logger.info('Saving post image as PNG file...')
        output_file_path = self._save_image_as(output_file_name,
                                               output_file_folder)

        # Return output file path
        return output_file_path


# --- Helper methods ---

    # Add offer price to current image
    def _add_offer_price(self,
                         x:float,
                         y:float,
                         price_now:float,
                         price_before:float|None = None,
                         font_size:float = DEFAULT_FONT_SIZE,
                         text_align:str = 'left'
                         ) -> None:
        # TODO Add a docstring

        # Prepare price text
        if not price_before:
            price_text = f'Por apenas R$ {f'{price_now:.2f}'.replace('.',',')}'
        else:
            price_text = f'De {f'{price_before:.2f}'.replace('.',',')} '\
                         f'por apenas {f'{price_now:.2f}'.replace('.',',')}'        

        # Add price text to offer image
        self._insert_textbox(price_text,
                             x, y,
                             font_size, 
                             text_align)
        
        # Return nothing
        return None


    # Add offer title to current image
    def _add_offer_title(self,
                         x:float,
                         y:float,
                         title:str,
                         title_max_length:int = DEFAULT_OFFER_TITLE_MAX_LENGTH,
                         font_size:float = DEFAULT_FONT_SIZE,
                         text_align:str = 'left'
                         ) -> None:
        # TODO Add a docstring

        # Clip offer title if it exceeds max length
        self._logger.debug(f'Clipping offer title "{title}" '\
                           f'to max length ({title_max_length})...')
        if len(title) > title_max_length:
            if title[title_max_length-4]==' ':
                title = f'{title[:title_max_length-4]}...'
            else:
                title = f'{title[:title_max_length-3]}...'

        # Break title into multiple lines
        title = '\n'.join(wrap(text=title, width=30))
        self._logger.debug(f'Clipped offer title to "{title}".')

        # Insert offer title into current offer image
        self._insert_textbox(title, 
                             x, y, 
                             font_size, 
                             text_align)

        # Return nothing
        return None


    # Insert textbox
    def _insert_textbox(self,
                        text:str,
                        x:float,
                        y:float,
                        font_size:float = DEFAULT_FONT_SIZE,
                        text_align:str = 'left',
                        font_path:str = DEFAULT_FONT_PATH,
                        ) -> None:
        # TODO Add a docstring
        
        # Set the font
        text_font = ImageFont.truetype(font=font_path,
                                       size=font_size,
                                       encoding='unic')

        # Add textbox to offer image
        self._logger.debug(f'Inserting textbox at (x,y)=({x}, {y}) '\
                           f'with text "{text}"...')
        draw = ImageDraw.Draw(im=self._current_image)
        draw.multiline_text(xy=(x, y),
                            text=text,
                            fill=(0, 0, 0),
                            font=text_font,
                            align=text_align,
                            stroke_width=0)
        self._logger.debug('Inserted textbox.')

        # Return nothing
        return None


    # New image from template
    def _new_image_from_template(self) -> None:
        # TODO Add a docstring

        # Create new PIL Image from template
        new_image = Image.open(self.ig_post_template_path)

        # Set new image as object current image
        self._current_image = new_image

        # Return nothing
        return None


    # Paste image into current image
    def _paste(self, 
               source_path:str,
               x:int,
               y:int,
               width:int,
               heigth:int
               ) -> None:
        # TODO Add a docstring

        # Load source image as PIL Image
        im_src = Image.open(fp=source_path)

        # Resize source image
        im_src = im_src.resize(size=(width, heigth))
        
        # Paste source image into current image
        self._current_image.paste(im=im_src, box=(x,y))

        # Return nothing
        return None


    # Save current image as
    def _save_image_as(self,
                       output_file_name:str = DEFAULT_OUTPUT_FILE_NAME,
                       output_file_folder:str = DEFAULT_OUTPUT_FILE_FOLDER,
                       ) -> str:
        # TODO Add a docstring

        # Set destination path
        output_file_path = f'{output_file_folder}{output_file_name}'

        # Save current image to output file path
        self._logger.debug(f'Saving current image to "{output_file_path}"...')
        self._current_image.save(fp=output_file_path)
        self._logger.debug('Saved current image. Return output file path.')

        # Return destination path
        return output_file_path

