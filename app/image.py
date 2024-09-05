# --- Imports ---
# Standard
import logging
from textwrap import fill

# Third party
from PIL import Image, ImageDraw, ImageFont

# Local
from offer import Offer


# --- Global configuration ---
# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)

# Global variables
DEFAULT_FONT_PATH = './resources/fonts/open_sans.ttf'
DEFAULT_PRODUCT_NAME_MAX_LEN = 50
DEFAULT_POST_IMG_TEMPLATE = './resources/templates/story-720x1280-blue.png'
DEFAULT_OUTPUT_IMG_FOLDER = './temp/'
DEFAULT_OUTPUT_IMG_NAME = 'offer-post-image.png'


# --- The Generator class ---
class Generator:
    # --- Magic methods ---
    # __init__
    def __init__(self, post_img_template:str):
        """
        Initialize an instance of Generator class.

        :param post_img_template: File path to a post image template.

        :returns: None.
        """
        # Instance logger setup
        self._logger = logging.getLogger(__name__)\
                              .getChild(self.__class__.__name__)\

        # Validate offer post template
        if not post_img_template:
            raise ValueError('Missing post image template file path.')

        # Set instance variables
        self.post_img_template = post_img_template
    
    # --- Public methods ---
    # Get Generator
    @classmethod
    def get(cls, post_img_template:str = DEFAULT_POST_IMG_TEMPLATE):
        """
        Get a Generator instance.

        :param post_img_template: File path to a post template image.

        :returns: An instance of Generator.
        """
        # Return Generator object
        logger.info('Getting Generator object ...')
        return Generator(post_img_template=post_img_template)

    # Create an offer post image
    def create_offer_post_image(
            self,
            offer:Offer,
            output_img_folder:str = DEFAULT_OUTPUT_IMG_FOLDER,
            output_img_name:str = DEFAULT_OUTPUT_IMG_NAME
        ) -> str:
        """
        Create an offer post image for Instagram.

        :param offer: An instance of Offer (with offer data in it).

        :param output_img_folder: Path to output image folder.

        :param output_img_name: Output image file name.

        :returns: Path to output image file.
        """
        # Create new post image from template
        self._logger.info('Creating new post image from template ...')
        self._new_image_from_template()

        # Add product thumbnail to post image
        self._logger.info('Adding product thumbnail to post image ...')
        self._paste(src=offer.thumbnail,
                    x=109,
                    y=172,
                    width=502,
                    heigth=502)

        # Add price "boom" to post image
        self._logger.info('Adding price "boom" to post image...')
        self._paste(src='./resources/templates/offer-boom.png',
                    x=10,
                    y=620,
                    width=700,
                    heigth=489,
                    has_transparency=True)

        # Add product name to post image
        # TODO Some product names extrapolate price "boom" image area.
        self._logger.info('Adding product name to post image ...')
        self._insert_textbox(anchor='ma',
                             x=720/2,
                             y=745,
                             text=fill(text=offer.name,
                                       width=30,
                                       tabsize=1,
                                       break_long_words=True,
                                       break_on_hyphens=True,
                                       drop_whitespace=True,
                                       max_lines=2,
                                       placeholder=' [...]'),
                             text_font=DEFAULT_FONT_PATH,
                             text_size=35,
                             text_boldness=1,
                             text_underline=False,
                             text_strikethrough=False,
                             text_color=(0,0,0),
                             text_bg_color=None,
                             text_align='center')
        
        # Add product price to post image
        self._logger.info('Adding product price(s) to post image ...')

        if offer.price_before and offer.discount:

            # "-00%"
            # TODO Make discount be ancored/aligned to the right.
            self._insert_textbox(x=132,
                                 y=850,
                                 text=f'-{offer.get_discount(True)}',
                                 text_font=DEFAULT_FONT_PATH,
                                 text_size=60,
                                 text_color=(255,0,0))

            # "R$0.000,00"
            self._insert_textbox(x=132+150,
                                 y=850,
                                 text=f'R${offer.get_price('now')}',
                                 text_font=DEFAULT_FONT_PATH,
                                 text_size=60,
                                 text_boldness=2)
            
            # "De:"
            self._insert_textbox(x=131,
                                 y=920,
                                 text='De:',
                                 text_size=40,
                                 text_boldness=1,
                                 text_color=(84,84,84))

            # "-R$0.000,00-" (with strikethrough)
            self._insert_textbox(x=207,
                                 y=920,
                                 text=f'R${offer.get_price('before')}',
                                 text_size=40,
                                 text_strikethrough=True,
                                 text_color=(84,84,84))
        
        else:
            # "R$0000,00"
            # TODO Make it bigger and better aligned.
            self._insert_textbox(anchor='ma',
                                 x=720/2,
                                 y=858,
                                 text=f'R${offer.get_price('now')}',
                                 text_size=70,
                                 text_boldness=2)

        # Save offer image as PNG file
        self._logger.info('Saving post image as PNG file ...')
        output_file_path = self._save_image_as(output_img_folder,
                                               output_img_name)

        # Return output file path
        return output_file_path

    # --- Helper methods ---
    # Insert textbox into image
    def _insert_textbox(
            self,
            anchor:str='la',
            x:float = 0,
            y:float = 0,
            text:str = '',
            text_font:str = DEFAULT_FONT_PATH,
            text_size:float = 10,
            text_boldness:int = 0,
            text_underline:bool = False,
            text_strikethrough:bool = False,
            text_color:tuple = (0,0,0),
            text_bg_color:tuple|None = None,
            text_align:str = 'left',
        ) -> None:
        """"
        Insert a textbox into current image.

        :param anchor: ImageDraw.Draw() anchor.

        :param x: Textbox's X coordinate (in pixels).

        :param y: Textbox's Y coordinate (in pixels).

        :param text: Textbox's content text.

        :param text_font: File path to a TTF font.

        :param text_size: Size of text.

        :param text_boldness: Boldness of text. Use 0, 1, or 2.

        :param text_underline: If set to true, adds underline to text.

        :param text_strikethrough: If set to true, adds strikethrough to text.

        :param text_color: Color of text.

        :param text_bg_color: Parameter not yet implemented.

        :param text_align: Alignment of text. Use "left", "center", or "right".

        :returns: None.
        """
        self._logger.debug(f'Inserting textbox at (x,y)=({x},{y}) ...')

        # Get drawing interface
        draw = ImageDraw.Draw(im=self._current_image)

        # Set parameters
        font = ImageFont.truetype(font=text_font, 
                                  size=text_size, 
                                  encoding='unic')

        # Add text to image
        draw.text(xy=(x,y),
                  text=text,
                  fill=text_color,
                  font=font,
                  anchor=anchor,
                  align=text_align,
                  stroke_width=text_boldness)

        # Add underline and or strikethrough
        if text_underline or text_strikethrough:
            tx0, ty0, tx1, ty1 = draw.textbbox(xy=(x,y),
                                               text=text,
                                               font=font,
                                               align=text_align,
                                               stroke_width=text_boldness)
            if text_strikethrough:
                draw.line(xy=(tx0,
                              ty0+(ty1-ty0)/2,
                              tx0+(tx1-tx0),
                              ty0+(ty1-ty0)/2),
                          fill=text_color,
                          width=int(text_size/10),
                          joint='curve')
            if text_underline:
                draw.line(xy=(tx0,
                              ty0+(ty1-ty0),
                              tx0+(tx1-tx0),
                              ty0+(ty1-ty0)),
                          fill=text_color,
                          width=int(text_size/10),
                          joint='curve')

        self._logger.debug('Inserted textbox.')

        # Return nothing
        return None

    # New image from template
    def _new_image_from_template(self) -> None:
        """
        Create a new current image from a template image file in disk.

        :returns: None.
        """
        # Create new PIL Image from template
        new_image = Image.open(self.post_img_template)

        # Set new image as object current image
        self._current_image = new_image

        # Return nothing
        return None

    # Paste image into current image
    # FIXME Make this method resize images while keeping aspect ratio.
    def _paste(
            self, 
            src:str,
            x:int,
            y:int,
            width:int,
            heigth:int,
            has_transparency:bool = False
        ) -> None:
        # TODO Improve this docstring.
        """
        Paste an image to current image.

        :param src: Path to source image file.

        :param x: 
        
        :param y:
        
        :param width:
        
        :param height:

        :param has_transparency:

        :returns: None.
        """
        self._logger.debug(f'Pasting image "{src}" to self._current_image ...')

        # Load source image as PIL Image, resize it
        im_src = Image.open(fp=src)\
                      .convert(mode='RGBA')\
                      .resize(size=(width, heigth))
        
        # Paste source image into current image
        if has_transparency:
            self._current_image.paste(im=im_src, box=(x,y), mask=im_src)
        else:
            self._current_image.paste(im=im_src, box=(x,y))
        self._logger.debug('Pasted image. Returning nothing ...')

        # Return nothing
        return None

    # Save current image as
    def _save_image_as(
            self,
            dest_folder:str,
            dest_file_name:str
        ) -> str:
        """"
        Save current image to disk.

        :param dest_folder: Path to destination folder. 

        :param dest_file_name: Output file name.

        :returns: Destination file path.
        """
        # Set destination path
        output_file_path = f'{dest_folder}{dest_file_name}'

        # Save current image to output file path
        self._logger.debug(
            f'Saving self._current_image to "{output_file_path}" ...')
        self._current_image.save(fp=output_file_path)
        self._logger.debug(
            f'Saved current image to "{output_file_path}". Returning output file path ...')

        # Return destination path
        return output_file_path
