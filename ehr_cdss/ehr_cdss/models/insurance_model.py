from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InsurancePlan(models.Model):
    _name = 'ehr_cdss.insurance.plan'
    _description = 'Insurance Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Plan Name", required=True, tracking=True)
    plan_id = fields.Char(string="Plan ID", tracking=True)
    
    # Insurance Company
    payer_id = fields.Many2one('ehr_cdss.insurance.payer', string="Insurance Payer", required=True, tracking=True)
    
    # Plan Classification
    plan_type = fields.Selection([
        ('commercial', 'Commercial'),
        ('medicare', 'Medicare'),
        ('medicaid', 'Medicaid'),
        ('medicare_advantage', 'Medicare Advantage'),
        ('tricare', 'TRICARE'),
        ('champva', 'CHAMPVA'),
        ('workers_comp', 'Workers Compensation'),
        ('self_pay', 'Self Pay'),
        ('other', 'Other'),
    ], string="Plan Type", required=True, tracking=True)
    
    # Plan Details
    plan_level = fields.Selection([
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('catastrophic', 'Catastrophic'),
        ('other', 'Other'),
    ], string="Plan Level")
    
    # Behavioral Health Coverage
    mental_health_coverage = fields.Boolean(string="Mental Health Coverage", default=True)
    substance_use_coverage = fields.Boolean(string="Substance Use Coverage", default=True)
    
    # Service Coverage
    # covered_service_ids = fields.Many2many('ehr_cdss.service.type', string="Covered Services")
    telehealth_coverage = fields.Boolean(string="Telehealth Coverage", default=True)
    
    # Provider Requirements
    network_type = fields.Selection([
        ('hmo', 'HMO'),
        ('ppo', 'PPO'),
        ('epo', 'EPO'),
        ('pos', 'POS'),
        ('indemnity', 'Indemnity'),
        ('other', 'Other'),
    ], string="Network Type")
    
    requires_referral = fields.Boolean(string="Requires Referral", default=False)
    requires_authorization = fields.Boolean(string="Requires Authorization", default=False)
    requires_pcp = fields.Boolean(string="Requires Primary Care Provider", default=False)
    
    # Contact Information
    # contact_info_id = fields.Many2one('ehr_cdss.contact.info', string="Contact Information")
    
    # Electronic Claims
    accepts_electronic_claims = fields.Boolean(string="Accepts Electronic Claims", default=True)
    electronic_payer_id = fields.Char(string="Electronic Payer ID")
    claims_clearinghouse = fields.Char(string="Claims Clearinghouse")
    
    # Patient Cost Sharing
    has_deductible = fields.Boolean(string="Has Deductible", default=True)
    typical_deductible = fields.Float(string="Typical Deductible")
    
    has_copay = fields.Boolean(string="Has Copay", default=True)
    typical_copay = fields.Float(string="Typical Copay")
    
    has_coinsurance = fields.Boolean(string="Has Coinsurance", default=True)
    typical_coinsurance_percentage = fields.Float(string="Typical Coinsurance Percentage")
    
    # Administrative
    verification_url = fields.Char(string="Verification URL")
    verification_phone = fields.Char(string="Verification Phone")
    
    billing_notes = fields.Text(string="Billing Notes")
    
    # Status
    active = fields.Boolean(string="Active", default=True, tracking=True)
    
    _sql_constraints = [
        ('name_payer_unique', 'UNIQUE(name, payer_id)', 'Plan name must be unique per payer!'),
    ]


class InsurancePayer(models.Model):
    _name = 'ehr_cdss.insurance.payer'
    _description = 'Insurance Payer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Payer Name", required=True, tracking=True)
    payer_id = fields.Char(string="Payer ID", tracking=True)
    
    # Payer Details
    payer_type = fields.Selection([
        ('commercial', 'Commercial'),
        ('government', 'Government'),
        ('third_party', 'Third Party Administrator'),
        ('self_insured', 'Self-Insured'),
        ('other', 'Other'),
    ], string="Payer Type", required=True)
    
    # Contact Information
    contact_info_id = fields.Many2one('ehr_cdss.contact.info', string="Contact Information")
    
    # Claims Information
    claims_address_id = fields.Many2one('ehr_cdss.address', string="Claims Address")
    claims_phone = fields.Char(string="Claims Phone")
    claims_fax = fields.Char(string="Claims Fax")
    
    # Electronic Claims
    accepts_electronic_claims = fields.Boolean(string="Accepts Electronic Claims", default=True)
    electronic_payer_id = fields.Char(string="Electronic Payer ID")
    claims_clearinghouse = fields.Char(string="Claims Clearinghouse")
    
    # Plans
    plan_ids = fields.One2many('ehr_cdss.insurance.plan', 'payer_id', string="Insurance Plans")
    
    # Administrative
    website = fields.Char(string="Website")
    provider_portal = fields.Char(string="Provider Portal")
    
    notes = fields.Text(string="Notes")
    
    # Status
    active = fields.Boolean(string="Active", default=True, tracking=True)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Payer name must be unique!'),
        ('payer_id_unique', 'UNIQUE(payer_id)', 'Payer ID must be unique!'),
    ]


class Insurance(models.Model):
    _name = 'ehr_cdss.insurance'
    _description = 'Patient Insurance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Insurance ID", readonly=True, copy=False, default=lambda self: _('New'))
    
    # Relationships
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient", required=True, tracking=True)
    plan_id = fields.Many2one('ehr_cdss.insurance.plan', string="Insurance Plan", required=True, tracking=True)
    payer_id = fields.Many2one('ehr_cdss.insurance.payer', related='plan_id.payer_id', string="Insurance Payer", store=True)
    
    # Identification
    member_id = fields.Char(string="Member ID", required=True, tracking=True)
    group_number = fields.Char(string="Group Number")
    policy_number = fields.Char(string="Policy Number")
    
    # Coverage
    coverage_type = fields.Selection([
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('tertiary', 'Tertiary'),
        ('quaternary', 'Quaternary'),
        ('other', 'Other'),
    ], string="Coverage Type", required=True, default='primary', tracking=True)
    
    is_self_pay = fields.Boolean(string="Self Pay",compute='_compute_is_self_pay', store=True)
    
    # Subscriber Information
    is_subscriber = fields.Boolean(string="Patient is Subscriber", default=True, tracking=True)
    
    # subscriber_id = fields.Many2one('ehr_cdss.contact', string="Subscriber")
    
    # Only used if patient is not subscriber
    subscriber_first_name = fields.Char(string="Subscriber First Name")
    subscriber_middle_name = fields.Char(string="Subscriber Middle Name")
    subscriber_last_name = fields.Char(string="Subscriber Last Name")
    
    subscriber_dob = fields.Date(string="Subscriber DOB")
    subscriber_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Subscriber Gender")
    
    # subscriber_address_id = fields.Many2one('ehr_cdss.address', string="Subscriber Address")
    subscriber_phone = fields.Char(string="Subscriber Phone")
    
    subscriber_relationship = fields.Selection([
        ('self', 'Self'),
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('other', 'Other'),
    ], string="Relationship to Subscriber", default='self')
    
    # Eligibility and Coverage
    effective_date = fields.Date(string="Effective Date", tracking=True)
    termination_date = fields.Date(string="Termination Date", tracking=True)
    
    eligibility_verified = fields.Boolean(string="Eligibility Verified", default=False)
    eligibility_verification_date = fields.Date(string="Verification Date")
    eligibility_notes = fields.Text(string="Eligibility Notes")
    
    # Benefits
    copay_amount = fields.Float(string="Copay Amount")
    coinsurance_percentage = fields.Float(string="Coinsurance Percentage")
    deductible_amount = fields.Float(string="Deductible Amount")
    deductible_met = fields.Float(string="Deductible Met")
    out_of_pocket_max = fields.Float(string="Out of Pocket Maximum")
    out_of_pocket_met = fields.Float(string="Out of Pocket Met")
    
    # Service Authorizations
    authorization_required = fields.Boolean(string="Authorization Required", default=False)
    authorization_ids = fields.One2many('ehr_cdss.insurance.authorization', 'insurance_id', string="Authorizations")
    
    # Card Information
    card_image_front = fields.Binary(string="Insurance Card Front")
    card_image_back = fields.Binary(string="Insurance Card Back")
    
    # Status
    active = fields.Boolean(string="Active", default=True, tracking=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending Verification'),
        ('termed', 'Termed'),
    ], string="Status", default='active', tracking=True)
    
    # Notes
    notes = fields.Text(string="Notes")
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Insurance ID must be unique!'),
        ('patient_plan_coverage_unique', 'UNIQUE(patient_id, plan_id, coverage_type)', 
         'This insurance plan and coverage type is already assigned to this patient!'),
    ]
    
    @api.model
    def create(self, vals):
        """Generate unique insurance ID"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('ehr_cdss.insurance') or _('New')
        return super(Insurance, self).create(vals)
    
    @api.onchange('is_subscriber')
    def _onchange_is_subscriber(self):
        """Clear subscriber info if patient is subscriber"""
        if self.is_subscriber:
            self.subscriber_first_name = False
            self.subscriber_middle_name = False
            self.subscriber_last_name = False
            self.subscriber_dob = False
            self.subscriber_gender = False
            # self.subscriber_address_id = False
            self.subscriber_phone = False
            self.subscriber_relationship = 'self'
    
    def action_verify_eligibility(self):
        """Mark insurance as verified"""
        return self.write({
            'eligibility_verified': True,
            'eligibility_verification_date': fields.Date.today(),
            'status': 'active'
        })
    
    def action_term(self):
        """Mark insurance as termed"""
        return self.write({
            'status': 'termed',
            'active': False,
            'termination_date': fields.Date.today()
        })
        
    
    @api.depends('plan_id.plan_type')
    def _compute_is_self_pay(self):
        for record in self:
            record.is_self_pay = record.plan_id.plan_type == 'self_pay'


class InsuranceAuthorization(models.Model):
    _name = 'ehr_cdss.insurance.authorization'
    _description = 'Insurance Authorization'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Authorization Number", required=True, tracking=True)
    
    # Relationships
    insurance_id = fields.Many2one('ehr_cdss.insurance', string="Insurance", required=True, ondelete='cascade')
    patient_id = fields.Many2one('ehr_cdss.patient.info', related='insurance_id.patient_id', string="Patient", store=True)
    
    # Service Information
    # service_ids = fields.Many2many('ehr_cdss.service.type', string="Authorized Services")
    # diagnosis_ids = fields.Many2many('ehr_cdss.diagnosis', string="Authorized Diagnoses")
    
    # Authorization Details
    authorized_visits = fields.Integer(string="Authorized Visits/Units")
    visits_used = fields.Integer(string="Visits/Units Used")
    visits_remaining = fields.Integer(string="Visits/Units Remaining", compute="_compute_visits_remaining", store=True)
    
    # Dates
    request_date = fields.Date(string="Request Date")
    effective_date = fields.Date(string="Effective Date", required=True)
    expiration_date = fields.Date(string="Expiration Date", required=True)
    
    # Contact
    auth_contact_name = fields.Char(string="Authorization Contact")
    auth_contact_phone = fields.Char(string="Contact Phone")
    auth_reference = fields.Char(string="Reference Number")
    
    # Notes
    notes = fields.Text(string="Notes")
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft', tracking=True)
    
    @api.depends('authorized_visits', 'visits_used')
    def _compute_visits_remaining(self):
        """Compute remaining visits"""
        for record in self:
            if record.authorized_visits is not None and record.visits_used is not None:
                record.visits_remaining = record.authorized_visits - record.visits_used
            else:
                record.visits_remaining = 0
    
    @api.constrains('effective_date', 'expiration_date')
    def _check_dates(self):
        """Check that expiration date is after effective date"""
        for record in self:
            if record.effective_date and record.expiration_date and record.effective_date > record.expiration_date:
                raise ValidationError(_("Expiration date must be after effective date"))
    
    def action_submit(self):
        """Submit the authorization request"""
        return self.write({'state': 'pending'})
    
    def action_approve(self):
        """Mark authorization as approved"""
        return self.write({'state': 'approved'})
    
    def action_deny(self):
        """Mark authorization as denied"""
        return self.write({'state': 'denied'})
    
    def action_cancel(self):
        """Cancel the authorization"""
        return self.write({'state': 'cancelled'})
    
    def action_reset_to_draft(self):
        """Reset to draft status"""
        return self.write({'state': 'draft'})
