{
    "name":"Diagnosis AI",
    "version":"1.0",
    "summary":"This is about the Demo File",
    "author":"Prabhu",
    "category":"MED AI",
    "depends":['base',"web"],
    "data":[
        "security/ir.model.access.csv",
        "views/Demo.xml",
        "views/disease_prediction.xml",


    ],
    'assets':{
        'web.assets_backend':[
           'Demo_form1/static/src/js/demo.js',
           'Demo_form1/static/src/scss/demo.scss',
           'Demo_form1/static/src/xml/demo.xml',
           'Demo_form1/static/src/js/disease_prediction.js',
           'Demo_form1/static/src/xml/disease_prediction.xml'
        ],
    },
    "installable":True,
    "application":True,

}