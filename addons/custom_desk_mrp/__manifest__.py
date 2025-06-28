{
    'name': 'Custom Desk MRP',
    'summary': 'Manage custom desk production orders with inventory and sales integration.',
    'depends': [
        'base',
        'mail',
        'product',
        'sale',
        'stock',
        'account',
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/desk_order_views.xml',
        'report/desk_order_report.xml',
        # 'data/demo_data.xml',  # if adding demo data
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
