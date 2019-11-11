import requests
import json
import csv

from etsyapi.api import Api

# import local config
from config import Config as conf



def main():
    config = conf()
    etsy = Api(config.etsy_api_url, config.api_token)

    listings = etsy.listing.getShopActiveListings('enfete')
    
    out_file = open("reports/active_products.csv", "w")
    csv_writer = csv.writer(out_file)

    count = 0

    for listing in listings: 
        if count == 0:
            # writer the headers with the keys
            headers = listing.keys()
            csv_writer.writerow(headers)
            count += 1
        if listing is not None:
            csv_writer.writerow(listing.values())
            count += 1
    
    out_file.close()
    print(f"Wrote {count} lines to reports/active_products.csv") 


if __name__ == '__main__':
    main()
