from odoo import models, fields, api

# class NewRecordForm(models.Model):
#     _name= "new.record.form"
#     _description= "Insert data of the patient"

class PatientImageRecord(models.Model):
    _name = 'patient.image.record'
    _description = 'Patient Imaging Record'

    name = fields.Char(string='Image Title', required=True)
    image_type = fields.Selection([
        ('ct', 'CT Scan'),
        ('xray', 'X-Ray'),
        ('mri', 'MRI'),
        ('ultrasound', 'Ultrasound'),
    ], string='Image Type', required=True)
    body_region = fields.Char(string='Body Part/Region', required=True)
    study_date = fields.Date(string='Study Date', required=True)
    provider = fields.Char(string='Healthcare Provider/Facility')
    physician = fields.Char(string='Physician/Specialist')
    contrast_used = fields.Boolean(string='Contrast Used')
    run_ai = fields.Boolean(string='Run AI Analysis on Save')