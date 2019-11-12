import datetime

fields = [
        {
            'field_name': 'Product/Service Name',
            'etsy_field': 'title',
            'default':  '',
            'valid': ()
        },
        {
            'field_name': 'Sales Description',
            'etsy_field': 'title',
            'default':  '',
            'valid': ()
        },
        {
            'field_name': 'SKU',
            'etsy_field': 'sku',
            'default':  '',
            'valid': ()
        },
        {
            'field_name': 'Type',
            'etsy_field': '',
            'default': 'Inventory',
            'valid': ('Inventory', 'Noninventory', 'Service')
            'valid': ()
        },
        {
            'field_name': 'Sales Price / Rate',
            'etsy_field': 'price',
            'default': '',
            'valid': ()
        },
        {
            'field_name': 'Income Account',
            'etsy_field': None,
            'default': '',
            'valid': ()
        },
        {
            'field_name': 'Purchase Description',
            'etsy_field': 'title',
            'default': '',
            'valid': ()
        },
        {
            'field_name': 'Purchase Cost',
            'etsy_field': None,
            'default': '0.00',
            'valid': ()
        },
        {
            'field_name': 'Expense Account',
            'etsy_field': None,
            'default': '',
            'valid': ()
        },
        {
            'field_name': 'Quantity on Hand',
            'etsy_field': 'quantity',
            'default': 0,
            'valid': ()
        },
        {
            'field_name': 'Reorder Point',
            'etsy_field': None,
            'default': 0,
            'valid': ()
        },
        {
            'field_name': 'Inventory Asset Account',
            'etsy_field': None,
            'default': '',
            'valid': ()
        },
        {
            'field_name': 'Quantity as-of Date',
            'etsy_field': None,
            'default': datetime.datetime.now(),
            'valid': ()
        }
]
