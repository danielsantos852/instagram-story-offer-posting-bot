# Imports
from bs4 import BeautifulSoup
import pandas as pd
import requests


# Global variables
OFFER_URL = 'https://amzn.to/4d5Ktbr'


# Main function
def main():
    
    scrape_amazon_offer(OFFER_URL)


# Scrape amazon offer function
def scrape_amazon_offer(offer_url:str) -> None:
    
    # Send HTTP GET request to offer url
    response = requests.get(url=offer_url)

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract offer title
    offer_title = soup.find(id='productTitle').get_text().strip()
    print(f'Offer title: "{offer_title}".')

    # Extract offer thumbnail

    # Extract offer "before" price

    # Extract offer "now" price

    # Return scraped data


# Call main function
if __name__=='__main__': main()