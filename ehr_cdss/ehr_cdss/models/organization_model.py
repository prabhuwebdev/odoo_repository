from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Organization(models.Model):
    _name = 'ehr_cdss.organization'
    _description = 'Healthcare Organization'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Organization Name", required=True, tracking=True)
    code = fields.Char(string="Organization Code", tracking=True)
    
    # Type
    organization_type = fields.Selection([
        ('hospital', 'Hospital'),
        ('clinic', 'Clinic'),
        ('practice', 'Private Practice'),
        ('group_practice', 'Group Practice'),
        ('community_center', 'Community Health Center'),
        ('mental_health', 'Mental Health Center'),
        ('rehabilitation', 'Rehabilitation Center'),
        ('insurance', 'Insurance Company'),
        ('pharmacy', 'Pharmacy'),
        ('lab', 'Laboratory'),
        ('imaging', 'Imaging Center'),
        ('other', 'Other'),
    ], string="Organization Type", required=True, tracking=True)
    
    organization_subtype = fields.Char(string="Organization Subtype")
    specialty = fields.Char(string="Specialty")
    
    # Identification
    tax_id = fields.Char(string="Tax ID")
    npi = fields.Char(string="NPI Number")
    legal_name = fields.Char(string="Legal Name")
    website = fields.Char(string="Website")
    
    # Contact Information
    # contact_info_id = fields.Many2one('ehr_cdss.contact.info', string="Contact Information")
    phone = fields.Char(string="Phone")
    fax = fields.Char(string="Fax")
    email = fields.Char(string="Email")
    
    # Address
    # address_id = fields.Many2one('ehr_cdss.address', string="Primary Address")
    
    # Relationships
    parent_id = fields.Many2one('ehr_cdss.organization', string="Parent Organization")
    child_ids = fields.One2many('ehr_cdss.organization', 'parent_id', string="Child Organizations")
    
    # location_ids = fields.One2many('ehr_cdss.location', 'organization_id', string="Locations")
    # department_ids = fields.One2many('ehr_cdss.department', 'organization_id', string="Departments")
    provider_ids = fields.One2many('ehr_cdss.provider', 'organization_id', string="Providers")
    
    # Healthcare Network
    partner_organization_ids = fields.Many2many(
        'ehr_cdss.organization', 'organization_partner_rel',
        'organization_id', 'partner_id', string="Partner Organizations")
    
    # Administrative
    is_insurance_accepted = fields.Boolean(string="Accepts Insurance", default=True)
    # accepted_insurance_ids = fields.Many2many('ehr_cdss.insurance.plan', string="Accepted Insurance Plans")
    
    accreditation_ids = fields.One2many('ehr_cdss.organization.accreditation', 'organization_id', string="Accreditations")
    certification_ids = fields.One2many('ehr_cdss.organization.certification', 'organization_id', string="Certifications")
    
    # Operational
    # operating_hours_ids = fields.One2many('ehr_cdss.operating.hours', 'organization_id', string="Operating Hours")
    is_24_hours = fields.Boolean(string="Open 24 Hours")
    
    # Services
    service_ids = fields.Many2many('ehr_cdss.service', string="Services Offered")
    accepts_new_patients = fields.Boolean(string="Accepting New Patients", default=True)
    telehealth_available = fields.Boolean(string="Telehealth Available", default=True)
    emergency_services = fields.Boolean(string="Emergency Services Available")
    
    # Notes
    notes = fields.Text(string="Notes")
    
    # State
    active = fields.Boolean(string="Active", default=True, tracking=True)
    state = fields.Selection([('active', 'Active'),('inactive', 'Inactive'),('pending', 'Pending Verification'),('suspended', 'Suspended')], string="Status", default='active', tracking=True)
    
    # Display Image
    logo = fields.Binary(string="Logo")
    
    _sql_constraints = [
        ('npi_unique', 'UNIQUE(npi)', 'NPI Number must be unique!')
    ]
    
    def action_activate(self):
        """Activate the organization"""
        return self.write({'state': 'active', 'active': True})
    
    def action_deactivate(self):
        """Deactivate the organization"""
        return self.write({'state': 'inactive', 'active': False})
    
    def action_pending(self):
        """Set to pending verification"""
        return self.write({'state': 'pending'})
    
    def action_suspend(self):
        """Suspend the organization"""
        return self.write({'state': 'suspended', 'active': False})


class OrganizationAccreditation(models.Model):
    _name = 'ehr_cdss.organization.accreditation'
    _description = 'Organization Accreditation'
    
    organization_id = fields.Many2one('ehr_cdss.organization', string="Organization", required=True, ondelete='cascade')
    name = fields.Char(string="Accreditation Name", required=True)
    accrediting_body = fields.Char(string="Accrediting Body", required=True)
    accreditation_number = fields.Char(string="Accreditation Number")
    issue_date = fields.Date(string="Issue Date")
    expiry_date = fields.Date(string="Expiry Date")
    status = fields.Selection([('active', 'Active'),('pending', 'Pending'),('expired', 'Expired'),('revoked', 'Revoked')], string="Status", default='active')
    notes = fields.Text(string="Notes")
    document_id = fields.Many2one('ehr_cdss.document', string="Accreditation Document")


class OrganizationCertification(models.Model):
    _name = 'ehr_cdss.organization.certification'
    _description = 'Organization Certification'
    
    organization_id = fields.Many2one('ehr_cdss.organization', string="Organization", required=True, ondelete='cascade')
    name = fields.Char(string="Certification Name", required=True)
    certifying_body = fields.Char(string="Certifying Body", required=True)
    certification_number = fields.Char(string="Certification Number")
    issue_date = fields.Date(string="Issue Date")
    expiry_date = fields.Date(string="Expiry Date")
    status = fields.Selection([
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ], string="Status", default='active')
    notes = fields.Text(string="Notes")
    document_id = fields.Many2one('ehr_cdss.document', string="Certification Document")


class OperatingHours(models.Model):
    _name = 'ehr_cdss.operating.hours'
    _description = 'Operating Hours'
    _order = 'day_of_week,start_time'
    
    organization_id = fields.Many2one('ehr_cdss.organization', string="Organization", ondelete='cascade')
    location_id = fields.Many2one('ehr_cdss.location', string="Location", ondelete='cascade')
    department_id = fields.Many2one('ehr_cdss.department', string="Department", ondelete='cascade')
    
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string="Day of Week", required=True)
    
    start_time = fields.Float(string="Open Time", required=True)
    end_time = fields.Float(string="Close Time", required=True)
    is_closed = fields.Boolean(string="Closed")
    
    notes = fields.Text(string="Notes")
    
    @api.constrains('start_time', 'end_time')
    def _check_times(self):
        """Ensure end time is after start time"""
        for record in self:
            if not record.is_closed and record.start_time >= record.end_time:
                raise ValidationError(_("End time must be later than start time"))


class Service(models.Model):
    _name = 'ehr_cdss.service'
    _description = 'Healthcare Service'
    
    name = fields.Char(string="Service Name", required=True)
    code = fields.Char(string="Service Code")
    category = fields.Selection([
        ('preventive', 'Preventive Care'),
        ('diagnostic', 'Diagnostic'),
        ('treatment', 'Treatment'),
        ('surgical', 'Surgical'),
        ('emergency', 'Emergency'),
        ('rehabilitation', 'Rehabilitation'),
        ('mental_health', 'Mental Health'),
        ('specialty', 'Specialty Care'),
        ('support', 'Support Service'),
        ('other', 'Other'),
    ], string="Category", required=True)
    
    description = fields.Text(string="Description")
    duration = fields.Float(string="Typical Duration (minutes)")
    requires_referral = fields.Boolean(string="Requires Referral")
    requires_authorization = fields.Boolean(string="Requires Authorization")
    telehealth_eligible = fields.Boolean(string="Telehealth Eligible")
    
    # billing_code_ids = fields.Many2many('ehr_cdss.billing.code', string="Billing Codes")
    
    organization_ids = fields.Many2many('ehr_cdss.organization', string="Organizations Offering This Service")
    # department_ids = fields.Many2many('ehr_cdss.department', string="Departments Offering This Service")
    
    active = fields.Boolean(string="Active", default=True)
