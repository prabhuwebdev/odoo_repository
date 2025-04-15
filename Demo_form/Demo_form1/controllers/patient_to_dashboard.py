from odoo import http
from odoo.http import request

class PatientDashboardController(http.Controller):

    @http.route('/ehr_cdss/patient_dashboard', type='json', auth='public')
    def get_patients_with_info(self):
        # Fetch all records from ehr_cdss.patient.info
        patients = request.env['ehr_cdss.patient.info'].sudo().search([])

        if not patients:
            print("No data fetched")
        else:
            print("Fetched patient data:", patients)

        # Directly map the required fields from ehr_cdss.patient.info
        result = []
        for patient in patients:
            result.append({
                'id': patient.id,
                'name': patient.name,
                'birth_date': patient.birth_date,
                'age': patient.age,
                'gender': patient.gender,
                'phone_primary': patient.phone_primary
            })

        return result


@http.route('/ehr_cdss/get_patient', type='json', auth='public')
def get_patient(self, patient_id):
    patient = request.env['ehr_cdss.patient.info'].sudo().browse(patient_id)
    print(patient)
    if not patient:
        print("No Matching patient data is available")
    else:
        return {
            'id': patient.id,
            'name': patient.name,
            'birth_date': str(patient.birth_date),
            'age': patient.age,
            'gender': patient.gender,
            'phone_primary': patient.phone_primary,
            # 'smoking': patient.smoking,
            # 'alcohol': patient.alcohol,
            # 'exercise': patient.exercise,
        }



