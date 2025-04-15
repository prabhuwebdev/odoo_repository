# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class PatientProfile(models.Model):
    _name = 'patient.profile'
    _description = 'Patient Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Personal Information
    name = fields.Char(string='Full Name', required=True, tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True, tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', required=True, tracking=True)
    sex_assigned_at_birth = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Sex Assigned at Birth', required=True, tracking=True)
    medical_record_number = fields.Char(string='Medical Record Number', tracking=True)
    contact_information = fields.Char(string='Contact Information', tracking=True)

    # Demographic Information
    ethnicity_race = fields.Selection([
        ('caucasian', 'Caucasian'),
        ('african', 'African'),
        ('hispanic', 'Hispanic'),
        ('asian', 'Asian'),
        ('pacific_islander', 'Pacific Islander'),
        ('native_american', 'Native American'),
        ('other', 'Other')
    ], string='Ethnicity and Race', tracking=True)
    primary_language = fields.Char(string='Primary Language', tracking=True)
    need_interpreter = fields.Boolean(string='Need for Interpreter', tracking=True)
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
        ('partnered', 'Partnered')
    ], string='Marital Status', tracking=True)
    family_structure = fields.Text(string='Family Structure', tracking=True)
    education_level = fields.Selection([
        ('none', 'None'),
        ('elementary', 'Elementary'),
        ('secondary', 'Secondary'),
        ('higher', 'Higher Education'),
        ('vocational', 'Vocational'),
        ('postgraduate', 'Postgraduate')
    ], string='Education Level', tracking=True)
    geographic_location = fields.Char(string='Geographic Location', tracking=True)
    employment_status = fields.Selection([
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('self_employed', 'Self-employed'),
        ('retired', 'Retired'),
        ('student', 'Student')
    ], string='Employment Status', tracking=True)
    occupation = fields.Char(string='Occupation', tracking=True)

    # Cultural/Religious Information
    cultural_preferences = fields.Text(string='Cultural Preferences', tracking=True)
    religious_preferences = fields.Text(string='Religious Preferences', tracking=True)
    aboriginal_status = fields.Boolean(string='Aboriginal and Torres Strait Islander Status', tracking=True)
    dietary_restrictions = fields.Text(string='Dietary Restrictions', tracking=True)
    cultural_customs = fields.Text(string='Cultural Customs/Taboos', tracking=True)
    written_language_pref = fields.Char(string='Language Preferences for Written Materials', tracking=True)
    verbal_language_pref = fields.Char(string='Language Preferences for Verbal Communication', tracking=True)

    # Insurance/Financial Status
    insurance_coverage = fields.Selection([
        ('private', 'Private'),
        ('medicare', 'Medicare'),
        ('medicaid', 'Medicaid'),
        ('self_pay', 'Self Pay'),
        ('other', 'Other')
    ], string='Insurance Coverage', tracking=True)
    insurance_provider = fields.Char(string='Insurance Provider', tracking=True)
    policy_number = fields.Char(string='Policy Number', tracking=True)

    # Primary Insurance Information
    primary_insurance_coverage = fields.Selection([
        ('private', 'Private'),
        ('medicare', 'Medicare'),
        ('medicaid', 'Medicaid'),
        ('self_pay', 'Self Pay'),
        ('other', 'Other')
    ], string='Primary Insurance Coverage', tracking=True)
    primary_insurance_provider = fields.Char(string='Primary Insurance Provider', tracking=True)
    primary_policy_number = fields.Char(string='Primary Policy Number', tracking=True)

    # Secondary Insurance Information
    secondary_insurance_coverage = fields.Selection([
        ('private', 'Private'),
        ('medicare', 'Medicare'),
        ('medicaid', 'Medicaid'),
        ('self_pay', 'Self Pay'),
        ('none', 'None'),
        ('other', 'Other')
    ], string='Secondary Insurance Coverage', tracking=True)
    secondary_insurance_provider = fields.Char(string='Secondary Insurance Provider', tracking=True)
    secondary_policy_number = fields.Char(string='Secondary Policy Number', tracking=True)

    financial_status = fields.Selection([
        ('secure', 'Secure'),
        ('stable', 'Stable'),
        ('unstable', 'Unstable'),
        ('critical', 'Critical')
    ], string='Financial Status Assessment', tracking=True)
    financial_assistance = fields.Boolean(string='Financial Assistance Needed', tracking=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        """Compute age based on date of birth"""
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                delta = today - record.date_of_birth
                record.age = delta.days // 365
            else:
                record.age = 0