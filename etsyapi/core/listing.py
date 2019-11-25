from etsyapi.core.paginatedQuery import PaginatedQuery


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

    def listing_inventory(self, listing_id):
        url = "/listings/{}/inventory".format(listing_id)
        resp = self.oauth_client.get(self.api_url + url)

        return resp.json()
