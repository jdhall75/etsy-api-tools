from etsyapi.core import listing
from etsyapi.core import receipt
from etsyapi.core import transaction


class Api(object):
    """ Entry point for the etsy api
    url: string - etsy api url
    oauth_client: Object - fully authenticated OAuth1Session
                           object from reqeusts-oauth lib
    """

    def __init__(self, url, oauth_client=None):
        base_url = '{}/v2'.format(url if url[-1] != '/' else url[:-1])
        # self.token = token
        self.base_url = base_url
        self.oauth_client = oauth_client

        # expose classes in the api object
        self.shop_listings = listing.ShopListings(self)
        self.listing_inventory = listing.ListingInventory(self)
        self.receipts = receipt.Receipt(self)
        self.transactions = transaction.Transaction(self)
