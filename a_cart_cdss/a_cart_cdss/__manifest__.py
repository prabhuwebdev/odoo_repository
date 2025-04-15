{
    "name": "CDSS",  # Module title
    "summary": "CARgenix CDSS",  # Module subtitle phrase
    "description": """
CAR T 
========================
Patient Selection
Treatement Planning
Intervention Timing
    """,  # Supports reStructuredText(RST) format (description is Deprecated)
    "version": "18.0",
    "author": "JVL Technologies Pvt. Ltd.",
    "category": "CARgenix",
    "website": "http://www.jvltechnologies.com",
    "license": "AGPL-3",
    "depends": ["base","web","mail"],
    "data": [            
        "security/ir.model.access.csv",
        "views/View_Patient_Profile.xml"
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
    "installable": True,
    "application": True,
}
