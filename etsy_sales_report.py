from etsyapi.api import Api
from config import Config
from requests_oauthlib import OAuth1Session
import time
import csv


def main(start_ts, end_ts):
    config = Config()

    oauth_client = OAuth1Session(
        config.client_token,
        client_secret=config.client_secret,
        resource_owner_key=config.resource_owner_key,
        resource_owner_secret=config.resource_owner_secret,
    )

    etsy = Api(config.etsy_api_url, oauth_client=oauth_client)

    params = {
        "min_created": start_ts,
        "max_created": end_ts
    }

    # dictionary to store sales
    sales_items = {}

    receipts = etsy.receipts.all_shop_receipts("enfete", params=params)

    for receipt in receipts:
        if receipt is None:
            continue
        transactions = etsy.transactions.get_receipt_transactions(receipt_id=receipt['receipt_id'])

        for transaction in transactions:
            if transaction is None:
                continue
            pid = transaction['product_data']['product_id']
            # if the item is in the sales_items keys then add the two quantities
            if pid in sales_items.keys():
                sales_items[pid]['quantity'] += transaction['quantity']
            else:
                sales_items[pid] = {'quantity': transaction['quantity'], 'sku': transaction['product_data']['sku']}


    with open('reports/jan_sales.csv', 'w+') as report_file:
        writer = csv.writer(report_file)
        writer.writerow(['product_id', 'sku', 'sold'])

        # write the sales items
        for k in sales_items.keys():
            writer.writerow([k, sales_items[k]['sku'],sales_items[k]['quantity']])


if __name__ == "__main__":
    readable_time = "31 Dec 2019 23:55:00"
    time_obj = time.strptime(readable_time, "%d %b %Y %H:%M:%S")
    start_ts = time.mktime(time_obj)

    with open('cache/report_time.sec', 'r') as ts_file:
        end_ts = ts_file.read()

    main(start_ts, end_ts)

