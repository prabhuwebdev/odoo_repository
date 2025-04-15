{
    "name":"Demo File",
    "version":"1.0",
    "summary":"This is about the Demo File",
    "author":"Prabhu",
    "category":"custom",
    "depends":['base',"web","ehr_cdss"],
    "data":[
        "security/ir.model.access.csv",
        "views/Demo.xml",
        "views/disease_prediction.xml",
        'views/dashboard.xml',
        'views/new_record.xml',
        'views/patient_record.xml',
        'views/past_medications.xml',
        'views/patient_to_dashboard.xml'


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
            'Demo_form1/static/src/xml/new_record.xml',
            'Demo_form1/static/src/xml/past_medications.xml',
            'Demo_form1/static/src/js/past_medications.js',
            'Demo_form1/static/src/js/patient_to_dashboard.js',
            'Demo_form1/static/src/xml/patient_to_dashboard.xml',



        ],
    },
    "installable":True,
    "application":True,

}