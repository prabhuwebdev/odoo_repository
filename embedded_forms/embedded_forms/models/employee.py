from odoo import models, fields, api

class EmployeeInfo(models.Model):
    _name = 'employee.info'
    _description = 'Employee Information'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    
    def get_info_data(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

class EmployeeAddress(models.Model):
    _name = 'employee.address'
    _description = 'Employee Address'

    employee_id = fields.Many2one('employee.info', string='Employee', required=True, ondelete='cascade')
    city = fields.Char(string='City', required=True)
    pin = fields.Char(string='PIN', required=True)

    def get_address_data(self, employee_id):
        address = self.search([('employee_id', '=', employee_id)], limit=1)
        if address:
            return {
                'city': address.city,
                'pin': address.pin,
            }
        return {'city': '', 'pin': ''}


from odoo import models, fields


class MedicalHistory(models.Model):
    _name = 'medical.history'
    _description = 'Medical History'

    primary_cancer_diagnosis = fields.Text(string="Primary Cancer Diagnosis", help="Type, Location, Date of Diagnosis")
    histological_molecular_subtype = fields.Text(string="Histological Molecular Subtype",help="Histological and Molecular Subtype")
    stage_at_diagnosis = fields.Text(string="Stage at Diagnosis", help="TNM Classification")
    previous_cancer_diagnosis = fields.Boolean(string="Previous Cancer Diagnosis",help="Previous Cancer Diagnosis or Recurrence")
    previous_cancer_details = fields.Text(string="Previous Cancer Details",help="Details of Previous Cancer if applicable")

    treatment_history = fields.Selection([
        ('surgery', 'Surgery'),
        ('chemotherapy', 'Chemotherapy'),
        ('radiotherapy', 'Radiotherapy'),
        ('immunotherapy', 'Immunotherapy'),
        ('targeted_therapy', 'Targeted Therapy'),
    ], string="Treatment History")

    treatment_details = fields.Text(string="Treatment Details", help="Details of treatments received")

    response_to_treatment = fields.Selection([
        ('partial', 'Partial'),
        ('complete', 'Complete'),
        ('stable', 'Stable'),
        ('progressive_disease', 'Progressive Disease'),
    ], string="Response to Treatment")

    date_of_last_followup = fields.Date(string="Date of Last Follow-Up")

    comorbidities = fields.Many2many(
        'medical.comorbidity',
        relation='medical_history_comorbidities_rel',
        column1='medical_history_id',
        column2='comorbidity_id',
        string="Comorbidities"
    )

    comorbidities_details = fields.Text(string="Comorbidities Details")
    surgical_history = fields.Text(string="Surgical History")
    biopsy_history = fields.Text(string="Biopsy History")
    procedure_history = fields.Text(string="Procedure History")

    current_medications = fields.Many2many(
        'medical.medication',
        relation='medical_history_current_medications_rel',
        column1='medical_history_id',
        column2='medication_id',
        string="Current Medications"
    )

    past_medications = fields.Many2many(
        'medical.medication',
        relation='medical_history_past_medications_rel',
        column1='medical_history_id',
        column2='medication_id',
        string="Past Medications"
    )

    chemotherapy_drugs = fields.Many2many(
        'medical.medication',
        relation='medical_history_chemotherapy_drugs_rel',
        column1='medical_history_id',
        column2='medication_id',
        string="Chemotherapy Drugs"
    )

    supportive_medications = fields.Many2many(
        'medical.medication',
        relation='medical_history_supportive_medications_rel',
        column1='medical_history_id',
        column2='medication_id',
        string="Supportive Medications"
    )

    otc_medications = fields.Many2many(
        'medical.medication',
        relation='medical_history_otc_medications_rel',
        column1='medical_history_id',
        column2='medication_id',
        string="OTC Medications"
    )

    drug_allergies = fields.Many2many(
        'medical.allergy',
        relation='medical_history_drug_allergies_rel',
        column1='medical_history_id',
        column2='allergy_id',
        string="Drug Allergies"
    )

    allergy_reactions = fields.Text(string="Allergy Reactions")
    food_environmental_allergies = fields.Text(string="Food & Environmental Allergies")
    anaphylaxis_history = fields.Boolean(string="Anaphylaxis History")

    hospitalization_history = fields.Text(string="Hospitalization History")
    major_illnesses = fields.Text(string="Major Illnesses")

    infectious_isolation_status = fields.Selection([
        ('infected', 'Infected'),
        ('isolated', 'Isolated'),
        ('none', 'None'),
    ], string="Infectious Isolation Status")

    implants_lda = fields.Text(string="Implants/LDA")

    immunization_status = fields.Selection([
        ('complete', 'Complete'),
        ('incomplete', 'Incomplete'),
        ('unknown', 'Unknown'),
    ], string="Immunization Status")

    immunizations = fields.Many2many(
        'medical.immunization',
        relation='medical_history_immunizations_rel',
        column1='medical_history_id',
        column2='immunization_id',
        string="Immunizations"
    )

    recent_overseas_travel = fields.Text(string="Recent Overseas Travel")
    maternal_history = fields.Text(string="Maternal History")
    antenatal_history = fields.Text(string="Antenatal History")

    delivery_type = fields.Selection([
        ('vaginal', 'Vaginal'),
        ('c_section', 'C-Section'),
    ], string="Delivery Type")

    delivery_complications = fields.Text(string="Delivery Complications")
    apgar_score = fields.Integer(string="Apgar Score")
    resuscitation_at_delivery = fields.Boolean(string="Resuscitation at Delivery")

    hep_b_status = fields.Selection([
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('unknown', 'Unknown'),
    ], string="Hepatitis B Status")

    vitamin_k_status = fields.Selection([
        ('given', 'Given'),
        ('not_given', 'Not Given'),
    ], string="Vitamin K Status")

    newborn_screening_status = fields.Selection([
        ('completed', 'Completed'),
        ('incomplete', 'Incomplete'),
        ('unknown', 'Unknown'),
    ], string="Newborn Screening Status")

