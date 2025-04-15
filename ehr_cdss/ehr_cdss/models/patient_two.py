from odoo import models, fields, api
from odoo.exceptions import UserError

import random
import string

class PatientInfo(models.Model):
    _name = 'ehr_cdss.patient.info'
    _description = 'Patient Information'

    # Basic Information
    patient_id = fields.Char("Patient ID", readonly=True, default=lambda self: self._generate_patient_id())
    allergy_ids = fields.One2many('ehr_cdss.medical.patient.allergy', 'patient_id', string='Allergies')
    allergy_count = fields.Integer(compute='_compute_allergy_count', string='Allergy Count')
    has_critical_allergies = fields.Boolean(compute='_compute_has_critical_allergies', string='Has Critical Allergies', store=True)
    allergy_band_ids = fields.One2many('ehr_cdss.medical.patient.allergy.band', 'patient_id', string='Allergy Bands')
    current_allergy_band = fields.Many2one('ehr_cdss.medical.patient.allergy.band', compute='_compute_current_allergy_band', string='Current Allergy Band')

    name = fields.Char(string='Full Name',)
    primary_provider_id = fields.Many2one('ehr_cdss.provider', string="Primary Provider")
    preferred_name = fields.Char(string='Preferred Name')
    birth_date = fields.Date(string='Date of Birth', )
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    mrn = fields.Char(string="Medical Record Number", tracking=True)
    is_minor = fields.Boolean(string="Is a Minor")
    image = fields.Binary(string="Patient Image")
    gender = fields.Selection([
        ('prefer_not_to_say', 'Prefer Not to Say'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_binary', 'Non-Binary'),
        ('transgender_male', 'Transgender Male'),
        ('transgender_female', 'Transgender Female'),
        ('other', 'Other'),
    ], string='Gender', default='prefer_not_to_say')
    sex_assigned_at_birth = fields.Selection([
        ('prefer_not_to_say', 'Prefer Not to Say'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('intersex', 'Intersex'),
    ], string='Sex Assigned at Birth', default='prefer_not_to_say')

    # Contact Information
    address_street = fields.Char(string='Street Address')
    address_city = fields.Char(string='City')
    address_state = fields.Char(string='State/Province')
    address_postal_code = fields.Char(string='Postal/ZIP Code')
    address_country = fields.Char(string='Country')
    phone_primary = fields.Char(string='Primary Phone Number')
    phone_secondary = fields.Char(string='Secondary Phone Number')
    email = fields.Char(string='Email Address')
    preferred_contact_method = fields.Selection([
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('mail', 'Mail'),
        ('patient_portal', 'Patient Portal')
    ], string='Preferred Contact Method')
    
    # Demographic Information
    ethnicity = fields.Selection([
        ('hispanic_latino', 'Hispanic/Latino'),
        ('not_hispanic_latino', 'Not Hispanic/Latino'),
        ('unknown', 'Unknown'),
        ('prefer_not_to_say', 'Prefer Not to Say')
    ], string='Ethnicity')
    race = fields.Selection([
        ('white', 'White'),
        ('black_african_american', 'Black/African American'),
        ('asian', 'Asian'),
        ('american_indian_alaska_native', 'American Indian/Alaska Native'),
        ('native_hawaiian_pacific_islander', 'Native Hawaiian/Pacific Islander'),
        ('modelracial', 'modelracial'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer Not to Say')
    ], string='Race')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('domestic_partnership', 'Domestic Partnership'),
        ('divorced', 'Divorced'),
        ('separated', 'Separated'),
        ('widowed', 'Widowed'),
        ('other', 'Other')
    ], string='Marital Status')
    preferred_language = fields.Char(string='Preferred Language')
    interpreter_needed = fields.Boolean(string='Interpreter Needed')
    interpreter_language = fields.Char(string='Interpreter Language')
    english_proficiency = fields.Selection([
        ('fluent', 'Fluent'),
        ('good', 'Good'),
        ('limited', 'Limited'),
        ('none', 'None')
    ], string='English Proficiency')
    
    # Socioeconomic Information
    education_level = fields.Selection([
        ('less_than_high_school', 'Less than High School'),
        ('high_school_ged', 'High School/GED'),
        ('some_college', 'Some College'),
        ('associates_degree', 'Associate\'s Degree'),
        ('bachelors_degree', 'Bachelor\'s Degree'),
        ('graduate_degree', 'Graduate Degree'),
        ('professional_degree', 'Professional Degree'),
        ('doctorate', 'Doctorate'),
        ('other', 'Other')
    ], string='Education Level')
    employment_status = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('self_employed', 'Self Employed'),
        ('unemployed', 'Unemployed'),
        ('retired', 'Retired'),
        ('student', 'Student'),
        ('disabled', 'Disabled'),
        ('other', 'Other')
    ], string='Employment Status')
    occupation = fields.Char(string='Occupation')
    employer = fields.Char(string='Employer')
    industry = fields.Char(string='Industry')
    income_range = fields.Selection([
        ('under_15000', 'Under $15,000'),
        ('15000_to_25000', '$15,000 to $25,000'),
        ('25000_to_50000', '$25,000 to $50,000'),
        ('50000_to_75000', '$50,000 to $75,000'),
        ('75000_to_100000', '$75,000 to $100,000'),
        ('over_100000', 'Over $100,000'),
        ('prefer_not_to_say', 'Prefer Not to Say')
    ], string='Income Range')
    household_size = fields.Integer(string='Household Size')
    veteran_status = fields.Boolean(string='Veteran Status')
    
    # Geographic Information
    geographic_location = fields.Selection([
        ('urban', 'Urban'),
        ('suburban', 'Suburban'),
        ('rural', 'Rural')
    ], string='Geographic Location')
    travel_time_to_facility = fields.Float(string='Travel Time to Facility')
    transportation = fields.Selection([
        ('own_vehicle', 'Own Vehicle'),
        ('public_transportation', 'Public Transportation'),
        ('walk', 'Walk'),
        ('bicycle', 'Bicycle'),
        ('taxi_rideshare', 'Taxi/Rideshare'),
        ('other', 'Other')
    ], string='Primary Mode of Transportation')
    housing_status = fields.Selection([
        ('own', 'Own'),
        ('rent', 'Rent'),
        ('live_with_family', 'Live with Family'),
        ('temporary_housing', 'Temporary Housing'),
        ('homeless', 'Homeless'),
        ('other', 'Other')
    ], string='Housing Status')
    
    # Cultural and Religious Information
    religion = fields.Selection([
        ('none', 'None'),
        ('christianity', 'Christianity'),
        ('islam', 'Islam'),
        ('judaism', 'Judaism'),
        ('hinduism', 'Hinduism'),
        ('buddhism', 'Buddhism'),
        ('sikhism', 'Sikhism'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer Not to Say')
    ], string='Religious Preference')
    religious_practices = fields.Text(string='Important Religious Practices')
    cultural_preferences = fields.Text(string='Cultural Preferences')
    dietary_restrictions = fields.Text(string='Dietary Restrictions')
    is_aboriginal_torres_strait = fields.Boolean(string='Aboriginal or Torres Strait Islander')
    
    # Family Information
    family_structure = fields.Text(string='Family Structure')
    children = fields.Integer(string='Number of Children')
    dependents = fields.Integer(string='Number of Dependents')
    caregiver_name = fields.Char(string='Primary Caregiver Name')
    caregiver_relationship = fields.Selection([
        ('spouse', 'Spouse'),
        ('parent', 'Parent'),
        ('child', 'Child'),
        ('sibling', 'Sibling'),
        ('friend', 'Friend'),
        ('other', 'Other')
    ], string='Caregiver Relationship')
    caregiver_phone = fields.Char(string='Caregiver Phone')
    emergency_contact_name = fields.Char(string='Emergency Contact Name', )
    emergency_contact_relationship = fields.Selection([
        ('spouse', 'Spouse'),
        ('parent', 'Parent'),
        ('child', 'Child'),
        ('sibling', 'Sibling'),
        ('friend', 'Friend'),
        ('other', 'Other')
    ], string='Emergency Contact Relationship', )
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone', )
    emergency_contact_address = fields.Char(string='Emergency Contact Address')
    
    # Insurance and Financial Information
    insurance_ids = fields.One2many('ehr_cdss.patient.insurance', 'patient_id', string='Insurance Records')

    # insurance_status = fields.Selection([
    #     ('private', 'Private'),
    #     ('medicare', 'Medicare'),
    #     ('medicaid', 'Medicaid'),
    #     ('veterans', 'Veterans'),
    #     ('none', 'None'),
    #     ('other', 'Other')
    # ], string='Insurance Status', )
    # primary_insurance = fields.Char(string='Primary Insurance Name')
    # primary_insurance_id = fields.Char(string='Primary Insurance ID')
    # primary_insurance_group = fields.Char(string='Primary Insurance Group')
    # primary_insurance_holder = fields.Selection([
    #     ('self', 'Self'),
    #     ('spouse', 'Spouse'),
    #     ('parent', 'Parent'),
    #     ('other', 'Other')
    # ], string='Primary Insurance Holder')
    # primary_insurance_holder_name = fields.Char(string='Primary Insurance Holder Name')
    # primary_insurance_holder_dob = fields.Date(string='Primary Insurance Holder DOB')
    # secondary_insurance = fields.Char(string='Secondary Insurance Name')
    # secondary_insurance_id = fields.Char(string='Secondary Insurance ID')
    # secondary_insurance_group = fields.Char(string='Secondary Insurance Group')
    # financial_assistance = fields.Boolean(string='Financial Assistance Program')
    # financial_counseling = fields.Boolean(string='Financial Counseling Offered')
    # pharmacy_preference = fields.Char(string='Preferred Pharmacy')
    # pharmacy_address = fields.Char(string='Pharmacy Address')
    # pharmacy_phone = fields.Char(string='Pharmacy Phone')
    
    # Administrative Information
    registration_date = fields.Date(string='Initial Registration Date')
    last_updated = fields.Datetime(string='Information Last Updated')
    admission_source = fields.Selection([
        ('self_referral', 'Self Referral'),
        ('physician_referral', 'Physician Referral'),
        ('transfer', 'Transfer'),
        ('emergency', 'Emergency'),
        ('other', 'Other')
    ], string='Admission Source')
    pcp_name = fields.Char(string='Primary Care Provider')
    pcp_phone = fields.Char(string='PCP Phone')
    pcp_address = fields.Char(string='PCP Address')
    referring_provider = fields.Char(string='Referring Provider')
    preferred_facility = fields.Char(string='Preferred Facility')
    advance_directive = fields.Boolean(string='Advance Directive on File')
    healthcare_proxy = fields.Char(string='Healthcare Proxy')
    organ_donor_status = fields.Boolean(string='Organ Donor Status')
    hipaa_acknowledgment = fields.Boolean(string='HIPAA Acknowledgment Signed')
    consent_to_treat = fields.Boolean(string='Consent to Treat Signed')
    patient_portal_access = fields.Boolean(string='Patient Portal Access')
    recent_overseas_travel = fields.Boolean(string='Recent Overseas Travel')
    overseas_location = fields.Char(string='Overseas Travel Location')
    overseas_return_date = fields.Date(string='Date Returned from Overseas')
    show_back_button = fields.Boolean(string="Show Back Button")


    # inreverse id
    patient_ids=fields.Many2one("ehr_cdss.patients",string="patient id")



    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                birth_date = fields.Date.from_string(record.birth_date)
                record.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                record.age = 0

    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'PT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def action_demographic(self):
        record_id = self.id  # Get the ID of the current record (person)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.info',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': record_id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in a new window
            'flags': {'form': {'action': 'open_in_new_tab','default_patient_id': self.id,}},  # Custom flag to trigger JS
        }


    def action_medical_history(self):
        # Assuming 'self' is a record for a person or patient.
        record_id = self.id  # Get the ID of the current record (person)
        medical_history = self.env['ehr_cdss.medical.history'].search([('patient_id', '=', record_id)], limit=1)
        
        if not medical_history:
            # Handle case where no medical history exists for the patient
            medical_history = self.env['ehr_cdss.medical.history'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        return { 
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.history',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': medical_history.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True,'default_patient_id': self.id,
},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        
    
    def action_family_history(self):
        record_id = self.id  # Get the ID of the current record (person)
        
        family_history = self.env['ehr_cdss.medical.family.history'].search([('patient_id', '=', record_id)], limit=1)
        
        if not family_history:
            # Handle case where no medical history exists for the patient
            family_history = self.env['ehr_cdss.medical.family.history'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.family.history',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': family_history.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trig
        }
    
    def action_immunization_infectious_disease(self):
        record_id = self.id  # Get the ID of the current record (person)
        
        immunization_id = self.env['ehr_cdss.patient.immunization.record'].search([('partner_id', '=', record_id)], limit=1)
        
        if not immunization_id:
            # Handle case where no medical history exists for the patient
            immunization_id = self.env['ehr_cdss.patient.immunization.record'].create({
                'partner_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.immunization.record',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': immunization_id.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }

    
    def action_medical_patient_allergy(self):
        record_id = self.id  # Get the ID of the current record (person)
        patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].search([('patient_id', '=', record_id)], limit=1)
        
        if not patient_allergy:
            # Handle case where no medical history exists for the patient
            patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.patient.allergy',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': patient_allergy.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        

    def action_medication(self):
        record_id = self.id  # Get the ID of the current record (person)
        medication = self.env['ehr_cdss.medical.medication'].search([('patient_id', '=', record_id)], limit=1)
        
        if not medication:
            # Handle case where no medical history exists for the patient
            medication = self.env['ehr_cdss.medical.medication'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.medication',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': medication.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        

    def action_document(self):
        record_id = self.id  # Get the ID of the current record (person)
        document = self.env['ehr_cdss.document'].search([('patient_id', '=', record_id)], limit=1)
        
        if not document:
            # Handle case where no medical history exists for the patient
            document = self.env['ehr_cdss.document'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.document',  # Replace with actual model
            'view_mode': 'kanban,form',
            'view_type': 'form',
            'res_id': document.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'domain': [('patient_id', '=', record_id)],  # Filter documents by patient
            'context': {'search_default_filter_by_patient': 1, 'default_patient_id': record_id},
        }
        
        # action_appointment
        
    def action_appointment(self):
        record_id = self.id  # Get the ID of the current record (person)
        appointment = self.env['ehr_cdss.appointment'].search([('patient_id', '=', record_id)], limit=1)
        
        if not appointment:
            # Handle case where no medical history exists for the patient
            appointment = self.env['ehr_cdss.appointment'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.appointment',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': appointment.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        
        
    def action_insurance(self):
        record_id = self.id  # Get the ID of the current record (person)
        insurance = self.env['ehr_cdss.patient.insurance'].search([('patient_id', '=', record_id)], limit=1)
        
        if not insurance:
            # Handle case where no medical history exists for the patient
            insurance = self.env['ehr_cdss.patient.insurance'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.insurance',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': insurance.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        
    # @api.multi
    def open_insurance_record(self):
        self.ensure_one()
        insurance = self.env['ehr_cdss.patient.insurance_patient'].search([
            ('patient_id', '=', self.id)
        ], limit=1)

        if not insurance:
            insurance = self.env['ehr_cdss.patient.insurance_patient'].create({
                'patient_id': self.id,
                'user_id': self.env.user.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.insurance_patient',
            'view_mode': 'form',
            'res_id': insurance.id,
            'target': 'current',
            'context': {'from_patient_form': True},
        }
    
    def open_allergy_record(self):
        self.ensure_one()
        allergy = self.env['ehr_cdss.patient.allergy'].search([
            ('patient_id', '=', self.id)
        ], limit=1)

        if not allergy:
            allergy = self.env['ehr_cdss.patient.allergy'].create({
                'patient_id': self.id,
                'user_id': self.env.user.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.allergy',
            'view_mode': 'form',
            'res_id': allergy.id,
            'target': 'current',
            'context': {'from_patient_form': True},
        }

        

class PatientInsurance(models.Model):
    _name = 'ehr_cdss.patient.insurance'
    _description = 'Insurance and Financial Information'
    _rec_name = 'patient_id'  # or whatever field you want shown


    patient_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True, tracking=True)
    insurance_status = fields.Selection([
        ('private', 'Private'),
        ('medicare', 'Medicare'),
        ('medicaid', 'Medicaid'),
        ('veterans', 'Veterans'),
        ('none', 'None'),
        ('other', 'Other')
    ], string='Insurance Status')
    user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)

    primary_insurance = fields.Char(string='Primary Insurance Name')
    primary_insurance_id = fields.Char(string='Primary Insurance ID')
    primary_insurance_group = fields.Char(string='Primary Insurance Group')

    primary_insurance_holder = fields.Selection([
        ('self', 'Self'),
        ('spouse', 'Spouse'),
        ('parent', 'Parent'),
        ('other', 'Other')
    ], string='Primary Insurance Holder')

    primary_insurance_holder_name = fields.Char(string='Primary Insurance Holder Name')
    primary_insurance_holder_dob = fields.Date(string='Primary Insurance Holder DOB')

    secondary_insurance = fields.Char(string='Secondary Insurance Name')
    secondary_insurance_id = fields.Char(string='Secondary Insurance ID')
    secondary_insurance_group = fields.Char(string='Secondary Insurance Group')

    financial_assistance = fields.Boolean(string='Financial Assistance Program')
    financial_counseling = fields.Boolean(string='Financial Counseling Offered')

    pharmacy_preference = fields.Char(string='Preferred Pharmacy')
    pharmacy_address = fields.Char(string='Pharmacy Address')
    pharmacy_phone = fields.Char(string='Pharmacy Phone')
    show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')


    @api.depends_context('from_patient_form')
    def _compute_show_back_button(self):
        for rec in self:
            print("rec: ",rec)
            rec.show_back_button = self._context.get('from_patient_form', False)
            
    
    
    def action_medical_history(self):
        # Assuming 'self' is a record for a person or patient.
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        medical_history = self.env['ehr_cdss.medical.history'].search([('patient_id', '=', record_id)], limit=1)
        
        if not medical_history:
            # Handle case where no medical history exists for the patient
            medical_history = self.env['ehr_cdss.medical.history'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        return { 
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.history',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': medical_history.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag

            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
    
    def action_family_history(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        family_history = self.env['ehr_cdss.medical.family.history'].search([('patient_id', '=', record_id)], limit=1)
        
        if not family_history:
            # Handle case where no medical history exists for the patient
            family_history = self.env['ehr_cdss.medical.family.history'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.family.history',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': family_history.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trig
        }
        
        
    def action_immunization_infectious_disease(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        immunization_id = self.env['ehr_cdss.patient.immunization.record'].search([('partner_id', '=', record_id)], limit=1)
        
        if not immunization_id:
            # Handle case where no medical history exists for the patient
            immunization_id = self.env['ehr_cdss.patient.immunization.record'].create({
                'partner_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.immunization.record',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': immunization_id.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }

    
    def action_appointment(self):
        record_id = self.patient_id.id # Get the ID of the current record (person)
        appointment = self.env['ehr_cdss.appointment'].search([('patient_id', '=', record_id)], limit=1)
        
        if not appointment:
            # Handle case where no medical history exists for the patient
            appointment = self.env['ehr_cdss.appointment'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.appointment',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': appointment.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        
    def action_medical_patient_allergy(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].search([('patient_id', '=', record_id)], limit=1)
        
        if not patient_allergy:
            # Handle case where no medical history exists for the patient
            patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.patient.allergy',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': patient_allergy.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        

    def action_medication(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        medication = self.env['ehr_cdss.medical.medication'].search([('patient_id', '=', record_id)], limit=1)
        
        if not medication:
            # Handle case where no medical history exists for the patient
            medication = self.env['ehr_cdss.medical.medication'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.medication',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': medication.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        
    def action_document(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        document = self.env['ehr_cdss.document'].search([('patient_id', '=', record_id)], limit=1)
        
        if not document:
            # Handle case where no medical history exists for the patient
            document = self.env['ehr_cdss.document'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.document',  # Replace with actual model
            'view_mode': 'kanban,form',
            'view_type': 'form',
            'res_id': document.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'domain': [('patient_id', '=', record_id)],  # Filter documents by patient
            'context': {'search_default_filter_by_patient': 1, 'default_patient_id': record_id},
        }
    
    def action_back_to_patient(self):
        """ Redirect back to the Patient form """
        print("patient_id: ",self.patient_id.id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.info',
            'view_mode': 'form',
            'res_id': self.patient_id.id,  # Open the related patient record
            'target': 'current',
        }
    def dummy_action(self):
        pass  # Do nothing
    
    
    @api.depends('allergy_ids')
    def _compute_allergy_count(self):
        for patient in self:
            patient.allergy_count = len(patient.allergy_ids.filtered(lambda a: a.active))
    
    @api.depends('allergy_ids', 'allergy_ids.severity_id', 'allergy_ids.active')
    def _compute_has_critical_allergies(self):
        critical_severity = self.env['ehr_cdss.medical.allergy.severity'].search([('name', 'in', ['Severe', 'Critical', 'Life-threatening'])])
        for patient in self:
            patient.has_critical_allergies = bool(patient.allergy_ids.filtered(lambda a: a.active and a.severity_id in critical_severity))
    
    @api.depends('allergy_band_ids', 'allergy_band_ids.state')
    def _compute_current_allergy_band(self):
        for patient in self:
            current_band = patient.allergy_band_ids.filtered(lambda b: b.state == 'applied')
            patient.current_allergy_band = current_band[0] if current_band else False
    
    def action_view_allergies(self):
        self.ensure_one()
        return {
            'name': 'Patient Allergies',
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.patient.allergy',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }
    
    def action_apply_allergy_band(self):
        self.ensure_one()
        return {
            'name': 'Apply Allergy Band',
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.allergy.band.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_allergy_ids': self.allergy_ids.filtered(lambda a: a.active).ids,
            }
        }
    
    def action_verify_emr_allergies(self):
        self.ensure_one()
        return {
            'name': 'Verify EMR Allergies',
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.emr.allergy.verification.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
            }
        }
        

class insurance_patient(models.Model):
        _name = 'ehr_cdss.patient.insurance_patient'
        _description = 'Insurance and Financial Information'
        _rec_name = 'patient_id'  # or whatever field you want shown
        
        patient_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True, tracking=True)
        insurance_ids = fields.One2many('ehr_cdss.patient.insurance', 'patient_id', string='Insurance Records')
        user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
        show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')

        
        @api.depends_context('from_patient_form')
        def _compute_show_back_button(self):
            for rec in self:
                print("rec: ",rec)
                rec.show_back_button = self._context.get('from_patient_form', False)
                
        
        
        def action_medical_history(self):
            # Assuming 'self' is a record for a person or patient.
            record_id = self.patient_id.id  # Get the ID of the current record (person)
            medical_history = self.env['ehr_cdss.medical.history'].search([('patient_id', '=', record_id)], limit=1)
            
            if not medical_history:
                # Handle case where no medical history exists for the patient
                medical_history = self.env['ehr_cdss.medical.history'].create({
                    'patient_id': record_id,
                    'user_id': self.env.user.id,  # Associate the current user who is creating the record
                })
                # raise UserError("No medical history record found for this patient.")
            print("record_id",record_id)
            return { 
                'type': 'ir.actions.act_window',
                'res_model': 'ehr_cdss.medical.history',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': medical_history.id,  # Pass the record ID of the person to be displayed
                'target': 'current',  # Open in the same window or use 'new' for a popup
                'context': {'from_patient_form': True},  # ✅ pass context flag

                'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
            }
        
        def action_family_history(self):
            record_id = self.patient_id.id  # Get the ID of the current record (person)
            
            family_history = self.env['ehr_cdss.medical.family.history'].search([('patient_id', '=', record_id)], limit=1)
            
            if not family_history:
                # Handle case where no medical history exists for the patient
                family_history = self.env['ehr_cdss.medical.family.history'].create({
                    'patient_id': record_id,
                    'user_id': self.env.user.id,  # Associate the current user who is creating the record
                })
                # raise UserError("No medical history record found for this patient.")
            print("record_id",record_id)
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ehr_cdss.medical.family.history',  # Replace with actual model
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': family_history.id,  # Pass the record ID of the person to be displayed
                'target': 'current',  # Open in the same window or use 'new' for a popup
                'context': {'from_patient_form': True},  # ✅ pass context flag
                'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trig
            }
            
            
        def action_immunization_infectious_disease(self):
            record_id = self.patient_id.id  # Get the ID of the current record (person)
            
            immunization_id = self.env['ehr_cdss.patient.immunization.record'].search([('partner_id', '=', record_id)], limit=1)
            
            if not immunization_id:
                # Handle case where no medical history exists for the patient
                immunization_id = self.env['ehr_cdss.patient.immunization.record'].create({
                    'partner_id': record_id,
                    'user_id': self.env.user.id,  # Associate the current user who is creating the record
                })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ehr_cdss.patient.immunization.record',  # Replace with actual model
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': immunization_id.id,  # Pass the record ID of the person to be displayed
                'target': 'current',  # Open in the same window or use 'new' for a popup
                'context': {'from_patient_form': True},  # ✅ pass context flag
                'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
            }

        
        def action_appointment(self):
            record_id = self.patient_id.id # Get the ID of the current record (person)
            appointment = self.env['ehr_cdss.appointment'].search([('patient_id', '=', record_id)], limit=1)
            
            if not appointment:
                # Handle case where no medical history exists for the patient
                appointment = self.env['ehr_cdss.appointment'].create({
                    'patient_id': record_id,
                    'user_id': self.env.user.id,  # Associate the current user who is creating the record
                })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ehr_cdss.appointment',  # Replace with actual model
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': appointment.id,  # Pass the record ID of the person to be displayed
                'target': 'current',
                'context': {'from_patient_form': True},  # ✅ pass context flag
                'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
            }
            
        def action_medical_patient_allergy(self):
            record_id = self.patient_id.id  # Get the ID of the current record (person)
            patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].search([('patient_id', '=', record_id)], limit=1)
            
            if not patient_allergy:
                # Handle case where no medical history exists for the patient
                patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].create({
                    'patient_id': record_id,
                    'user_id': self.env.user.id,  # Associate the current user who is creating the record
                })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ehr_cdss.medical.patient.allergy',  # Replace with actual model
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': patient_allergy.id,  # Pass the record ID of the person to be displayed
                'target': 'current',
                'context': {'from_patient_form': True},  # ✅ pass context flag
                'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
            }
            

        def action_medication(self):
            record_id = self.patient_id.id  # Get the ID of the current record (person)
            medication = self.env['ehr_cdss.medical.medication'].search([('patient_id', '=', record_id)], limit=1)
            
            if not medication:
                # Handle case where no medical history exists for the patient
                medication = self.env['ehr_cdss.medical.medication'].create({
                    'patient_id': record_id,
                    'user_id': self.env.user.id,  # Associate the current user who is creating the record
                })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ehr_cdss.medical.medication',  # Replace with actual model
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': medication.id,  # Pass the record ID of the person to be displayed
                'target': 'current',
                'context': {'from_patient_form': True},  # ✅ pass context flag
                'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
            }
            
        def action_document(self):
            record_id = self.patient_id.id  # Get the ID of the current record (person)
            document = self.env['ehr_cdss.document'].search([('patient_id', '=', record_id)], limit=1)
            
            if not document:
                # Handle case where no medical history exists for the patient
                document = self.env['ehr_cdss.document'].create({
                    'patient_id': record_id,
                    'user_id': self.env.user.id,  # Associate the current user who is creating the record
                })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ehr_cdss.document',  # Replace with actual model
                'view_mode': 'kanban,form',
                'view_type': 'form',
                'res_id': document.id,  # Pass the record ID of the person to be displayed
                'target': 'current',
                'domain': [('patient_id', '=', record_id)],  # Filter documents by patient
                'context': {'search_default_filter_by_patient': 1, 'default_patient_id': record_id},
            }
            
            
        def open_insurance_record(self):
            self.ensure_one()
            record_id = self.patient_id.id  # Get the ID of the current record (person)
            
            insurance = self.env['ehr_cdss.patient.insurance_patient'].search([
                ('patient_id', '=', record_id)
            ], limit=1)

            if not insurance:
                insurance = self.env['ehr_cdss.patient.insurance_patient'].create({
                    'patient_id': record_id,
                    'user_id': self.env.user.id,
                })

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ehr_cdss.patient.insurance_patient',
                'view_mode': 'form',
                'res_id': insurance.id,
                'target': 'current',
                'context': {'from_patient_form': True},
            }
        
        def open_allergy_record(self):
            self.ensure_one()
            record_id = self.patient_id.id  # Get the ID of the current record (person)
            
            allergy = self.env['ehr_cdss.patient.allergy'].search([
                ('patient_id', '=', record_id)
            ], limit=1)

            if not allergy:
                allergy = self.env['ehr_cdss.patient.allergy'].create({
                    'patient_id': record_id,
                    'user_id': self.env.user.id,
                })

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ehr_cdss.patient.allergy',
                'view_mode': 'form',
                'res_id': allergy.id,
                'target': 'current',
                'context': {'from_patient_form': True},
            }
        
        def action_back_to_patient(self):
            """ Redirect back to the Patient form """
            print("patient_id: ",self.patient_id.id)
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ehr_cdss.patient.info',
                'view_mode': 'form',
                'res_id': self.patient_id.id,  # Open the related patient record
                'target': 'current',
            }
        
        def dummy_action(self):
            pass  # Do nothing



class AllergyPatient(models.Model):
    _name = 'ehr_cdss.patient.allergy'
    _description = 'Allergy Information'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
    show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')

    allergy_ids = fields.One2many('ehr_cdss.medical.patient.allergy', 'patient_id', string='Allergies')
    allergy_count = fields.Integer(compute='_compute_allergy_count', string='Allergy Count')
    has_critical_allergies = fields.Boolean(compute='_compute_has_critical_allergies', string='Has Critical Allergies', store=True)
    allergy_band_ids = fields.One2many('ehr_cdss.medical.patient.allergy.band', 'patient_id', string='Allergy Bands')
    current_allergy_band = fields.Many2one('ehr_cdss.medical.patient.allergy.band', compute='_compute_current_allergy_band', string='Current Allergy Band')

    @api.depends('allergy_ids')
    def _compute_allergy_count(self):
        for patient in self:
            patient.allergy_count = len(patient.allergy_ids.filtered(lambda a: a.active))

    @api.depends('allergy_ids', 'allergy_ids.severity_id', 'allergy_ids.active')
    def _compute_has_critical_allergies(self):
        critical_severity = self.env['ehr_cdss.medical.allergy.severity'].search([
            ('name', 'in', ['Severe', 'Critical', 'Life-threatening'])
        ])
        for patient in self:
            patient.has_critical_allergies = bool(
                patient.allergy_ids.filtered(lambda a: a.active and a.severity_id in critical_severity)
            )

    @api.depends('allergy_band_ids', 'allergy_band_ids.state')
    def _compute_current_allergy_band(self):
        for patient in self:
            current_band = patient.allergy_band_ids.filtered(lambda b: b.state == 'applied')
            patient.current_allergy_band = current_band[0] if current_band else False

    def action_view_allergies(self):
        self.ensure_one()
        return {
            'name': 'Patient Allergies',
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.patient.allergy',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_apply_allergy_band(self):
        self.ensure_one()
        return {
            'name': 'Apply Allergy Band',
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.allergy.band.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_allergy_ids': self.allergy_ids.filtered(lambda a: a.active).ids,
            }
        }

    def action_verify_emr_allergies(self):
        self.ensure_one()
        return {
            'name': 'Verify EMR Allergies',
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.emr.allergy.verification.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
            }
        }

    
    @api.depends_context('from_patient_form')
    def _compute_show_back_button(self):
        for rec in self:
            print("rec: ",rec)
            rec.show_back_button = self._context.get('from_patient_form', False)
            
    
    
    def action_medical_history(self):
        # Assuming 'self' is a record for a person or patient.
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        medical_history = self.env['ehr_cdss.medical.history'].search([('patient_id', '=', record_id)], limit=1)
        
        if not medical_history:
            # Handle case where no medical history exists for the patient
            medical_history = self.env['ehr_cdss.medical.history'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        return { 
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.history',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': medical_history.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag

            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
    
    def action_family_history(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        family_history = self.env['ehr_cdss.medical.family.history'].search([('patient_id', '=', record_id)], limit=1)
        
        if not family_history:
            # Handle case where no medical history exists for the patient
            family_history = self.env['ehr_cdss.medical.family.history'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.family.history',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': family_history.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trig
        }
        
        
    def action_immunization_infectious_disease(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        immunization_id = self.env['ehr_cdss.patient.immunization.record'].search([('partner_id', '=', record_id)], limit=1)
        
        if not immunization_id:
            # Handle case where no medical history exists for the patient
            immunization_id = self.env['ehr_cdss.patient.immunization.record'].create({
                'partner_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.immunization.record',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': immunization_id.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }

    
    def action_appointment(self):
        record_id = self.patient_id.id # Get the ID of the current record (person)
        appointment = self.env['ehr_cdss.appointment'].search([('patient_id', '=', record_id)], limit=1)
        
        if not appointment:
            # Handle case where no medical history exists for the patient
            appointment = self.env['ehr_cdss.appointment'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.appointment',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': appointment.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        
    def action_medical_patient_allergy(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].search([('patient_id', '=', record_id)], limit=1)
        
        if not patient_allergy:
            # Handle case where no medical history exists for the patient
            patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.patient.allergy',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': patient_allergy.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
    
    def action_back_to_patient(self):
        """ Redirect back to the Patient form """
        print("patient_id: ",self.patient_id.id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.info',
            'view_mode': 'form',
            'res_id': self.patient_id.id,  # Open the related patient record
            'target': 'current',
        }

    def action_medication(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        medication = self.env['ehr_cdss.medical.medication'].search([('patient_id', '=', record_id)], limit=1)
        
        if not medication:
            # Handle case where no medical history exists for the patient
            medication = self.env['ehr_cdss.medical.medication'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.medication',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': medication.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        
    def action_document(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        document = self.env['ehr_cdss.document'].search([('patient_id', '=', record_id)], limit=1)
        
        if not document:
            # Handle case where no medical history exists for the patient
            document = self.env['ehr_cdss.document'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.document',  # Replace with actual model
            'view_mode': 'kanban,form',
            'view_type': 'form',
            'res_id': document.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'domain': [('patient_id', '=', record_id)],  # Filter documents by patient
            'context': {'search_default_filter_by_patient': 1, 'default_patient_id': record_id},
        }
        
        
    def open_insurance_record(self):
        self.ensure_one()
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        insurance = self.env['ehr_cdss.patient.insurance_patient'].search([
            ('patient_id', '=', record_id)
        ], limit=1)

        if not insurance:
            insurance = self.env['ehr_cdss.patient.insurance_patient'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.insurance_patient',
            'view_mode': 'form',
            'res_id': insurance.id,
            'target': 'current',
            'context': {'from_patient_form': True},
        }
    
    def open_allergy_record(self):
        self.ensure_one()
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        allergy = self.env['ehr_cdss.patient.allergy'].search([
            ('patient_id', '=', record_id)
        ], limit=1)

        if not allergy:
            allergy = self.env['ehr_cdss.patient.allergy'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.allergy',
            'view_mode': 'form',
            'res_id': allergy.id,
            'target': 'current',
            'context': {'from_patient_form': True},
        }
    
    def dummy_action(self):
        pass  # Do nothing

