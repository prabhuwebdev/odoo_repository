from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = 'ehr_cdss.patient'
    _description = 'Patient Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    # Basic Information
    name = fields.Char(string="Patient Name", required=True, tracking=True)
    mrn = fields.Char(string="Medical Record Number", required=True, tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    image = fields.Binary(string="Patient Image")
    
    # Demographics
    demographics_id = fields.Many2one('ehr_cdss.demographics', string="Demographics")
    birth_date = fields.Date(string="Date of Birth", tracking=True)
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_binary', 'Non-Binary'),
        ('transgender_ftm', 'Transgender FTM'),
        ('transgender_mtf', 'Transgender MTF'),
        ('other', 'Other'),
        ('unknown', 'Unknown'),
    ], string="Gender Identity", tracking=True)
    pronouns = fields.Many2many('ehr_cdss.pronoun', string="Pronouns")
    marital_status = fields.Selection([
        ('single', 'Single/Never Married'),
        ('married', 'Married or Domestic Partnership'),
        ('separated', 'Separated'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ], string="Marital Status", tracking=True)
    sexual_orientation = fields.Many2many('ehr_cdss.sexual_orientation', string="Sexual Orientation")
    
    # Ethnicity and Language
    race_ids = fields.Many2many('ehr_cdss.race', string="Race")
    ethnicity = fields.Selection([
        ('hispanic', 'Hispanic'),
        ('not_hispanic', 'Not Hispanic')
    ], string="Ethnicity", tracking=True)
    preferred_language_id = fields.Many2one('res.lang', string="Preferred Language")
    interpreter_needed = fields.Boolean(string="Interpreter Needed")
    
    # Contact Information
    contact_info_id = fields.Many2one('ehr_cdss.contact.info', string="Contact Information")
    address_id = fields.Many2one('ehr_cdss.address', string="Address")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    emergency_contact_ids = fields.One2many('ehr_cdss.contact', 'patient_id', string="Emergency Contacts")
    
    # Clinical Information
    primary_provider_id = fields.Many2one('ehr_cdss.provider', string="Primary Provider")
    insurance_ids = fields.One2many('ehr_cdss.insurance', 'patient_id', string="Insurance Plans")
    diagnosis_ids = fields.One2many('ehr_cdss.diagnosis', 'patient_id', string="Diagnoses")
    medical_record_ids = fields.One2many('ehr_cdss.medical.record', 'patient_id', string="Medical Records")
    treatment_plan_ids = fields.One2many('ehr_cdss.treatment.plan', 'patient_id', string="Treatment Plans")
    appointment_ids = fields.One2many('ehr_cdss.appointment', 'patient_id', string="Appointments")
    document_ids = fields.One2many('ehr_cdss.document', 'patient_id', string="Documents")
    
    # Medical History
    medical_history = fields.Text(string="Medical History")
    surgical_history = fields.Text(string="Surgical History")
    psychiatric_history = fields.Text(string="Psychiatric History")
    current_medications = fields.Text(string="Current Medications")
    allergies = fields.Text(string="Allergies")
    
    # Family History
    family_history = fields.Text(string="Family History")
    family_mental_health_history = fields.Text(string="Family Mental Health History")
    family_substance_use_history = fields.Text(string="Family Substance Use History")
    
    # Social History
    social_history = fields.Text(string="Social History")
    occupation = fields.Char(string="Occupation")
    employment_status = fields.Selection([
        ('employed_full', 'Employed Full Time (>35 hours/week)'),
        ('employed_part', 'Employed Part Time'),
        ('unemployed', 'Unemployed'),
        ('student', 'Student'),
        ('homemaker', 'Homemaker'),
        ('military', 'Military'),
        ('retired', 'Retired'),
        ('disabled', 'Disabled'),
        ('self_employed', 'Self Employed'),
    ], string="Employment Status")
    employer_or_school = fields.Char(string="Employer or School Name")
    education_level = fields.Selection([
        ('current_student', 'Current Student'),
        ('less_than_high_school', 'Less than High School'),
        ('high_school_ged', 'High School/GED'),
        ('some_college', 'Some College'),
        ('college_graduate', 'College Graduate'),
        ('post_grad', 'Post-Graduate'),
        ('as_degree', 'AS Degree'),
        ('vocational_college', 'Vocational College'),
    ], string="Highest Level of Education")
    
    # Substance Use
    substance_use_ids = fields.One2many('ehr_cdss.substance.use', 'patient_id', string="Substance Use")
    
    # Psychosocial
    trauma_abuse_history = fields.Boolean(string="Trauma or Abuse History")
    trauma_abuse_description = fields.Text(string="Trauma/Abuse Description")
    strengths = fields.Text(string="Patient Strengths")
    social_concerns = fields.Text(string="Social Concerns")
    interpersonal_family_info = fields.Text(string="Interpersonal/Family Information")
    living_situation = fields.Text(string="Current Living Situation")
    cultural_considerations = fields.Text(string="Cultural Considerations for Treatment")
    
    # Risk Assessment
    risk_assessment_ids = fields.One2many('ehr_cdss.risk.assessment', 'patient_id', string="Risk Assessments")
    safety_plan_ids = fields.One2many('ehr_cdss.safety.plan', 'patient_id', string="Safety Plans")
    
    # Child/Adolescent Specific
    is_minor = fields.Boolean(string="Is a Minor")
    parent_guardian_ids = fields.Many2many('ehr_cdss.contact', string="Parents/Guardians")
    custody_arrangements = fields.Text(string="Custody Arrangements")
    developmental_history = fields.Text(string="Developmental History")
    school_performance = fields.Text(string="School Performance")
    
    # Administrative
    date_registered = fields.Date(string="Registration Date")
    referral_source = fields.Char(string="Referral Source")
    consent_for_treatment = fields.Boolean(string="Consent for Treatment Obtained")
    telehealth_appropriate = fields.Boolean(string="Appropriate for Telehealth")
    
    # State Fields
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('discharged', 'Discharged'),
    ], string="Status", default='active', tracking=True)
    
    _sql_constraints = [
        ('mrn_unique', 'UNIQUE(mrn)', 'Medical Record Number must be unique!')
    ]
    
    @api.depends('birth_date')
    def _compute_age(self):
        """Compute age based on birth date"""
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                record.age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0


class PatientSubstanceUse(models.Model):
    _name = 'ehr_cdss.substance.use'
    _description = 'Patient Substance Use'
    
    patient_id = fields.Many2one('ehr_cdss.patient', string="Patient", required=True)
    substance = fields.Selection([
        ('alcohol', 'Alcohol'),
        ('tobacco', 'Tobacco'),
        ('cannabis', 'Cannabis'),
        ('stimulants', 'Stimulants'),
        ('opioids', 'Opioids'),
        ('hallucinogens', 'Hallucinogens'),
        ('sedatives', 'Sedatives'),
        ('other', 'Other'),
    ], string="Substance", required=True)
    other_substance = fields.Char(string="Other Substance Name")
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('occasionally', 'Occasionally'),
    ], string="Frequency of Use")
    last_use_date = fields.Date(string="Date of Last Use")
    first_use_age = fields.Integer(string="Age of First Use")
    details = fields.Text(string="Details of Substance Use")
    is_current = fields.Boolean(string="Current Use", default=True)


class PatientRiskAssessment(models.Model):
    _name = 'ehr_cdss.risk.assessment'
    _description = 'Patient Risk Assessment'
    _order = 'assessment_date desc'
    
    patient_id = fields.Many2one('ehr_cdss.patient', string="Patient", required=True)
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", required=True)
    assessment_date = fields.Datetime(string="Assessment Date", default=fields.Datetime.now)
    
    # Columbia Suicide Severity Rating Scale
    cssr_q1 = fields.Boolean(string="Wished dead or to sleep and not wake up")
    cssr_q2 = fields.Boolean(string="Had thoughts of killing themselves")
    cssr_q3 = fields.Boolean(string="Thinking about how to kill themselves")
    cssr_q4 = fields.Boolean(string="Had thoughts with intention to act")
    cssr_q5 = fields.Boolean(string="Started to work out details of suicide plan")
    cssr_q6 = fields.Boolean(string="Ever done anything to end life")
    cssr_q6a = fields.Boolean(string="Done anything to end life in lifetime")
    cssr_q6b = fields.Boolean(string="Done anything to end life in past 3 months")
    cssr_rating = fields.Selection([
        ('no_risk', 'No Risk Reported'),
        ('low_risk', 'Low Risk'),
        ('moderate_risk', 'Moderate Risk'),
        ('high_risk', 'High Risk'),
    ], string="Columbia Scale Rating", compute="_compute_cssr_rating", store=True)
    
    # Self Risk
    prior_si_attempts = fields.Boolean(string="Prior Suicidal Ideation/Attempts")
    prior_si_description = fields.Text(string="Prior SI/Attempt Description")
    current_si = fields.Selection([
        ('none', 'No'),
        ('occasional', 'Occasional/Fleeting'),
        ('half_time', 'More than half the time'),
        ('constant', 'Constant'),
    ], string="Current Suicidal Ideation")
    current_intent = fields.Boolean(string="Current Suicidal Intent")
    intent_description = fields.Text(string="Intent Description")
    current_plan = fields.Boolean(string="Current Suicidal Plan")
    plan_description = fields.Text(string="Plan Description")
    access_to_means = fields.Boolean(string="Access to Means")
    means_description = fields.Text(string="Means Description")
    self_harm = fields.Boolean(string="Self-Harm Behaviors")
    self_harm_description = fields.Text(string="Self-Harm Description")
    
    # Risk to Others
    prior_aggression = fields.Boolean(string="Prior Physical Aggression/Property Destruction")
    prior_aggression_description = fields.Text(string="Prior Aggression Description")
    current_aggression = fields.Boolean(string="Current Physical Aggression/Property Destruction")
    current_aggression_description = fields.Text(string="Current Aggression Description")
    homicidal_ideation = fields.Boolean(string="Current Homicidal Ideation")
    homicidal_ideation_description = fields.Text(string="Homicidal Ideation Description")
    access_to_weapons = fields.Boolean(string="Access to Weapons")
    weapons_description = fields.Text(string="Weapons Description")
    
    # Overall Risk Assessment
    overall_risk_rating = fields.Selection([
        ('none', 'None Reported'),
        ('low', 'Low/Mild'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
    ], string="Overall Risk Rating")
    risk_explanation = fields.Text(string="Risk Explanation")
    safety_plan_created = fields.Boolean(string="Safety Plan Created")
    safety_plan_id = fields.Many2one('ehr_cdss.safety.plan', string="Associated Safety Plan")
    
    @api.depends('cssr_q1', 'cssr_q2', 'cssr_q3', 'cssr_q4', 'cssr_q5', 'cssr_q6', 'cssr_q6a', 'cssr_q6b')
    def _compute_cssr_rating(self):
        for record in self:
            if record.cssr_q4 or record.cssr_q5 or record.cssr_q6b:
                record.cssr_rating = 'high_risk'
            elif record.cssr_q3 or record.cssr_q6a:
                record.cssr_rating = 'moderate_risk'
            elif record.cssr_q1 or record.cssr_q2:
                record.cssr_rating = 'low_risk'
            else:
                record.cssr_rating = 'no_risk'


class Pronoun(models.Model):
    _name = 'ehr_cdss.pronoun'
    _description = 'Gender Pronouns'
    
    name = fields.Char(string="Pronoun", required=True)


class SexualOrientation(models.Model):
    _name = 'ehr_cdss.sexual_orientation'
    _description = 'Sexual Orientation'
    
    name = fields.Char(string="Sexual Orientation", required=True)


class Race(models.Model):
    _name = 'ehr_cdss.race'
    _description = 'Race Categories'
    
    name = fields.Char(string="Race", required=True)
    description = fields.Text(string="Description")
