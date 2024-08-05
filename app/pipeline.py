# --- Imports ---

# Standard
import logging
import os


# --- Global Configuration ---

# Logger setup
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(filename='./logs/log.log', mode='a')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)

# Global variables
DEFAULT_INPUT_TXT_FILE_CONTENT = "Paste a single offer url per line, no more, no less.\n"
DEFAULT_INPUT_TXT_FILE_PATH = './offers/input.txt'
DEFAULT_VALID_URL_PREFIXES = ['https://amzn.to/', 
                              'https://www.amazon.com.br/']


# --- The Pipeline class ---

class Pipeline:

    # --- Magic methods ---

    # __init__
    def __init__(self,
                 input_txt_file_path:str,
                 valid_url_prefixes:list
                 ) -> None:
        
        # Set object variables
        self.input_txt_file_path = input_txt_file_path
        self.valid_url_prefixes = valid_url_prefixes

        # Return nothing
        return None


    # --- Public methods ---

    # Get Pipeline
    @classmethod
    def get(cls,
            input_txt_file_path:str = DEFAULT_INPUT_TXT_FILE_PATH,
            valid_url_prefixes:list = DEFAULT_VALID_URL_PREFIXES,
            default_input_txt_file_content:str = DEFAULT_INPUT_TXT_FILE_CONTENT
            ):

        # Return Pipeline object        
        return Pipeline(input_txt_file_path=input_txt_file_path,
                        valid_url_prefixes=valid_url_prefixes)


    # Run pipeline
    def run(self):
        ...


    # Check input.txt status
    def check_input_txt(self,
                        create_if_absent:bool = True
                        ) -> str|None:

        # If file absent:
        if not os.path.exists(self.input_txt_file_path):

            # If create_if_absent is True:
            if create_if_absent:

                # Create input.txt and return path
                print(f'File "{self.input_txt_file_path}" does not exist.')
                return self.create_input_txt()
            
            # Else (create_if_absent is False), return nothing:
            else:
                return None

        # Return path to input.txt
        print(f'File "{self.input_txt_file_path}" exists.')
        return self.input_txt_file_path


    # Create input.txt
    def create_input_txt(self,
                         content:str,
                         urls:list = []
                         ) -> str:

        # If urls list provided, add urls to content
        if len(urls) > 0:
            print(f'Adding urls to file content ... ', end='')
            for url in urls:
                content = f'{content}{url}\n'
            print('Done.')

        # Create text file and write content
        print(f'Creating "{self.input_txt_file_path}" ...', end='')
        with open(self.input_txt_file_path, 'w') as file:
            file.write(content)
        print('Done.')

        # Return path to text file
        return self.input_txt_file_path


    # Parse input.txt
    def parse_input_txt(self) -> list:

        # Read input.txt lines to memory
        with open(self.input_txt_file_path, 'r') as file:
            lines = file.readlines()

        # Check each line for a valid url prefix
        valid_lines = []
        for line in lines:
            for valid_prefix in self.valid_url_prefixes:

                # If prefix found, save line, go to next line:
                if valid_prefix in line:
                    valid_lines.append(line)
                    break
        print(f'valid_lines = {valid_lines}')

        # Extract valid urls from valid lines
        valid_urls = []
        for line in valid_lines:
            valid_url = line.replace('\n','').strip()
            valid_urls.append(valid_url)
        print(f'valid_urls = {valid_urls}')

        # Return valid urls
        return valid_urls
    

    # --- Helper methods ---

