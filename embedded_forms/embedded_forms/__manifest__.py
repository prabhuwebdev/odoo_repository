{
    'name': 'Employee Lazy Embedded Forms',
    'version': '18.0',
    'summary': 'Lazy-loaded embedded employee forms',
    'description': 'Embedded forms for employee info and address with lazy loading functionality',
    'category': 'Human Resources',
    'author': 'JVL Technologies Pvt. Ltd.',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'embedded_forms/static/src/js/employee_lazy_form.js',
            'embedded_forms/static/src/xml/employee_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}