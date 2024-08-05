# --- Imports ---

# Local
from pipeline import Pipeline


# --- Global configuration ---

# Global variables
INPUT_TXT_FILE_PATH = './offers/input.txt'
VALID_URL_PREFIXES = ['https://amzn.to/', 
                      'https://www.amazon.com.br/']


# --- Main Function ---

def main():

    # Get pipeline object
    pipeline = Pipeline.get(input_txt_file_path=INPUT_TXT_FILE_PATH,
                            valid_url_prefixes=VALID_URL_PREFIXES)

    # Run pipeline
    pipeline.run()


# Call main()
if __name__=='__main__': main()