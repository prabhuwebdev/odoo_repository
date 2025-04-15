from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random
import string

class MedicalRecord(models.Model):
    _name = 'ehr_cdss.medical.record'
    _description = 'Medical Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'
    
    name = fields.Char(string="Record ID", readonly=True, default=lambda self: self._generate_patient_id())
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient", required=True, tracking=True)
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", required=True, tracking=True)
    date = fields.Datetime(string="Record Date", default=fields.Datetime.now, tracking=True)
    
    # General Record Information
    record_type = fields.Selection([
        ('initial_assessment', 'Initial Assessment'),
        ('progress_note', 'Progress Note'),
        ('soap_note', 'SOAP Note'),
        ('treatment_plan', 'Treatment Plan'),
        ('safety_plan', 'Safety Plan'),
        ('discharge_note', 'Discharge Note'),
        ('referral', 'Referral'),
        ('clinical_review_update', 'Clinical Review Update'),
        ('other', 'Other'),
    ], string="Record Type", required=True, tracking=True)
    service_provided = fields.Selection([
        ('individual_therapy', 'Individual Therapy'),
        ('couples_therapy', 'Couples Therapy'),
        ('family_therapy', 'Family Therapy'),
        ('group_therapy', 'Group Therapy'),
        ('medication_management', 'Medication Management'),
        ('assessment', 'Assessment'),
        ('crisis_intervention', 'Crisis Intervention'),
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
    
    # Assessment Elements
    # assessment_id = fields.Many2one('ehr_cdss.assessment', string="Assessment")
    
    # Progress/SOAP Note Elements
    # progress_note_id = fields.Many2one('ehr_cdss.progress.note', string="Progress Note")
    
    # Treatment Plan Elements
    # treatment_plan_id = fields.Many2one('ehr_cdss.treatment.plan', string="Treatment Plan")
    
    # Safety Plan Elements
    # safety_plan_id = fields.Many2one('ehr_cdss.safety.plan', string="Safety Plan")
    
    # Discharge Elements
    discharge_date = fields.Date(string="Discharge Date")
    discharge_reason = fields.Selection([
        ('goals_achieved', 'Treatment goals were achieved'),
        ('medical_necessity', 'Medical necessity was no longer met'),
        ('provider_rematch', 'Provider requested rematch'),
        ('higher_care', 'Client was referred to a higher level of care'),
        ('client_rematch', 'Client requested a rematch'),
        ('client_no_return', 'Client did not return to treatment'),
        ('client_end', 'Client chose to end treatment'),
        ('telehealth_inappropriate', 'Client was not appropriate for telehealth services'),
        ('client_deceased', 'Client passed away'),
        ('other', 'Other'),
    ], string="Reason for Discharge")
    goals_achievement = fields.Selection([
        ('fully', 'Fully achieved'),
        ('partially', 'Partially achieved'),
        ('no', 'No'),
        ('unknown', 'Unknown'),
    ], string="Treatment Goals Achieved")
    
    # Common Fields
    # diagnosis_ids = fields.Many2many('ehr_cdss.diagnosis', string="Diagnoses")
    # document_ids = fields.One2many('ehr_cdss.document', 'medical_record_id', string="Related Documents")
    notes = fields.Text(string="Additional Notes")
    
    # Session Timing
    session_start_time = fields.Datetime(string="Session Start Time")
    session_end_time = fields.Datetime(string="Session End Time")
    session_duration = fields.Float(string="Session Duration (minutes)", compute="_compute_session_duration", store=True)
    
    # Measures and Assessments
    baseline_measures_completed = fields.Boolean(string="Client Completed Baseline Measures")
    measures_reviewed = fields.Boolean(string="Measures Reviewed with Client")
    risk_factors_present = fields.Boolean(string="Risk Factors Present")
    
    # Billing Info
    # service_code = fields.Many2one('ehr_cdss.billing.code', string="Service Code")
    insurance_id = fields.Many2one('ehr_cdss.insurance', string="Insurance Used")
    
    # Signatures
    provider_signature = fields.Binary(string="Provider Signature")
    provider_sign_date = fields.Datetime(string="Provider Signature Date")
    patient_signature = fields.Binary(string="Patient Signature")
    patient_sign_date = fields.Datetime(string="Patient Signature Date")
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('signed', 'Signed'),
        ('locked', 'Locked'),
        ('amended', 'Amended'),
    ], string="Status", default='draft', tracking=True)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Record ID must be unique!')
    ]
    
    @api.model
    def create(self, vals):
        """Generate a unique record ID"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('ehr_cdss.medical.record') or _('New')
        return super(MedicalRecord, self).create(vals)
    
    @api.depends('session_start_time', 'session_end_time')
    def _compute_session_duration(self):
        """Compute session duration in minutes"""
        for record in self:
            if record.session_start_time and record.session_end_time:
                delta = record.session_end_time - record.session_start_time
                record.session_duration = delta.total_seconds() / 60
            else:
                record.session_duration = 0
    
    def action_sign(self):
        """Sign the medical record"""
        return self.write({
            'state': 'signed',
            'provider_sign_date': fields.Datetime.now(),
        })
    
    def action_lock(self):
        """Lock the medical record"""
        return self.write({'state': 'locked'})
    
    def action_amend(self):
        """Amend the medical record"""
        return self.write({'state': 'amended'})


class ClinicalReviewUpdate(models.Model):
    _name = 'ehr_cdss.clinical.review.update'
    _description = 'Clinical Review Update'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Review ID", readonly=True, copy=False, default=lambda self: _('New'))
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient", required=True, tracking=True)
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", required=True, tracking=True)
    date = fields.Date(string="Date", default=fields.Date.today, tracking=True)
    
    # CCR Specific Fields
    ccr_email_date = fields.Date(string="CCR Email Date", required=True)
    treatment_plan_update_date = fields.Date(string="Last Treatment Plan Update Date")
    symptom_interference = fields.Text(string="How Symptoms Interfere with Life", required=True)
    client_accomplishments = fields.Text(string="Client Treatment Plan Accomplishments", required=True)
    therapy_continuation_benefit = fields.Text(string="How Continued Therapy Will Help", required=True)
    
    # Clinical Rationale
    risk_of_harm = fields.Boolean(string="Client at Risk of Harm")
    mental_health_crisis = fields.Boolean(string="Client Experiencing Mental Health Crisis")
    goals_in_progress = fields.Boolean(string="Treatment Goals Not Yet Met but on Track")
    decompensation_risk = fields.Boolean(string="Risk of Decompensation Without Treatment")
    symptom_severity = fields.Boolean(string="Symptom Severity Requires Ongoing Treatment")
    outcome_survey_need = fields.Boolean(string="Outcome Survey Indicates Need for Treatment")
    
    # Record Integration
    medical_record_id = fields.Many2one('ehr_cdss.medical.record', string="Associated Medical Record")
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ], string="Status", default='draft', tracking=True)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Review ID must be unique!')
    ]
    
    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'Medical Record-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def action_submit(self):
        """Submit the clinical review update"""
        return self.write({'state': 'submitted'})
    
    def action_approve(self):
        """Approve the clinical review update"""
        return self.write({'state': 'approved'})
    
    def action_deny(self):
        """Deny the clinical review update"""
        return self.write({'state': 'denied'})
