{
    'name': 'Open Ai Diagnosis',
    'version': '1.0',
    'summary': 'AI-powered medical diagnosis',
    'description': """
        This module provides AI-powered medical diagnosis functionality 
        based on patient symptoms and medical history.
    """,
    'category': 'Healthcare',
    'author': 'Your Company',
    'website': 'https://www.example.com',
    'depends': ['base',],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/diagnosis_views.xml',
        'views/diagnosis_substance.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}