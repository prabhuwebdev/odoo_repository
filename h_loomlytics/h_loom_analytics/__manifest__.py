{
    "name": "Analytics",  # Module title
    "summary": "Loomlyticas Data Analytics App",  # Module subtitle phrase
    "description": """
Manage Retail
==============
Efficiently manage the entire retail stores
    """,  # Supports reStructuredText(RST) format (description is Deprecated)
    "version": "18.0",
    "author": "JVL Technologies Pvt. Ltd.",
    "category": "Loomlyticas",
    "website": "http://www.jvltechnologies.com",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/loomlytics_analytics.xml",
        "views/sale_pivot_report.xml",
        "views/daily_sales.xml",
        "views/daily_stock.xml",
        "views/monthly_stock.xml",
        "views/daily_sale_stock_report.xml"
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
    "installable": True,
    "application": True,
}
