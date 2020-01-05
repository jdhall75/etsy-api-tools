from etsyapi.core.paginatedQuery import PaginatedQuery


class Receipt(PaginatedQuery):
    def __init__(self, api):
        super().__init__(client=api.oauth_client)
        # TODO Need input checking
        self.api_url = api.base_url
        self.shop_name = ''

    def all_shop_receipts(self, shop_name, params={}):
        url = '/shops/{}/receipts'.format(shop_name)
        self.shop_name = shop_name
        self._get(self.api_url + url, params=params)
        return self
