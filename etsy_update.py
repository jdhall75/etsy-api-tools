import json
import random

from etsyapi.api import Api
from requests_oauthlib import OAuth1Session
from config import Config
from pprint import pprint
import logging
import time
import datetime


import pathlib
import csv

SKU = 0
LISTING_ID = 1
PRODUCT_ID = 2
PHY_COUNT = 3


def get_sales(etsy, start_time=0, cache=True):

    # a dict to return sold products
    sold_products = {}

    # params to query etsy with
    params = {
        "min_created": start_time,
        "was_paid": True,
    }

    receipts_dir = pathlib.Path("cache/receipts")
    if cache:
        # if cache doesnt exist create it

        # if it doesnt exist create it
        if not receipts_dir.exists():
            receipts_dir.mkdir()

            receipts = etsy.receipts.all_shop_receipts("enfete", params=params)
            for r in receipts:
                if r is None:
                    continue
                receipt_dir = receipts_dir / str(r["receipt_id"])
                if not receipt_dir.exists():
                    receipt_dir.mkdir()
                transactions = etsy.transactions.get_receipt_transactions(
                    receipt_id=r["receipt_id"]
                )
                for t in transactions:
                    with open(
                        f"{str(receipt_dir)}/{t['transaction_id']}.json", "w+"
                    ) as t_file:
                        json.dump(t, t_file)

        transaction_files = receipts_dir.glob("**/*.json")
        for t_file in transaction_files:
            ts_data = json.loads(t_file.read_text())

            key = ts_data["product_data"]["product_id"]
            if key in sold_products.keys():
                sold_products[key] += ts_data["quantity"]
            else:
                sold_products[key] = ts_data["quantity"]

    else:
        receipts = etsy.receipts.all_shop_receipts("enfete", params=params)
        # loop over receipts and get receipt transactions
        for r in receipts:
            if r is None:
                continue
            if r["receipt_id"] is None:
                continue

            transactions = etsy.transactions.get_receipt_transactions(
                receipt_id=r["receipt_id"]
            )
            for t in transactions:
                key = t["product_data"]["product_id"]
                # update sold product with sku and and count
                if key in sold_products.keys():
                    sold_products[key] += t["quantity"]
                else:
                    sold_products[key] = t["quantity"]

    return sold_products


def get_logger():

    # create a logger by the name of main
    logger = logging.getLogger("main")

    # file and console handler
    f_handler = logging.FileHandler('logs/main.log', mode='w')
    f_handler.setLevel(logging.NOTSET)

    # handlers for console and file
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.NOTSET)

    # set the formatter
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    # add the format to the handler
    logger.addHandler(f_handler)
    logger.addHandler(c_handler)

    # return the created logger to the app for usage
    return logger


def get_listings(api, cache=False):
    if cache:
        catalog = pathlib.Path("cache/catalog")
        if not catalog.exists():
            catalog.mkdir()

            listings = api.shop_listings.shop_active_listings(
                shop_name="enfete", params={"state": "active"}
            )
            for listing in listings:
                if listing is not None:
                    listing_dir = catalog / str(listing["listing_id"])
                    listing_dir.mkdir(exist_ok=True)

                    with open(f"{listing_dir}/listing.json", "w+") as lf:
                        json.dump(listing, lf)

                    listing_inventory = api.listing_inventory.listing_inventory(
                        listing["listing_id"]
                    )
                    with open(f"{listing_dir}/products.json", "w+") as pf:
                        json.dump(listing_inventory, pf)

        # read from catalog
        listing_files = catalog.glob("**/listing.json")
        for lf in listing_files:
            with open(lf, 'r') as listing_f:
                ld = json.load(listing_f)

            product_file = catalog / str(ld['listing_id']) / "products.json"
            with open(str(product_file), "r") as f:
                ld['inventory'] = json.load(f)
            yield ld

    else:
        listings = api.shop_listings.shop_active_listings(
            shop_name="enfete", params={"state": "active"}
        )
        for listing in listings:
            if listing is not None:
                listing['inventory'] = api.listing_inventory.listing_inventory(
                    listing["listing_id"]
                )

                yield listing


def save_transaction(listing, status):
    with open('reports/updates.csv', 'a+', newline="") as csv_file:
        writer = csv.writer(csv_file)
        row = []
        ts = datetime.datetime.now()
        for product in listing['inventory']['products']:
            row.append(ts)
            row.append(status)
            row.append(listing['listing_id'])
            row.append(product['product_id'])
            row.append(product['sku'])
            row.append(product['offerings'][0]['quantity'])
            writer.writerow(row)
            row = []


if __name__ == "__main__":
    config = Config()
    client = OAuth1Session(
        config.client_token,
        client_secret=config.client_secret,
        resource_owner_key=config.resource_owner_key,
        resource_owner_secret=config.resource_owner_secret,
    )
    etsy_api = Api(config.etsy_api_url, client)

    # get all receipts from the time we last colledted an inventory report
    with open("cache/report_time.sec", "r") as rt:
        report_time = rt.read()

    # create a logger by the name of main
    logger = logging.getLogger(__name__)

    # file and console handler
    f_handler = logging.FileHandler('logs/main.log', mode='w')
    f_handler.setLevel(logging.NOTSET)

    # handlers for console and file
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.NOTSET)

    # set the formatter
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    # add the format to the handler
    logger.addHandler(f_handler)
    logger.addHandler(c_handler)
    mylog = logger

    mylog.info("hello in the file")
    mylog.warning("This is a warning on the console")

    sales = get_sales(etsy_api, start_time=report_time, cache=True)

    report = {}
    # pprint(sales)
    with open("reports/update_to_etsy_final_011520.csv", "r") as csvfile:
        report_reader = csv.reader(csvfile, quotechar='"', delimiter=",")
        count = 0
        for row in report_reader:
            print(row)
            pk = int(row[PRODUCT_ID])
            if pk in sales.keys():
                # print(pk)
                # subtract the count from PYH_COUNT
                # print("print reducing phy count")
                before = row[PHY_COUNT]
                row[PHY_COUNT] = int(row[PHY_COUNT]) - sales[pk]
                msg = f"SALES - {row[SKU]} - Sold: {sales[pk]} count before: {before}; count after: {row[PHY_COUNT]}"

                mylog.warning(msg)

                row[PHY_COUNT] = 0 if row[PHY_COUNT] < 0 else row[PHY_COUNT]

            report[pk] = {
                "SKU": row[SKU],
                "LISTING_ID": int(row[LISTING_ID]),
                "PHY_COUNT": int(row[PHY_COUNT]),
            }
            count = count + 1
    print(report)
    # read all the products files

    for listing_data in get_listings(etsy_api, cache=True):
        changed = False
        changed_listing = {}
        listing_id = ''
        products_data = listing_data['inventory']
        for product in products_data['products']:
            if product["product_id"] in report.keys():
                # if inventory count is off from etsy
                prod_quant = product["offerings"][0]["quantity"]
                report_quant = report[product["product_id"]]["PHY_COUNT"]
                # if quantities don't match then update the product
                if prod_quant != report_quant:
                    msg = f"QUANTITY - SKU: {product['sku']} report: {report_quant} etsy: {prod_quant}; CHANGING"
                    mylog.warning(msg)
                    product["offerings"][0]["quantity"] = report[product["product_id"]][
                        "PHY_COUNT"
                    ]
                    listing_id = report[product["product_id"]]["LISTING_ID"]
                    changed = True

                # if the sku doesnt match then update the SKU
                if product["sku"] != report[product["product_id"]]["SKU"]:
                    listing_id = report[product["product_id"]]["LISTING_ID"]
                    msg = f"SKU - report: {report[product['product_id']]['SKU']} etsy: {product['sku']}; CHANGING"
                    product["sku"] = report[product["product_id"]]["SKU"]
                    changed = True
                    mylog.warning(msg)
            else:
                mylog.warning(f"INVENTORY - Not found: {product['product_id']} - {product['sku']}")
        if changed:
            params = {
                "products": json.dumps(products_data['products']),
                "price_on_property": ','.join([ str(x) for x in products_data['price_on_property']]),
                "sku_on_property": ','.join([ str(x) for x in products_data['sku_on_property']]),
                "quantity_on_property": ','.join([str(x) for x in products_data['quantity_on_property']])
            }
            changed = False

            if etsy_api.listing_inventory.update_inventory(listing_id=listing_id, params=params):
                save_transaction(listing_data, 'SUCCESS')
            else:
                save_transaction(listing_data, 'FAILURE')

