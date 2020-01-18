#!/home/jdhall/.venvs/etsy-api-tools/bin/python -u
from etsyapi.extras.output import ExcelWriter
from requests_oauthlib import OAuth1Session
from woocommerce import API
import argparse
import time
import urllib

# Uncomment to inspect data
# from pprint import pprint

from etsyapi.api import Api

# import local config
from config import Config as conf


def get_tstamp():
    t = time.localtime()
    return f"{t.tm_year}-{t.tm_mon}-{t.tm_mday}-{t.tm_hour}{t.tm_min}"


def woo_report(config):

    wcapi = API(
        url="https://enfete.com",
        consumer_key=config.woo_consumer_key,
        consumer_secret=config.woo_consumer_secret,
        version="wc/v3",
    )

    filename = f"woo_stock-{get_tstamp()}.xlsx"
    writer = ExcelWriter.ExcelWriter(f"reports/{filename}")

    writer.add_sheet(sheet_name="woo_products")
    writer.add_sheet(sheet_name="woo_variations")

    woo_products = []
    params = {"per_page": 50}

    def get_product_variations(product_id=0):
        interesting_data = [
            "id",
            "status",
            "sku",
            "description",
            "manage_stock",
            "product_id",
        ]
        return_variations = []
        vari = {}
        url = f"products/{product_id}/variations"
        local_variations = wcapi.get(url).json()
        # print(local_variations)
        # filter all the data we dont care about
        for v in local_variations:
            for key in v.keys():
                if key in interesting_data:
                    vari[key] = v[key]
            for meta in v["meta_data"]:
                if meta["key"] == "_etsy_id":
                    vari["etsy_id"] = meta["value"]
                if meta["key"] == "_etsy_variation_id":
                    vari["etsy_variation_id"] = meta["value"]

            return_variations.append(vari.copy())

        return return_variations

    def woo_get_products(url="", params={}):
        """ call woocommerce site for all the products"""
        interesting_data = [
            "id",
            "name",
            "slug",
            "type",
            "status",
            "sku",
            "manage_stock",
        ]

        resp = wcapi.get(url, params=params)
        products_list = resp.json()

        # call for all the variations for the product
        # append it to the products list
        for p in products_list:
            prod = {}

            # if there are variations in this listing retrieve them and replace
            # the var with the results of the query
            if len(p["variations"]) > 0:
                prod["variations"] = get_product_variations(p["id"])
            else:
                prod["variations"] = []
            # copy over keys that we care about
            for key in p.keys():
                if key in interesting_data:
                    prod[key] = p[key]

            # find the etsy id in the meta_data array
            for meta in p["meta_data"]:
                if meta["key"] == "_etsy_id":
                    prod["etsy_id"] = meta["value"]
            # print(prod)
            woo_products.append(prod.copy())

        # if there is a next url then adjust the params and call for
        # the next page
        if "next" in resp.links.keys():
            next_page = urllib.parse.urlparse(resp.links["next"]["url"]).query.split(
                "="
            )
            params["page"] = next_page[2]
            woo_get_products("products", params=params)

    woo_get_products(url="products", params=params)
    prod_count = 0
    for prod in woo_products:
        if prod_count == 0:
            # writer the headers with the keys
            writer.write_headers(list(prod.keys()), sheet_name="woo_products")
            prod_count += 1
        if prod is not None:
            variations = prod["variations"]
            del prod["variations"]
            writer.write_row(prod, sheet_name="woo_products")

            v_counter = 0
            for v in variations:
                if v_counter == 0:
                    writer.write_headers(list(v.keys()), sheet_name="woo_variations")
                    v_counter += 1
                writer.write_row(v, sheet_name="woo_variations")
                v_counter += 1


def etsy_report(config):
    oauth_client = OAuth1Session(
        config.client_token,
        client_secret=config.client_secret,
        resource_owner_key=config.resource_owner_key,
        resource_owner_secret=config.resource_owner_secret,
    )

    etsy = Api(config.etsy_api_url, oauth_client=oauth_client)

    listings = etsy.shop_listings.shop_active_listings("enfete")

    inv_count = 0
    count = 0

    filename = f"etsy_stock-{get_tstamp()}.xlsx"
    writer = ExcelWriter.ExcelWriter(f"reports/{filename}")

    writer.add_sheet(sheet_name="etsy_listings")
    writer.add_sheet(sheet_name="etsy_listing_product")

    # processing for etsy listings
    for listing in listings:
        if count == 0:
            # writer the headers with the keys
            headers = listing.keys()
            headers = list(headers)
            writer.write_headers(headers, sheet_name="etsy_listings")
            count += 1
        if listing is not None:
            # if list['has_variations']:
            listing_inv = etsy.listing_inventory.listing_inventory(
                listing["listing_id"]
            )

            for li in listing_inv['products']:
                if li["is_deleted"] == 1:
                    continue
                prod = {
                    "sku": li["sku"],
                    "listing_id": listing["listing_id"],
                    "product_id": li["product_id"],
                    "title": listing["title"],
                }

                if len(li["offerings"]) == 1:
                    prod["price"] = li["offerings"][0]["price"][
                        "currency_formatted_short"
                    ]
                    prod["quantity"] = li["offerings"][0]["quantity"]
                else:
                    pprint(li)

                li["listing_id"] = listing["listing_id"]
                if inv_count == 0:
                    writer.write_headers(
                        list(prod.keys()), sheet_name="etsy_listing_product"
                    )
                    inv_count += 1
                writer.write_row(prod, sheet_name="etsy_listing_product")
                inv_count += 1
                time.sleep(0.1)

            writer.write_row(listing, sheet_name="etsy_listings")
            count += 1

    print(f"Wrote {count} lines to reports/{filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments for report runner")
    parser.add_argument(
        "--report", action="append", help="report to run, options: etsy, woo"
    )
    args = parser.parse_args()

    config = conf()

    if "etsy" in args.report:
        etsy_report(config)
    if "woo" in args.report:
        woo_report(config)
