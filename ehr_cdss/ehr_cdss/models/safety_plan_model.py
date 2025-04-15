from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random
import string

class SafetyPlan(models.Model):
    _name = 'ehr_cdss.safety.plan'
    _description = 'Safety Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Plan ID", readonly=True, default=lambda self: self._generate_patient_id())
    
    # Relationships
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient", required=True, tracking=True)
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", required=True, tracking=True)
    medical_record_id = fields.Many2one('ehr_cdss.medical.record', string="Medical Record")
    risk_assessment_id = fields.Many2one('ehr_cdss.risk.assessment', string="Related Risk Assessment")
    
    # Plan Creation
    create_date = fields.Datetime(string="Date Created", readonly=True)
    last_update_date = fields.Datetime(string="Last Updated", readonly=True, tracking=True)
    is_active = fields.Boolean(string="Is Active Plan", default=True, tracking=True)
    
    # Step 1: Warning Signs
    warning_signs = fields.Text(string="Warning Signs", required=True,
                              help="Thoughts, images, mood, situation that a crisis may be developing")
    
    # Step 2: Internal Coping Strategies
    internal_coping_strategies = fields.Text(string="Internal Coping Strategies", required=True,
                                          help="Things I can do to take my mind off my problems without contacting another person")
    
    # Step 3: Social Contacts Who May Distract
    social_contacts = fields.Text(string="People and Social Settings for Distraction", required=True,
                                help="People and places that provide distraction")
    
    # Step 4: People Who Can Help
    help_contacts = fields.Text(string="People Who Can Help", required=True,
                               help="People whom I can ask for help during a crisis")
    help_contacts_ids = fields.One2many('ehr_cdss.safety.plan.contact', 'safety_plan_id', 
                                      string="Help Contacts", copy=True)
    
    # Step 5: Professionals or Agencies
    professional_contacts = fields.Text(string="Professionals or Agencies", required=True,
                                     help="Professionals or agencies I can contact during a crisis")
    professional_contacts_ids = fields.One2many('ehr_cdss.safety.plan.professional', 'safety_plan_id', 
                                             string="Professional Contacts", copy=True)
    
    # Step 6: Making the Environment Safe
    environment_safety = fields.Text(string="Making the Environment Safe", required=True,
                                  help="Things I can do to remove means of harm")
    
    # Step 7: Reasons for Living
    reasons_for_living = fields.Text(string="Reasons for Living", required=True,
                                  help="The one thing that is most important to me and worth living for")
    
    # Additional Information
    additional_resources = fields.Text(string="Additional Resources",
                                    help="Additional crisis resources, phone apps, etc.")
    
    triggering_events = fields.Text(string="Triggering Events",
                                 help="Specific events or situations that might trigger a crisis")
    
    early_warning_behaviors = fields.Text(string="Early Warning Behaviors",
                                       help="Behaviors that indicate escalating risk")
    
    # Document Information
    document_id = fields.Many2one('ehr_cdss.document', string="Related Document")
    
    # Signatures
    patient_signature = fields.Binary(string="Patient Signature")
    patient_sign_date = fields.Datetime(string="Patient Signature Date")
    provider_signature = fields.Binary(string="Provider Signature")
    provider_sign_date = fields.Datetime(string="Provider Signature Date")
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ], string="Status", default='draft', tracking=True)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Plan ID must be unique!')
    ]
    
    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'Safety Plan -' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def write(self, vals):
        """Update last_update_date when changed"""
        vals['last_update_date'] = fields.Datetime.now()
        return super(SafetyPlan, self).write(vals)
    
    def action_activate(self):
        """Activate the safety plan"""
        # Deactivate any other active safety plans for this patient
        active_plans = self.search([
            ('patient_id', '=', self.patient_id.id),
            ('id', '!=', self.id),
            ('is_active', '=', True)
        ])
        active_plans.write({'is_active': False, 'state': 'archived'})
        
        return self.write({
            'is_active': True,
            'state': 'active'
        })
    
    def action_archive(self):
        """Archive the safety plan"""
        return self.write({
            'is_active': False,
            'state': 'archived'
        })
    
    def action_set_to_draft(self):
        """Set back to draft"""
        return self.write({'state': 'draft'})
    
    def action_patient_sign(self):
        """Record patient signature"""
        return self.write({
            'patient_sign_date': fields.Datetime.now()
        })
    
    def action_provider_sign(self):
        """Record provider signature"""
        return self.write({
            'provider_sign_date': fields.Datetime.now()
        })
    
    def action_print_safety_plan(self):
        """Print the safety plan"""
        return self.env.ref('ehr_cdss.action_report_safety_plan').report_action(self)


class SafetyPlanContact(models.Model):
    _name = 'ehr_cdss.safety.plan.contact'
    _description = 'Safety Plan Contact'
    _order = 'sequence'
    
    safety_plan_id = fields.Many2one('ehr_cdss.safety.plan', string="Safety Plan", required=True, ondelete='cascade')
    sequence = fields.Integer(string="Sequence", default=10)
    
    name = fields.Char(string="Name", required=True)
    relationship = fields.Char(string="Relationship")
    phone = fields.Char(string="Phone Number")
    alternate_phone = fields.Char(string="Alternate Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    notes = fields.Text(string="Notes")
    
    is_emergency_contact = fields.Boolean(string="Emergency Contact")


class SafetyPlanProfessional(models.Model):
    _name = 'ehr_cdss.safety.plan.professional'
    _description = 'Safety Plan Professional Contact'
    _order = 'sequence'
    
    safety_plan_id = fields.Many2one('ehr_cdss.safety.plan', string="Safety Plan", required=True, ondelete='cascade')
    sequence = fields.Integer(string="Sequence", default=10)
    
    name = fields.Char(string="Name/Agency", required=True)
    role = fields.Char(string="Role/Service")
    phone = fields.Char(string="Phone Number")
    alternate_phone = fields.Char(string="Alternate Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    hours = fields.Char(string="Hours of Operation")
    notes = fields.Text(string="Notes")
    
    is_emergency_service = fields.Boolean(string="Emergency Service")
