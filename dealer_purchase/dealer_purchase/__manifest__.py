{
    "name": "Dealer Purchase",  # Module title
    "summary": "Dealer Purchase Modules",  # Module subtitle phrase
    "description": """
    Manage Retail
    ==============
    Efficiently manage the entire Dealer Purchase
    """,  
    "version": "18.0",
    "author": "Sakkthi.",
    "category": "Shopping",
    "website": "",
    "license": "AGPL-3",
    "depends": ["base","web"],
    "data": [
        'security/dealer_purchase_security.xml',
        'security/ir.model.access.csv',
        'views/dealer_purchase_views.xml',
        'views/dealer_purchase_line_views.xml',
        'views/dealer_pivot_view.xml',
        'report/dealer_purchase_report.xml',
   
    ],
    
    'assets': {
        'web.assets_backend': [
            'dealer_purchase/static/src/js/dealer_pivot_export.js',
            'web/static/src/views/pivot/pivot_view.js',
            'web/static/src/views/pivot/pivot_model.js',
            'web/static/src/views/pivot/pivot_renderer.js',
            'web/static/src/views/pivot/pivot_controller.js',

        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}