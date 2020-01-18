from etsyapi.core.paginatedQuery import PaginatedQuery

class Transaction(PaginatedQuery):
    def __init__(self, api):
        super().__init__(client=api.oauth_client)
        self.api_url = api.base_url
        self.oauth_client = api.oauth_client


    def get_receipt_transactions(self, receipt_id, params={}):
        url = '{}/receipts/{}/transactions'.format(self.api_url, receipt_id)
        self._get(url, params=params)
        return self
