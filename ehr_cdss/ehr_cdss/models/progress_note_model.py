from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random
import string

class ProgressNote(models.Model):
    _name = 'ehr_cdss.progress.note'
    _description = 'Progress Note'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Note ID", readonly=True, default=lambda self: self._generate_patient_id())
    
    # Relationships
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient", required=True, tracking=True)
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", required=True, tracking=True)
    medical_record_id = fields.Many2one('ehr_cdss.medical.record', string="Medical Record")
    appointment_id = fields.Many2one('ehr_cdss.appointment', string="Related Appointment")
    # treatment_plan_id = fields.Many2one('ehr_cdss.treatment.plan', string="Treatment Plan")
    
    # Session Information
    date_of_service = fields.Date(string="Date of Service", required=True, default=fields.Date.today, tracking=True)
    present_at_session = fields.Selection([
        ('client', 'Client'),
        ('client_partner', 'Client and Partner'),
        ('client_family', 'Client and Family Member(s)'),
        ('client_parent', 'Client and Parent(s)'),
        ('client_guardian', 'Client and Guardian'),
        ('other', 'Other'),
    ], string="Present at Session", required=True)
    present_at_session_other = fields.Char(string="Other Present at Session")
    
    service_provided = fields.Selection([
        ('individual_therapy', 'Individual Therapy'),
        ('couples_therapy', 'Couples Therapy'),
        ('family_therapy', 'Family Therapy'),
        ('group_therapy', 'Group Therapy'),
        ('other', 'Other'),
    ], string="Service Provided", required=True)
    
    # Service Delivery
    location = fields.Selection([
        ('telehealth', 'Telehealth'),
        ('office', 'Office (in person)'),
    ], string="Location of Service", required=True)
    
    telehealth_confirmation = fields.Selection([
        ('home', 'Yes – client at home'),
        ('other_location', 'Yes – client in another location, which has been confirmed'),
        ('no', 'No'),
    ], string="Telehealth Confirmation")
    
    telehealth_appropriate = fields.Boolean(string="Client Appropriate for Telehealth")
    
    # Outcome Measures
    ongoing_measures_completed = fields.Boolean(string="Client Completed Ongoing Measures")
    measures_reviewed = fields.Boolean(string="Measures Reviewed with Client")
    risk_factors_present = fields.Boolean(string="Risk Factors Present", tracking=True)
    
    # Note Content
    # Basic Progress Note Format
    current_symptoms = fields.Text(string="Current Symptoms", tracking=True)
    # symptom_ids = fields.Many2many('ehr_cdss.symptom', string="Symptoms")
    
    functional_impairment_areas = fields.Selection([
        ('work', 'Work'),
        ('social', 'Social/Relational'),
        ('school', 'School'),
        ('adl', 'Activities of daily living'),
        ('multiple', 'Multiple areas'),
    ], string="Area(s) of Functional Impairment")
    
    functional_impairment_details = fields.Text(string="How Symptoms Impact Functioning")
    
    session_focus = fields.Text(string="Focus of Session/Session Summary", required=True, tracking=True)
    
    # treatment_approaches = fields.Many2many('ehr_cdss.treatment.approach', string="Treatment Approaches Used")
    # intervention_ids = fields.Many2many('ehr_cdss.intervention', string="Interventions Used")
    specific_interventions = fields.Text(string="Specific Interventions")
    
    client_response = fields.Text(string="Client's Response to Interventions", required=True)
    
    plan = fields.Text(string="Plan/Homework for Next Session", required=True)
    
    progress_towards_goals = fields.Selection([
        ('no_change', 'No change since last visit'),
        ('some_progress', 'Some progress apparent'),
        ('significant_progress', 'Significant Progress'),
        ('maintaining', 'Maintaining/stable'),
        ('some_regression', 'Some regression of progress'),
        ('significant_regression', 'Significant regression of progress'),
    ], string="Progress Towards Treatment Goals", required=True, tracking=True)
    
    # SOAP Note Format
    is_soap_format = fields.Boolean(string="Use SOAP Format")
    
    subjective = fields.Text(string="Subjective",
                            help="Patient's reported symptoms, concerns, and medical history in their own words")
    
    objective = fields.Text(string="Objective",
                           help="Measurable data such as observations, test results, and physical exam findings")
    
    assessment = fields.Text(string="Assessment",
                            help="Provider's diagnosis or interpretation based on subjective and objective findings")
    
    plan = fields.Text(string="Plan",
                      help="Next steps for treatment, including interventions, medications, and follow-up")
    
    # Diagnosis
    diagnosis_ids = fields.Many2many('ehr_cdss.diagnosis', string="Diagnoses", tracking=True)
    
    # Session Timing
    session_start_time = fields.Datetime(string="Session Start Time", required=True)
    session_end_time = fields.Datetime(string="Session End Time", required=True)
    session_duration = fields.Float(string="Session Duration (minutes)", compute="_compute_session_duration", store=True)
    
    # Billing Information
    service_code = fields.Selection([
        ('90791', '90791 - Initial Assessment'),
        ('90832', '90832 - Psychotherapy, 16-37 min'),
        ('90834', '90834 - Psychotherapy, 38-52 min'),
        ('90837', '90837 - Psychotherapy, 53+ min'),
        ('90839', '90839 - Psychotherapy for crisis, 30-74 min'),
        ('90840', '90840 - Psychotherapy for crisis, add-on'),
        ('90846', '90846 - Family/couples therapy without client'),
        ('90847', '90847 - Family/couples therapy'),
        ('other', 'Other'),
    ], string="Service Code", required=True)
    service_code_other = fields.Char(string="Other Service Code")
    
    # Document Integration
    # document_id = fields.Many2one('ehr_cdss.document', string="Related Document")
    
    # Signature
    provider_signature = fields.Binary(string="Provider Signature")
    provider_sign_date = fields.Datetime(string="Provider Signature Date")
    
    # State
    state = fields.Selection([
        ('draft', 'Draft'),
        ('signed', 'Signed'),
        ('locked', 'Locked'),
    ], string="Status", default='draft', tracking=True)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Note ID must be unique!')
    ]
    
    
    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'PN-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    @api.depends('session_start_time', 'session_end_time')
    def _compute_session_duration(self):
        """Compute session duration in minutes"""
        for record in self:
            if record.session_start_time and record.session_end_time:
                delta = record.session_end_time - record.session_start_time
                record.session_duration = delta.total_seconds() / 60
            else:
                record.session_duration = 0
    
    @api.constrains('session_start_time', 'session_end_time')
    def _check_times(self):
        """Ensure end time is after start time"""
        for record in self:
            if record.session_start_time and record.session_end_time and record.session_start_time >= record.session_end_time:
                raise ValidationError(_("Session end time must be later than start time"))
    
    @api.onchange('location')
    def _onchange_location(self):
        """Clear telehealth fields if office location selected"""
        if self.location != 'telehealth':
            self.telehealth_confirmation = False
            self.telehealth_appropriate = False
    
    @api.onchange('is_soap_format')
    def _onchange_soap_format(self):
        """Toggle between note formats"""
        if self.is_soap_format:
            # Transfer data to SOAP format if available
            if self.current_symptoms or self.functional_impairment_details:
                self.subjective = f"Symptoms: {self.current_symptoms}\nFunctional Impact: {self.functional_impairment_details}"
            if self.session_focus:
                self.assessment = self.session_focus
    
    def action_sign(self):
        """Sign the progress note"""
        return self.write({
            'state': 'signed',
            'provider_sign_date': fields.Datetime.now()
        })
    
    def action_lock(self):
        """Lock the progress note"""
        return self.write({'state': 'locked'})
    
    def action_set_to_draft(self):
        """Set back to draft"""
        return self.write({'state': 'draft'})
