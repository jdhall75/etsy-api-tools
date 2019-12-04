import time
import csv


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

