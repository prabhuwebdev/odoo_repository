from odoo import models, fields

class PatientRecord(models.Model):
    _name = 'patient.record'
    _description = 'Patient Record'

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    dob = fields.Date(string="Date of Birth")
    contact = fields.Char(string="Contact")
    smoking = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="Smoking")
    alcohol = fields.Selection([
        ('never', 'Never'),
        ('occasionally', 'Occasionally'),
        ('regularly', 'Regularly')
    ], string="Alcohol")
    exercise = fields.Selection([
        ('none', 'None'),
        ('occasionally', 'Occasionally'),
        ('regular', 'Regular')
    ], string="Exercise")



    def records(self):
        return {
            "Name":self.name,
            "Age":self.age,
            "Gender":self.gender,
            "DOB":self.dob,
            "Contact":self.contact,
            "Smoking":self.smoking,
            "Alcohol":self.alcohol,
            "Exercise":self.exercise,

        }

class PatientFields(models.Model):
    _name = "ehr_cdss.patients"
    _description = "description about fetching the another module data"


    patient_info=fields.One2many("ehr_cdss.patient.info","patient_ids",string="Patient Info")