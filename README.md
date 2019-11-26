# ETSY-api-tools

## Inspiration
I wrote these tools to help assist my significant other synchronize her Etsy shop to her WooCommerce site. As well as exporting inventory data from Etsy to get it into places like QuickBooks Online and, again, WooCommerce.  Why write another library for talking to Etsy. The ones that I have found either don't handle paginated results or OAuth is broken in them or they are unmaintained.  I could have forked from someone else's and added functionality and that may still happen.  For now I needed a quick implementation that would handle exports easily.

## Example
Look in the `main.py` an example on how to use this file.  You will have to edit the config.example.py file to make it your own and rename it to config.py.

There is a `oauth_etsy.py` file in the tools dir.  It will help with the initial 3-way handshake to generate the oauth tokens needed.
