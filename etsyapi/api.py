from etsyapi.core import listing

class Api(object):
    def __init__(self, url, token=None):
        base_url = '{}/v2'.format(url if url[-1] != '/' else url[:-1])
        self.token = token
        self.base_url = base_url
        
        self.listing = listing.Listing(self)
