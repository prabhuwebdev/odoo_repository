from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random
import string

class Assessment(models.Model):
    _name = 'ehr_cdss.assessment'
    _description = 'Clinical Assessment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Assessment ID", readonly=True, default=lambda self: self._generate_patient_id())
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient", required=True, tracking=True)
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", required=True, tracking=True)
    date = fields.Date(string="Assessment Date", default=fields.Date.today, tracking=True)
    
    # Assessment Type
    assessment_type = fields.Selection([
        ('initial', 'Initial Assessment'),
        ('reassessment', 'Reassessment'),
        ('discharge', 'Discharge Assessment'),
        ('crisis', 'Crisis Assessment'),
        ('other', 'Other'),
    ], string="Assessment Type", required=True, tracking=True)
    
    # Service Information
    service_provided = fields.Selection([
        ('individual_therapy', 'Individual Therapy'),
        ('couples_therapy', 'Couples Therapy'),
        ('family_therapy', 'Family Therapy'),
        ('group_therapy', 'Group Therapy'),
        ('other', 'Other'),
    ], string="Service Provided")
    present_at_session = fields.Text(string="Present at Session")
    
    # Service Delivery
    location = fields.Selection([
        ('telehealth', 'Telehealth'),
        ('office', 'Office (in person)'),
    ], string="Location of Service")
    telehealth_confirmation = fields.Selection([
        ('home', 'Yes – client at home'),
        ('other_location', 'Yes – client in another location, which has been confirmed'),
        ('no', 'No'),
    ], string="Telehealth Confirmation")
    telehealth_appropriate = fields.Boolean(string="Client Appropriate for Telehealth")
    
    # Measures Administration
    baseline_measures_completed = fields.Boolean(string="Client Completed Baseline Measures")
    measures_reviewed = fields.Boolean(string="Measures Reviewed with Client")
    
    # History of Present Illness / Chief Complaint
    presenting_problem = fields.Text(string="Presenting Problem/Chief Complaint", tracking=True)
    current_symptoms = fields.Text(string="Current Symptoms", tracking=True)
    # symptom_ids = fields.Many2many('ehr_cdss.symptom', string="Symptoms")
    functional_impairment_areas = fields.Selection([
        ('work', 'Work'),
        ('social', 'Social/Relational'),
        ('school', 'School'),
        ('adl', 'Activities of daily living'),
        ('multiple', 'Multiple areas'),
    ], string="Area(s) of Functional Impairment")
    functional_impairment_details = fields.Text(string="Functional Impairment Details")
    
    # Treatment History
    mental_health_treatment_history = fields.Text(string="Mental Health Treatment History")
    substance_use_treatment_history = fields.Text(string="Substance Use Treatment History")
    family_mental_health_history = fields.Text(string="Family Mental Health/Substance Use History")
    
    # Psychosocial Assessment
    highest_education = fields.Selection([
        ('current_student', 'Current Student'),
        ('less_than_high_school', 'Less than High School'),
        ('high_school_ged', 'High School/GED'),
        ('some_college', 'Some College'),
        ('college_graduate', 'College Graduate'),
        ('post_grad', 'Post-Graduate'),
        ('as_degree', 'AS Degree'),
        ('vocational_college', 'Vocational College'),
    ], string="Highest Level of Education")
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
    employer_school = fields.Char(string="Employer or School Name")
    military_involvement = fields.Boolean(string="Military Involvement")
    military_details = fields.Text(string="Military Details")
    social_concerns = fields.Text(string="Social Concerns")
    interpersonal_family_info = fields.Text(string="Interpersonal/Family Information")
    living_situation = fields.Text(string="Current Living Situation")
    cultural_considerations = fields.Text(string="Cultural Considerations for Treatment")
    
    # Trauma History
    trauma_abuse_history = fields.Boolean(string="Trauma or Abuse History")
    trauma_abuse_description = fields.Text(string="Trauma/Abuse Description")
    
    # Client Strengths
    client_strengths = fields.Text(string="Client Strengths")
    
    # Substance Use Assessment
    substance_use_ids = fields.One2many('ehr_cdss.assessment.substance.use', 'assessment_id', string="Substance Use")
    
    # Health History
    health_history = fields.Text(string="Health History/Current Medical Conditions")
    current_medications = fields.Text(string="Current Medications")
    primary_care_physician = fields.Char(string="Primary Care Physician")
    psychiatrist_np = fields.Char(string="Psychiatrist/NP")
    
    # Risk Assessment
    risk_assessment_id = fields.Many2one('ehr_cdss.risk.assessment', string="Risk Assessment")
    
    # Mental Status Exam
    affect = fields.Many2many('ehr_cdss.mse.affect', string="Affect")
    mood = fields.Many2many('ehr_cdss.mse.mood', string="Mood")
    orientation = fields.Selection([
        ('normal', 'Within Normal Limits'),
        ('person', 'Disoriented- Person'),
        ('situation', 'Disoriented- Situation'),
        ('place', 'Disoriented- Place'),
        ('time', 'Disoriented- Time'),
    ], string="Orientation to Time, Place, and Person")
    recent_memory = fields.Selection([
        ('normal', 'Within normal limits'),
        ('immediate', 'Immediate'),
        ('impaired', 'Impaired'),
        ('intact', 'Intact'),
        ('poor', 'Poor'),
        ('selective', 'Selective'),
        ('brain_fog', 'Brain fog'),
    ], string="Recent Memory")
    remote_memory = fields.Selection([
        ('normal', 'Within normal limits'),
        ('impaired', 'Impaired'),
        ('intact', 'Intact'),
        ('poor', 'Poor'),
        ('selective', 'Selective'),
    ], string="Remote Memory")
    intellect = fields.Selection([
        ('average', 'Average'),
        ('above', 'Above'),
        ('below', 'Below'),
    ], string="Intellect")
    attention_concentration = fields.Many2many('ehr_cdss.mse.attention', string="Attention Span and Concentration")
    grooming_appearance = fields.Many2many('ehr_cdss.mse.grooming', string="Grooming and Appearance")
    behavior = fields.Selection([
        ('appropriate', 'Appropriate to situation'),
        ('inappropriate', 'Inappropriate to situation'),
    ], string="Behavior")
    hallucinations = fields.Selection([
        ('none', 'None'),
        ('present', 'Present'),
    ], string="Hallucinations")
    hallucinations_description = fields.Text(string="Hallucinations Description")
    delusions = fields.Selection([
        ('none', 'None'),
        ('present', 'Present'),
    ], string="Delusions")
    delusions_description = fields.Text(string="Delusions Description")
    obsessions = fields.Selection([
        ('none', 'None'),
        ('present', 'Present'),
    ], string="Obsessions")
    obsessions_description = fields.Text(string="Obsessions Description")
    thought_processes = fields.Many2many('ehr_cdss.mse.thought.process', string="Thought Processes")
    speech = fields.Many2many('ehr_cdss.mse.speech', string="Speech")
    motor = fields.Selection([
        ('normal', 'Normal'),
        ('excessive', 'Excessive'),
        ('slow', 'Slow'),
        ('not_available', 'Not available'),
    ], string="Motor")
    impulse_control = fields.Selection([
        ('adequate', 'Adequate'),
        ('impaired', 'Impaired'),
    ], string="Impulse Control")
    impulse_control_description = fields.Text(string="Impulse Control Description")
    insight = fields.Selection([
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('limited', 'Limited'),
        ('absent', 'Absent'),
    ], string="Insight")
    judgment = fields.Selection([
        ('normal', 'Within Normal Limits'),
        ('minimal', 'Impaired- minimal'),
        ('moderate', 'Impaired - moderate'),
        ('severe', 'Impaired - severe'),
    ], string="Judgment")
    mse_comments = fields.Text(string="MSE Comments")
    
    # Child/Adolescent Specific Fields
    is_minor = fields.Boolean(string="Patient is a Minor", related="patient_id.is_minor")
    minor_verbal_assent = fields.Boolean(string="Reviewed and Obtained Verbal Assent from Minor")
    parent_privacy_agreement = fields.Boolean(string="Reviewed and Obtained Privacy Agreement from Parent/Guardian")
    parent_guardian_names = fields.Text(string="Parent/Guardian Names")
    custody_arrangements = fields.Text(string="Custody Arrangements")
    prenatal_exposure = fields.Selection([
        ('no', 'No'),
        ('unknown', 'Unknown'),
        ('yes', 'Yes'),
    ], string="Prenatal/Perinatal Toxin/Drug Exposure")
    prenatal_exposure_details = fields.Text(string="Exposure Details")
    developmental_milestones = fields.Selection([
        ('early', 'Early'),
        ('normal', 'Normal'),
        ('late', 'Late'),
        ('unknown', 'Unknown'),
    ], string="Developmental Milestones")
    is_adopted = fields.Selection([
        ('no', 'No'),
        ('unknown', 'Unknown'),
        ('yes', 'Yes'),
    ], string="Adopted")
    adoption_age = fields.Integer(string="Age at Adoption")
    parents_marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('cohabitating', 'Cohabitating'),
        ('separated', 'Separated'),
        ('widowed', 'Widowed'),
    ], string="Parents' Marital Status")
    divorce_age = fields.Integer(string="Child's Age at Divorce")
    parent_relationships = fields.Text(string="Relationship with Parents")
    sibling_relationships = fields.Text(string="Relationships with Siblings")
    peer_relationships = fields.Text(string="Relationships with Peers")
    activities_hobbies = fields.Text(string="Activities/Hobbies")
    sexual_behavior_history = fields.Text(string="Sexual Behavior History")
    sleep_patterns = fields.Text(string="Sleep Patterns or Habits")
    eating_habits = fields.Text(string="Eating Habits")
    iep_services = fields.Selection([
        ('no', 'No'),
        ('unknown', 'Unknown'),
        ('yes', 'Yes'),
    ], string="IEP for Special Education Services")
    iep_details = fields.Text(string="IEP Details")
    cps_involvement = fields.Selection([
        ('no', 'No'),
        ('unknown', 'Unknown'),
        ('yes', 'Yes'),
    ], string="CPS Involvement")
    cps_details = fields.Text(string="CPS Details")
    
    # Couples Assessment
    relationship_length = fields.Text(string="Length of Time in Relationship")
    relationship_substance_strain = fields.Boolean(string="Alcohol/Drug Use Contributes to Relationship Strain")
    relationship_substance_details = fields.Text(string="Relationship Substance Use Details")
    relationship_abuse = fields.Boolean(string="History of Abuse in Relationship")
    relationship_abuse_details = fields.Text(string="Relationship Abuse Details")
    couple_strengths = fields.Text(string="Couple Strengths")
    
    # Family Assessment
    family_treatment_reason = fields.Text(string="Why Family Seeking Treatment")
    family_system_description = fields.Text(string="Family System Description")
    family_substance_strain = fields.Boolean(string="Alcohol/Drug Use Contributes to Family Strain")
    family_substance_details = fields.Text(string="Family Substance Use Details")
    family_abuse = fields.Boolean(string="History of Abuse in Family")
    family_abuse_details = fields.Text(string="Family Abuse Details")
    family_strengths = fields.Text(string="Family Strengths")
    
    # Clinical Summary
    clinical_summary = fields.Text(string="Clinical Summary", tracking=True)
    
    # Diagnoses
    # diagnosis_ids = fields.Many2many('ehr_cdss.diagnosis', string="Diagnoses", tracking=True)
    
    # Session Timing
    session_start_time = fields.Datetime(string="Session Start Time")
    session_end_time = fields.Datetime(string="Session End Time")
    session_duration = fields.Float(string="Session Duration (minutes)", compute="_compute_session_duration", store=True)
    
    # Medical Record Integration
    medical_record_id = fields.Many2one('ehr_cdss.medical.record', string="Medical Record")
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Assessment ID must be unique!')
    ]
    
    # @api.model
    # def create(self, vals):
    #     """Generate unique assessment ID"""
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('ehr_cdss.assessment') or _('New')
    #     return super(Assessment, self).create(vals)
    
    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'AS-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    @api.depends('session_start_time', 'session_end_time')
    def _compute_session_duration(self):
        """Compute session duration in minutes"""
        for record in self:
            if record.session_start_time and record.session_end_time:
                delta = record.session_end_time - record.session_start_time
                record.session_duration = delta.total_seconds() / 60
            else:
                record.session_duration = 0


class AssessmentSubstanceUse(models.Model):
    _name = 'ehr_cdss.assessment.substance.use'
    _description = 'Assessment Substance Use'
    
    assessment_id = fields.Many2one('ehr_cdss.assessment', string="Assessment", required=True, ondelete='cascade')
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


# Mental Status Examination Components
class MSEAffect(models.Model):
    _name = 'ehr_cdss.mse.affect'
    _description = 'MSE Affect Types'
    
    name = fields.Char(string="Affect Type", required=True)


class MSEMood(models.Model):
    _name = 'ehr_cdss.mse.mood'
    _description = 'MSE Mood Types'
    
    name = fields.Char(string="Mood Type", required=True)


class MSEAttention(models.Model):
    _name = 'ehr_cdss.mse.attention'
    _description = 'MSE Attention Types'
    
    name = fields.Char(string="Attention Type", required=True)


class MSEGrooming(models.Model):
    _name = 'ehr_cdss.mse.grooming'
    _description = 'MSE Grooming Types'
    
    name = fields.Char(string="Grooming Type", required=True)


class MSEThoughtProcess(models.Model):
    _name = 'ehr_cdss.mse.thought.process'
    _description = 'MSE Thought Process Types'
    
    name = fields.Char(string="Thought Process Type", required=True)


class MSESpeech(models.Model):
    _name = 'ehr_cdss.mse.speech'
    _description = 'MSE Speech Types'
    
    name = fields.Char(string="Speech Type", required=True)
