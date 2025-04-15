{
    "name":"School Management",
    "version":"1.0",
    "summary":"This is about the School Management Project",
    "author":"Jvl Techonologies",
    "category":"School Management",
    "depends":['base',"web"],
    "data":[
        "security/ir.model.access.csv",
        "views/fee_assignment.xml",
        'views/fee_category.xml',
        'views/fee_invoice.xml',
        'views/fee_structure.xml',
        'views/fee_remainder.xml'

    ],
    'assets':{

    },
    "installable":True,
    "application":True,

}