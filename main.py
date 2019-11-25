from requests_oauthlib import OAuth1Session
import json
from etsyapi.extras.output import ExcelWriter
import csv
from pprint import pprint

from sys import exit

from etsyapi.api import Api

# import local config
from config import Config as conf


def main():
    config = conf()

    oauth_client = OAuth1Session(config.client_token,
                                 client_secret=config.client_secret,
                                 resource_owner_key=config.resource_owner_key,
                                 resource_owner_secret=config.resource_owner_secret)

    etsy = Api(config.etsy_api_url, oauth_client=oauth_client)

    import time
    last_run = time.mktime(time.strptime('4/8/2019 15:14:00', "%m/%d/%Y %H:%M:%S"))

    receipts = etsy.receipts.all_shop_receipts('enfete', params={'min_created': last_run})

    unsure_names = []
    with open("reports/email_export.csv", 'w+') as csv_out:
        csv_writer = csv.writer(csv_out)
        row = 0
        for receipt in receipts:
            if row == 0:
                csv_writer.writerow(['First Name', 'Email'])
            if receipt is not None:
                if '"' in receipt['name'] or ',' in receipt['name']:
                    unsure_names.append(receipt)
                    continue
                name_parts = receipt['name'].split(' ')
                csv_writer.writerow([name_parts[0].title(), receipt['buyer_email'], time.ctime(receipt['creation_tsz'])])
                row += 1

    if len(unsure_names) > 0:
        with open("reports/unsure_names.csv", "w+") as csv_out:
            csv_writer = csv.writer((csv_out))
            for unsure_name in unsure_names:
                csv_writer.writerow([unsure_name['name'], unsure_name['buyer_email']])

    print("Exported {} receipts from Etsy".format(row))

    listings = etsy.shop_listings.shop_active_listings('enfete')

    count = 0

    writer = ExcelWriter.ExcelWriter('reports/etsy_stock.xlsx')

    for listing in listings:
        if count == 0:
            # writer the headers with the keys
            headers = listing.keys()
            headers = list(headers)
            writer.write_headers(headers)
            count += 1
        if listing is not None:
            # listing_inv = etsy.listing_inventory.listing_inventory(listing['listing_id'])
            # pprint(listing_inv)
            writer.write_row(listing)
            count += 1
    
    print(f"Wrote {count} lines to reports/etsy_stock.xlsx")


if __name__ == '__main__':
    main()
