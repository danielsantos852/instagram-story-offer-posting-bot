# Imports
from scraping import Scraper


# Global variables
OFFER_URLS = ['https://amzn.to/4d6pkxR',
              'https://amzn.to/4deW9Zl',
              'https://amzn.to/3WWlYry',
              'https://amzn.to/4dihsJy',
              'https://amzn.to/3WU5LmE',
              'https://amzn.to/3ymAWO7',
              'https://amzn.to/3WGDRJk',
              'https://amzn.to/4ce7GqF',
              'https://amzn.to/3YDq48Z',
              'https://amzn.to/4coLIkx',]
OFFER_URL = 'https://amzn.to/4fF1FG6'


# Main function
def main():

    # Get a scraper object
    scraper = Scraper.get()

    # Scrape offer urls
    for i in range(len(OFFER_URLS)):
        print(f'\n\nOFFER #{i+1}:')
        offer_data = scraper.scrape_amazon_offer(url=OFFER_URLS[i])
        print(offer_data)


# Call main function
if __name__=='__main__': main()