{
    "name": "EHR",  # Module title
    "summary": "EHR Modules",  # Module subtitle phrase
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
    "depends": ["base","mail","web"],
    "data": [
        # "security/hub_security.xml",
        "security/ir.model.access.csv",
        # "views/patient_view.xml",
        "views/patient_form_two_view.xml",
        "views/provider_view.xml",
        "views/organization_view.xml",
        "views/insurance_view.xml",
        "views/medical_record_view.xml",
        "views/assessment_view.xml",
        "views/appointment_view.xml",
        "views/appointment_slot_view.xml",
        "views/location_view.xml",
        "views/billing_code_view.xml",
        "views/progress_note_view.xml",
        "views/treatment_view.xml",
        "views/safety_plan_view.xml",
        "views/address_view.xml",
        "views/contact_view.xml",
        "views/contact_info_view.xml",
        "views/medical_history_views.xml",
        "views/patient-allergy-views.xml",
        "views/document_view.xml",
        # "views/document_owl.xml",
        "views/medication_view.xml",
        "views/immunization.xml",
        "views/family_history_views.xml",
        "views/odoo_progress_view.xml",
        # "views/ehr_cdss_kanban_templates.xml",
        "reports/odoo_progress_note_report.xml",
        
        
        
        # "views/assets.xml",
        
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
    'assets': {
        'web.assets_frontend': [
            # 'ehr_cdss/static/src/js/open_in_new_tab.1js',
        ],
        "web.assets_backend": [
            # "ehr_cdss/static/src/js/document.js",
            # "ehr_cdss/static/src/xml/document_template.xml",
            # 'ehr_cdss/static/src/js/open_in_new_tab.js',
            # 'ehr_cdss/static/src/js/kanban_buttons.js',
            
            'ehr_cdss/static/src/css/style.css',
        ],
    },
    "installable": True,
    "application": True,
}

