import requests
import json

class Listing:
    def __init__(self, api):

        ## TODO Need input checking

        self.api_url = api.base_url
        self.token = api.token

        self.listings_total = 0
        self.listings = []
        self.offset = 0
        
        # url being called by the current instance
        self.request_url = ''
        self.limit = 0
        self.params = {}
        
    def _get_listings(self, url=''):
        # add api key to all requests
        self.params['api_key'] = self.token
        # build the url 
        if self.request_url == '':
            self.request_url = self.api_url + url
        print("Calling {}".format(self.request_url))
        # make the request
        resp = requests.get(self.request_url, self.params)

# reset the array_index everytime _get_listings is called
        self.array_index = 0
        
        if(resp):
            data = json.loads(resp.content)
            self.listings = iter([listing for listing in data['results']])

            self.params['offset'] = data['pagination']['next_offset']
            self.listings_total = data['count']
            self.limit = data['params']['limit']
    
    def getShopActiveListings(self, shop_name='', params=dict()):

        url = '/shops/{}/listings/active'.format(shop_name)
        self.shop_name = shop_name
        self.params = params
        self._get_listings(url)
        return self

    def __next__(self):
        if self.array_index < self.limit:
            print(f"Returning a listing {self.array_index}")
            self.array_index = self.array_index + 1
            return next(self.listings)
        elif self.offset < self.listings_total:
            print(f"Calling for next set starting with {self.params['offset']}")
            self._get_listings()
        else:
            raise StopIteration()

    def __iter__(self):
        return self

