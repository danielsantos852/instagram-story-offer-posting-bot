# --- Imports ---

# Standard
import time

# Third party
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


# --- Global Configuration ---

# Global variables
OFFER_URL = 'https://amzn.to/4d6pkxR' # Bike (desconto)
# OFFER_URL = 'https://amzn.to/4deW9Zl' # Kindle (no discount)


# Main function
def main():
    
    scrape_amazon_offer(OFFER_URL)


# Scrape amazon offer function
def scrape_amazon_offer(offer_url:str) -> None:
    
    # Get Chrome web driver
    print('Creating webdriver ... ', end='')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    print('Done.')
    
    # Visit offer url
    print(f'Getting {OFFER_URL} ... ', end='')
    driver.get(url=offer_url)
    time.sleep(1)
    print('Done.')

    # Get offer thumbnail
    offer_thumbnail = driver.find_element(value='imgTagWrapperId').find_element(By.TAG_NAME,value='img').get_attribute(name='src')

    # Get offer title
    print('Getting offer_title ... ', end='')
    offer_title = driver.title.split('|')[0].strip()
    print('Done.')

    # Get offer prices
    price_data = driver.find_element(value='corePriceDisplay_desktop_feature_div').text.split('\n')
    #print(f'price_data = {price_data}')

    # If offer has discount:
    if len(price_data) == 5:
        offer_price_now = float(f'{price_data[1].replace('R$','').strip()}.{price_data[2].strip()}')
        offer_price_before = float(price_data[4].replace('R$','').replace(',','.').strip())
        offer_discount_rate = float(price_data[0].replace('-','').replace('%',''))/100

    # Else, if no discount:
    elif len(price_data) == 2:
        offer_price_now = float(f'{price_data[0].replace('R$','').strip()}.{price_data[1].strip()}')
        offer_price_before = None
        offer_discount_rate = None

    # Else (data length unknown):
    else:
        raise IndexError(f'Wrong price_data length (len(price_data):{len(price_data)}).')

    # Create offer data dict
    offer_data = {
        'offer_url':offer_url,
        'offer_thumbnail':offer_thumbnail,
        'offer_title':offer_title,
        'offer_price_now':offer_price_now,
        'offer_price_before':offer_price_before,
        'offer_discount_rate':offer_discount_rate,
    }
    print(offer_data)

    # Return offer data dict
    return offer_data


# Call main function
if __name__=='__main__': main()