from etsyapi.core.paginatedQuery import PaginatedQuery
from requests import HTTPError
import logging
from pprint import pprint
import json

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1


class ShopListings(PaginatedQuery):
    def __init__(self, api):
        super().__init__(client=api.oauth_client)
        # TODO Need input checking

        self.api_url = api.base_url
        self.shop_name = ''

        # reference to the oauth_client
        self.oauth_client = api.oauth_client
        print(self.oauth_client)

    def shop_active_listings(self, shop_name='', params={}):

        url = '/shops/{}/listings/active'.format(shop_name)
        self.shop_name = shop_name
        self._get(self.api_url + url, params=params)
        return self


class ListingInventory:
    def __init__(self, api):
        self.api_url = api.base_url
        self.oauth_client = api.oauth_client
        self.log = logging.getLogger(__name__)

    def listing_inventory(self, listing_id):
        url = "/listings/{}/inventory".format(listing_id)
        resp = self.oauth_client.get(self.api_url + url)
        inv_dict = resp.json()
        return inv_dict['results']

    def update_inventory(self, listing_id, params):
        url = "/listings/{}/inventory".format(listing_id)
        try:
            resp = self.oauth_client.put(
                f"{self.api_url}{url}",
                data=params
            )
            # print(resp.content)
            resp.raise_for_status()
        except HTTPError as http_err:
            self.log.exception(f'HTTP error occurred: {http_err}')
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            self.log.exception(f'Other error occurred: {err}')
            print(f'Other error occurred: {err}')
        else:
            return True

