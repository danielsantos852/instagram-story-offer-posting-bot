# --- Imports ---

# Standard
import logging
from textwrap import wrap

# Third party
from PIL import Image, ImageDraw, ImageFont


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
DEFAULT_IMAGE_OUTPUT_PATH = './temp/image.png'


# --- The Generator class ---
class Generator:

    # Class logger setup
    _class_logger = logging.getLogger(__name__).getChild(__qualname__)
    _class_logger.info('Class logger set up.')


    # --- Public methods ---

    # Create Instagram offer image
    @classmethod
    def create_instagram_offer_image(cls,
                                     template_path:str,
                                     offer_thumbnail_path:str,
                                     offer_title:str,
                                     offer_price_from:float,
                                     offer_price_for:float,
                                     dest_path:str
                                     ) -> str:
        
        # Create new offer image from template
        cls._load_image(source_path=template_path)

        # Add offer thumbnail to offer image
        cls._paste_image(source_path=offer_thumbnail_path,
                         pos_x=40,
                         pos_y=130,
                         size_x=640,
                         size_y=640)

        # Add offer title to offer image
        cls._add_offer_title(title=offer_title,
                             title_x=27.5, # (10 + 17.5)
                             title_y=827.5, # (100 + 700 + 20 + 7.5)
                             title_font_size=40,
                             title_max_length=50)

        # Add offer price to offer image
        cls._add_offer_price(price_from=offer_price_from,
                             price_to=offer_price_for,
                             price_x=27.5, # (10+17.5)
                             price_y=982.5, # (100 + 700 + 15 + 140 + 15 + 12.5)
                             price_font_size=37.5)

        # Save image as image file and return destination path
        return cls._save_image_as(dest_path=dest_path)        


    # --- Helper methods ---

    # Add offer price
    @classmethod
    def _add_offer_price(cls, 
                         price_from:float,
                         price_to:float,
                         price_x:float,
                         price_y:float,
                         price_font_size:float
                         ) -> None:
        
        # Prepare price text
        if (not price_from) or (price_from <= price_to):
            price_text = f'Por apenas R$ {f'{price_to:.2f}'.replace('.',',')}'
        else:
            price_text = f'De {f'{price_from:.2f}'.replace('.',',')} '\
                         f'por apenas {f'{price_to:.2f}'.replace('.',',')}'        

        # Add price text to offer image
        cls._insert_textbox(text=price_text,
                            x=price_x,
                            y=price_y,
                            font_size=price_font_size)

        # Return nothing
        return None


    # Add offer title to current image
    @classmethod
    def _add_offer_title(cls, 
                         title:str, 
                         title_x:float, 
                         title_y:float, 
                         title_font_size:float, 
                         title_max_length:int
                         ) -> None:
        
        # Clip offer title if it exceeds max length
        if len(title) > title_max_length:
            if title[title_max_length-4]==' ':
                title = f'{title[:title_max_length-4]}...'
            else:
                title = f'{title[:title_max_length-3]}...'

        # Break title into multiple lines
        title = '\n'.join(wrap(text=title, width=30))

        # Insert offer title into current offer image
        cls._insert_textbox(text=title,
                            x=title_x,
                            y=title_y,
                            font_size=title_font_size)

        # Return nothing
        return None


    # Insert textbox
    @classmethod
    def _insert_textbox(cls,
                        text:str,
                        x:float,
                        y:float,
                        text_align:str = 'left',
                        font_path:str = DEFAULT_FONT_PATH,
                        font_size:float = DEFAULT_FONT_SIZE
                        ) -> None:
        
        # Set the font
        text_font = ImageFont.truetype(font=font_path,
                                       size=font_size,
                                       encoding='unic')

        # Add textbox to offer image
        draw = ImageDraw.Draw(im=cls._current_image)
        draw.multiline_text(xy=(x, y),
                            text=text,
                            fill=(0, 0, 0),
                            font=text_font,
                            align=text_align,
                            stroke_width=0)

        # Return nothing
        return None


    # Load image
    @classmethod
    def _load_image(cls, source_path:str) -> None:
        
        # Load image from source path
        loaded_image = Image.open(fp=source_path)

        # Set loaded image as generator's current image
        cls._current_image = loaded_image
        
        # Return nothing
        return None


    # Paste image into current image
    @classmethod
    def _paste_image(cls, 
                     source_path:str,
                     pos_x:int,
                     pos_y:int,
                     size_x:int,
                     size_y:int
                     ) -> None:
        
        # Load source image
        source_image = Image.open(fp=source_path)

        # Resize source image 
        source_image = source_image.resize(size=(size_x, size_y))

        # Paste source image into current image
        cls._current_image.paste(im=source_image,
                                 box=(pos_x, pos_y))

        # Return nothing
        return None


    # Save current image as
    @classmethod
    def _save_image_as(cls,
                       dest_path = DEFAULT_IMAGE_OUTPUT_PATH
                       ) -> None:

        # Save current image to file path
        cls._current_image.save(fp=dest_path)

        # Return file path
        return dest_path

