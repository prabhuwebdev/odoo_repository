from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BillingCode(models.Model):
    _name = 'ehr_cdss.billing.code'
    _description = 'Billing Code'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Code Name", compute="_compute_name", store=True)
    code = fields.Char(string="Code", required=True, tracking=True)
    
    # Code Classification
    code_type = fields.Selection([
        ('cpt', 'CPT'),
        ('hcpcs', 'HCPCS'),
        ('icd10', 'ICD-10'),
        ('icd11', 'ICD-11'),
        ('dsm5', 'DSM-5'),
        ('revenue', 'Revenue Code'),
        ('custom', 'Custom'),
        ('other', 'Other'),
    ], string="Code Type", required=True, tracking=True)
    
    # Code Category for CPT/HCPCS
    category = fields.Selection([
        ('e_m', 'Evaluation & Management'),
        ('psychiatric', 'Psychiatric/Psychological'),
        ('therapy', 'Therapy/Counseling'),
        ('assessment', 'Assessment/Testing'),
        ('medical', 'Medical/Procedure'),
        ('group', 'Group Services'),
        ('telehealth', 'Telehealth'),
        ('other', 'Other'),
    ], string="Category")
    
    # Descriptions
    short_description = fields.Char(string="Short Description", required=True)
    description = fields.Text(string="Description")
    
    # Billing Information
    unit_type = fields.Selection([
        ('time', 'Time-based'),
        ('service', 'Service-based'),
        ('visit', 'Visit-based'),
        ('day', 'Day-based'),
        ('other', 'Other'),
    ], string="Unit Type", default='time')
    
    default_units = fields.Float(string="Default Units", default=1.0)
    max_units_per_day = fields.Float(string="Maximum Units Per Day")
    
    time_based = fields.Boolean(string="Time-Based Code")
    min_time = fields.Integer(string="Minimum Time (minutes)")
    max_time = fields.Integer(string="Maximum Time (minutes)")
    
    is_add_on = fields.Boolean(string="Add-on Code", 
                              help="Code that can only be billed with a primary code")
    parent_code_ids = fields.Many2many('ehr_cdss.billing.code', 'billing_code_parent_rel',
                                     'code_id', 'parent_id', string="Primary Codes",
                                     help="Codes this add-on can be billed with")
    
    # Rate Information
    default_rate = fields.Float(string="Default Rate")
    insurance_specific_rates = fields.Boolean(string="Insurance-Specific Rates")
    rate_ids = fields.One2many('ehr_cdss.billing.code.rate', 'billing_code_id', string="Insurance Rates")
    
    # Modifiers
    allowed_modifier_ids = fields.Many2many('ehr_cdss.billing.modifier', string="Allowed Modifiers")
    
    # Telehealth
    telehealth_eligible = fields.Boolean(string="Telehealth Eligible")
    telehealth_modifier_required = fields.Boolean(string="Telehealth Modifier Required")
    telehealth_place_of_service = fields.Char(string="Telehealth Place of Service")
    
    # Documentation Requirements
    required_documentation = fields.Text(string="Required Documentation")
    
    # Provider Restrictions
    # allowed_provider_types = fields.Many2many('ehr_cdss.provider.type', string="Allowed Provider Types")
    credential_requirements = fields.Text(string="Credential Requirements")
    
    # Diagnosis Requirements
    requires_diagnosis = fields.Boolean(string="Requires Diagnosis", default=True)
    # allowed_diagnosis_codes = fields.Many2many('ehr_cdss.diagnosis', string="Allowed Diagnosis Codes")
    
    # Scheduling
    default_duration = fields.Float(string="Default Appointment Duration (minutes)")
    
    # Usage
    # service_ids = fields.Many2many('ehr_cdss.service.type', string="Associated Services")
    applicable_notes = fields.Text(string="Applicable Notes")
    
    # Effective Dates
    effective_date = fields.Date(string="Effective Date")
    end_date = fields.Date(string="End Date")
    
    # Status
    active = fields.Boolean(string="Active", default=True, tracking=True)
    
    _sql_constraints = [
        ('code_type_unique', 'UNIQUE(code, code_type)', 'Billing code must be unique per code type!'),
    ]
    
    @api.depends('code', 'short_description')
    def _compute_name(self):
        """Compute a readable name for the billing code"""
        for record in self:
            if record.code and record.short_description:
                record.name = f"{record.code} - {record.short_description}"
            elif record.code:
                record.name = record.code
            else:
                record.name = record.short_description or "New Billing Code"
    
    @api.constrains('min_time', 'max_time')
    def _check_time_range(self):
        """Check that min time is less than max time for time-based codes"""
        for record in self:
            if record.time_based and record.min_time and record.max_time and record.min_time >= record.max_time:
                raise ValidationError(_("Minimum time must be less than maximum time for time-based codes"))


class BillingCodeRate(models.Model):
    _name = 'ehr_cdss.billing.code.rate'
    _description = 'Billing Code Rate'
    
    billing_code_id = fields.Many2one('ehr_cdss.billing.code', string="Billing Code", required=True, ondelete='cascade')
    insurance_plan_id = fields.Many2one('ehr_cdss.insurance.plan', string="Insurance Plan", required=True)
    
    rate = fields.Float(string="Rate", required=True)
    negotiated_rate = fields.Boolean(string="Negotiated Rate")
    
    effective_date = fields.Date(string="Effective Date")
    end_date = fields.Date(string="End Date")
    
    notes = fields.Text(string="Notes")
    
    _sql_constraints = [
        ('billing_code_insurance_unique', 'UNIQUE(billing_code_id, insurance_plan_id)', 
         'Only one rate per insurance plan is allowed!'),
    ]


class BillingModifier(models.Model):
    _name = 'ehr_cdss.billing.modifier'
    _description = 'Billing Modifier'
    
    name = fields.Char(string="Modifier Name", compute="_compute_name", store=True)
    code = fields.Char(string="Modifier Code", required=True)
    
    description = fields.Text(string="Description", required=True)
    
    # Effect on billing
    payment_impact = fields.Selection([
        ('increase', 'Increases Payment'),
        ('decrease', 'Decreases Payment'),
        ('none', 'No Payment Impact'),
        ('variable', 'Variable Impact'),
    ], string="Payment Impact", default='none')
    
    payment_percentage = fields.Float(string="Payment Adjustment Percentage")
    
    # Restrictions
    restricted_to_codes = fields.Boolean(string="Restricted to Specific Codes")
    applicable_code_ids = fields.Many2many('ehr_cdss.billing.code', string="Applicable Codes")
    
    # Usage
    usage_notes = fields.Text(string="Usage Notes")
    documentation_requirements = fields.Text(string="Documentation Requirements")
    
    # Status
    active = fields.Boolean(string="Active", default=True)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Modifier code must be unique!'),
    ]
    
    @api.depends('code', 'description')
    def _compute_name(self):
        """Compute a readable name for the modifier"""
        for record in self:
            if record.code and record.description:
                record.name = f"{record.code} - {record.description}"
            elif record.code:
                record.name = record.code
            else:
                record.name = record.description or "New Modifier"
