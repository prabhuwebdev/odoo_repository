from odoo import models, fields

class VaccineType(models.Model):
    _name = 'ehr_cdss.vaccine.type'
    _description = 'Vaccine Type'

    name = fields.Char(string='Vaccine Type', required=True)
