# Imports
from offer import Offer


# Main function
def main():
    
    # Test Offer.get_price()
    test_get_price()

    # Test Offer.get_discount()
    test_get_discount()


# Get fake offer
# TODO Insert this function into Offer class
def get_fake_offer() -> Offer:
    return Offer.get(
        url='www.google.com',
        name='Novo tênis Fancy Pro V2 Vintage Kombi Juntos e Shallow Now '\
             'TODOS OS TAMANHOS',
        thumbnail='./resources/testing/product-thumbnail-640x640.png',
        price_now=9999.99,
        price_before=9999.99,
        discount=0.99)


# Test Offer.get_price()
def test_get_price():
    
    # Create fake offer
    offer = get_fake_offer()

    # Get "now" price as float
    price_now_float = offer.get_price('now', False)
    print(f'price_now_float = {price_now_float}')

    # Get "before" price as str
    price_before_str = offer.get_price('before', True)
    print(f'price_before_str = {price_before_str}')


# Test Offer.get_discount()
def test_get_discount():

    # Create fake offer
    offer = get_fake_offer()

    # Get discount rate as float
    discount_float = offer.get_discount(False)
    print(f'discount_float = {discount_float}')

    # Get discount rate as str
    discount_str = offer.get_discount(True)
    print(f'discount_str = {discount_str}')


# Call main function
if __name__=='__main__': main()