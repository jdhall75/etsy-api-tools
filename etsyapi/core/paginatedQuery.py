import json


class PaginatedQuery:
    def __init__(self, client=None):
        if client is not None:
            self.oauth_client=client

        self.results_total = 0
        self.results = []
        self.limit = 0
        self.params = {}
        self.request_url = ''

    def _get(self, url='', params={}):
        # add api key to all requests
        if len(params) > 0:
            self.params.update(params)

        if url != '':
            self.request_url = url

        if len(self.params) > 0:
            print("Calling {} with params={}".format(self.request_url, self.params))
            resp = self.oauth_client.get(self.request_url, params=self.params)
        else:
            print("Calling {}".format(self.request_url))
            resp = self.oauth_client.get(self.request_url)

        # reset the array_index every time _get_listings is called
        self.array_index = 0

        if resp:
            data = json.loads(resp.content)
            self.results = iter([result for result in data['results']])


            self.params['offset'] = data['pagination']['next_offset']
            self.results_total = data['count']
            self.limit = data['params']['limit']

    def __next__(self):
        if self.array_index < self.limit:
            self.array_index = self.array_index + 1
            return next(self.results)
        elif self.params['offset'] is None:
            raise StopIteration
        elif self.params['offset'] < self.results_total:
            self._get()
        else:
            raise StopIteration()

    def __iter__(self):
        return self
