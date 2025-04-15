{
    "name":"Student Information",
    'version': '1.0',
    'summary': 'This is about student info',
    'author': 'Prabhu',
    'category': 'Custom',
    'depends': ['base'],  # Add dependencies if needed
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],  # Add XML/CSV files here if needed
    "assets":{
        'web.assets_backend':[
            'student_module/static/src/js/custom_widget.js',
            'student_module/static/src/scss/custom_widget.scss',
            'student_module/static/src/xml/custom_widget.xml'
        ]
    },
    'installable': True,
    'application': True,
}