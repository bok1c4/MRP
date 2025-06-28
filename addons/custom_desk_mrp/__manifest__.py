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
        'report/desk_order_report.xml',
        'views/desk_order_views.xml',
        'views/product_template_inherit.xml',
        'data/ir_sequence.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
