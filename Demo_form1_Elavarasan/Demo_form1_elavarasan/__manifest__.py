{
    "name":"Demo File Elavarasan",
    "version":"1.0",
    "summary":"This is about the Demo File",
    "author":"Prabhu",
    "category":"custom",
    "depends":['base',"web"],
    "data":[
        "security/ir.model.access.csv",
        "views/Demo.xml",
        "views/disease_prediction.xml",
        'views/dashboard.xml',
        'views/new_record.xml'


    ],
    'assets':{
        'web.assets_backend':[
           'Demo_form1/static/src/js/demo.js',
           'Demo_form1/static/src/scss/demo.scss',
           'Demo_form1/static/src/xml/demo.xml',
           'Demo_form1/static/src/js/disease_prediction.js',
           'Demo_form1/static/src/xml/disease_prediction.xml',
            'Demo_form1/static/src/xml/dashboard.xml',
            'Demo_form1/static/src/js/dashboard.js',
            'Demo_form1/static/src/js/new_record.js',
            'Demo_form1/static/src/xml/new_record.xml'
        ],
    },
    "installable":True,
    "application":True,

}