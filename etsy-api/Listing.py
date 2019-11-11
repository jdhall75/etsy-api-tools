import requests


class Listing:
    def __init__(self, api_url, api_key=None):

        ## TODO Need input checking

        self.api_url = api_url
        self.api_key = api_key

        self.listings_total = 0
        self.listings_count = 0
        self.listings_in_set = 0
        self.listings = []
        self.offset = 0
        self.page = 1
        self.next_page = 2
        
    def _get_listings(self):
        self.end_point = f"/shops/{self.shop_name}/listings/active?api_key={self.api_key}&offset={self.offset}"
        self.request_url = self.api_url + self.end_point

        resp = requests.get(self.request_url)
        self.array_index = 0
        if(resp):
            data = json.loads(resp.content)
            self.listings = iter([listing for listing in data['results']])

            self.offset = data['pagination']['next_offset']
            self.listings_total = data['count']
            self.limit = data['params']['limit']
    
    def getShopActiveListings(shop_name=''):
        self.shop_name = shop_name
        self._get_listings()

    def __next__(self):
        if self.array_index < self.limit:
            # print(f"Returning a listing {self.array_index}")
            self.array_index = self.array_index + 1
            return next(self.listings)
        elif self.offset < self.listings_total:
            # print(f"Calling for next set starting with {self.offset}")
            self._get_listings()
        else:
            raise StopIteration()

    def __iter__(self):
        return self

