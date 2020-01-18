import time
import csv
import requests
import json
import html

from requests_oauthlib import OAuth1Session

from config import Config
from etsyapi.api import Api


def set_timestamp(epoch, filename="runtime"):
    with open(f"cache/{filename}", "w+") as f:
        f.write(str(epoch))


def get_timestamp(filename="runtime"):
    try:
        with open(f"cache/{filename}", "r+") as f:
            ts = f.read()
        return float(ts)
    except IOError:
        return False


def main():
    config = Config()

    oauth_client = OAuth1Session(
        config.client_token,
        client_secret=config.client_secret,
        resource_owner_key=config.resource_owner_key,
        resource_owner_secret=config.resource_owner_secret,
    )

    etsy = Api(config.etsy_api_url, oauth_client=oauth_client)

    last_run = get_timestamp()

    now = time.time()
    set_timestamp(now)

    receipts = etsy.receipts.all_shop_receipts('enfete', params={'min_created': last_run})

    ck_url = config.ck_api_url + f'/forms/{config.ck_script_form}/subscribe'

    unsure_names = []
    row = 0
    for receipt in receipts:
        if receipt is not None:
            if '"' in receipt['name'] or ',' in receipt['name']:
                unsure_names.append(receipt)
                continue

            url = config.ck_api_url + f'/forms/{config.ck_script_form}/subscribe'
            print(url)
            name_parts = receipt['name'].split(" ")
            subscriber_data = {
                'email': receipt['buyer_email'],
                'first_name': html.unescape(name_parts[0].title()),
                'fields': {
                    'last_purchase': time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(receipt['creation_tsz']))
                },
                'tags': ['etsy_import'],
                'api_secret': config.ck_api_secret
            }

            headers = {'Content-Type': 'application/json; charset=utf-8',
                       'user-agent': 'pyCK 0.0.1'}
            resp = requests.post(ck_url, headers=headers, data=json.dumps(subscriber_data))

        row += 1

    if len(unsure_names) > 0:
        with open("reports/unsure_names.csv", "a+") as csv_out:
            csv_writer = csv.writer(csv_out)
            for unsure_name in unsure_names:
                csv_writer.writerow([unsure_name['name'], unsure_name['buyer_email']])

    print("Exported {} receipts from Etsy".format(row))


if __name__ == "__main__":
    main()
