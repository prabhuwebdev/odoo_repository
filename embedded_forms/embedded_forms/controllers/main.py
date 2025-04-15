from odoo import http
from odoo.http import request
import json

class EmployeeLazyController(http.Controller):
    
    @http.route('/employee_lazy/get_info', type='json', auth='user')
    def get_info(self, employee_id=False, **kwargs):
        if not employee_id:
            return {'first_name': '', 'last_name': ''}
            
        employee = request.env['employee.info'].browse(int(employee_id))
        if not employee.exists():
            return {'first_name': '', 'last_name': ''}
            
        return employee.get_info_data()
    
    @http.route('/employee_lazy/get_address', type='json', auth='user')
    def get_address(self, employee_id=False, **kwargs):
        if not employee_id:
            return {'city': '', 'pin': ''}
            
        address_model = request.env['employee.address']
        return address_model.get_address_data(int(employee_id))
    
    @http.route('/employee_lazy/save_data', type='json', auth='user')
    def save_data(self, employee_id=False, form_type='info', data=None, **kwargs):
        if data is None:
            data = {}
            
        result = {
            'success': False,
            'employee_id': employee_id,
        }
            
        if form_type == 'info':
            if employee_id:
                employee = request.env['employee.info'].browse(int(employee_id))
                if employee.exists():
                    employee.write({
                        'first_name': data.get('first_name', ''),
                        'last_name': data.get('last_name', ''),
                    })
                    result['success'] = True
            else:
                new_employee = request.env['employee.info'].create({
                    'first_name': data.get('first_name', ''),
                    'last_name': data.get('last_name', ''),
                })
                result['employee_id'] = new_employee.id
                result['success'] = True
                
        elif form_type == 'address' and employee_id:
            employee = request.env['employee.info'].browse(int(employee_id))
            if not employee.exists():
                return result
                
            address = request.env['employee.address'].search([
                ('employee_id', '=', int(employee_id))
            ], limit=1)
            
            if address:
                address.write({
                    'city': data.get('city', ''),
                    'pin': data.get('pin', ''),
                })
            else:
                request.env['employee.address'].create({
                    'employee_id': int(employee_id),
                    'city': data.get('city', ''),
                    'pin': data.get('pin', ''),
                })
                
            result['success'] = True
            
        return result


# from odoo import http
# from odoo.http import request

class MedicalHistoryController(http.Controller):

    @http.route('/medical_history/get_all', type='json', auth='user', methods=['GET'])
    def get_all_medical_histories(self):
        """ Fetch all medical history records with all fields """
        records = request.env['medical.history'].sudo().search([])
        return [
            {
                'id': rec.id,
                'primary_cancer_diagnosis': rec.primary_cancer_diagnosis,
                'histological_molecular_subtype': rec.histological_molecular_subtype,
                'stage_at_diagnosis': rec.stage_at_diagnosis,
                'previous_cancer_diagnosis': rec.previous_cancer_diagnosis,
                'previous_cancer_details': rec.previous_cancer_details,
                'treatment_history': rec.treatment_history,
                'treatment_details': rec.treatment_details,
                'response_to_treatment': rec.response_to_treatment,
                'date_of_last_followup': rec.date_of_last_followup,
                'comorbidities': rec.comorbidities.mapped('name'),
                'comorbidities_details': rec.comorbidities_details,
                'surgical_history': rec.surgical_history,
                'biopsy_history': rec.biopsy_history,
                'procedure_history': rec.procedure_history,
                'current_medications': rec.current_medications.mapped('name'),
                'past_medications': rec.past_medications.mapped('name'),
                'chemotherapy_drugs': rec.chemotherapy_drugs.mapped('name'),
                'supportive_medications': rec.supportive_medications.mapped('name'),
                'otc_medications': rec.otc_medications.mapped('name'),
                'drug_allergies': rec.drug_allergies.mapped('name'),
                'allergy_reactions': rec.allergy_reactions,
                'food_environmental_allergies': rec.food_environmental_allergies,
                'anaphylaxis_history': rec.anaphylaxis_history,
                'hospitalization_history': rec.hospitalization_history,
                'major_illnesses': rec.major_illnesses,
                'infectious_isolation_status': rec.infectious_isolation_status,
                'implants_lda': rec.implants_lda,
                'immunization_status': rec.immunization_status,
                'immunizations': rec.immunizations.mapped('name'),
                'recent_overseas_travel': rec.recent_overseas_travel,
                'maternal_history': rec.maternal_history,
                'antenatal_history': rec.antenatal_history,
                'delivery_type': rec.delivery_type,
                'delivery_complications': rec.delivery_complications,
                'apgar_score': rec.apgar_score,
                'resuscitation_at_delivery': rec.resuscitation_at_delivery,
                'hep_b_status': rec.hep_b_status,
                'vitamin_k_status': rec.vitamin_k_status,
                'newborn_screening_status': rec.newborn_screening_status,
            }
            for rec in records
        ]

    @http.route('/medical_history/get_selection_fields', type='json', auth='user', methods=['GET'])
    def get_selection_fields(self):
        """ Retrieve all selection field values dynamically """
        MedicalHistory = request.env['medical.history']

        selection_fields= {
            'treatment_history': MedicalHistory._fields.get('treatment_history', {}).selection,
            'response_to_treatment': MedicalHistory._fields.get('response_to_treatment', {}).selection,
            'infectious_isolation_status': MedicalHistory._fields.get('infectious_isolation_status', {}).selection,
            'immunization_status': MedicalHistory._fields.get('immunization_status', {}).selection,
            'delivery_type': MedicalHistory._fields.get('delivery_type', {}).selection,
            'hep_b_status': MedicalHistory._fields.get('hep_b_status', {}).selection,
            'vitamin_k_status': MedicalHistory._fields.get('vitamin_k_status', {}).selection,
            'newborn_screening_status': MedicalHistory._fields.get('newborn_screening_status', {}).selection,
        }
        print(selection_fields)
        return selection_fields

class MedicalController(http.Controller):
    @http.route('/medical/comorbidities', type='json', auth='user')
    def get_comorbidities(self):
        """Fetch all comorbidities"""
        comorbidities = request.env['medical.comorbidity'].sudo().search([])
        return [{'id': comorb.id, 'name': comorb.name} for comorb in comorbidities]

    @http.route("/medical/meditation",type="json",auth='user')
    def get_current_meditation(self):
        current_meditation=request.env["medical.meditation"].sudo().search([])
        return [{"id":med.id,"name":med.name}for med in current_meditation]

    @http.route("/medicat/past_medication",type="json",auth="public")
    def past_medication(self):
        past_medication = request.env["medical.meditation"].sudo().search([])
        return [{"id": past.id, "name": past.name} for past in past_medication]

    @http.route("/medicat/chemotherapy_drugs", type="json", auth="public")
    def past_medication(self):
        chemotherapy = request.env["res.partner"].sudo().search([],limit=6)
        return [{"id": chemo.id, "name": chemo.name} for chemo in chemotherapy]

    @http.route("/medicat/supportive_medications", type="json", auth="public")
    def supportive_medications(self):
        supportive_med = request.env["medical.medications"].sudo().search([], limit=6)
        return [{"id": supp.id, "name": supp.name} for supp in supportive_med]


    @http.route("/medicat/otc_medications",type="json",auth="public")
    def otc_medications(self):
        otc=request.env['medical.medications'].sudo().search([],limit=10)
        return [{"id":otc_med.id,"name":otc_med.name} for otc_med in otc]

    @http.route("/medicat/drug_allergies", type="json", auth="public")
    def drug_allergies(self):
        drug_allergie= request.env['medical.medications'].sudo().search([], limit=10)
        return [{"id": drug.id, "name": drug.name} for drug in drug_allergie]

    @http.route("/medicat/immunization",type="json",auth="public")
    def immunization(self):
        immune=request.env['medical.medications'].sudo().search([],limit=10)
        return [{"id":imu.id,"name":imu.name} for imu in immune]

