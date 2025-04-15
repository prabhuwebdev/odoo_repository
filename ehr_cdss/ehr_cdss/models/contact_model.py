from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Contact(models.Model):
    _name = 'ehr_cdss.contact'
    _description = 'Contact Person'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Contact Name", required=True, tracking=True)
    
    # Basic Information
    first_name = fields.Char(string="First Name", required=True)
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name", required=True)
    suffix = fields.Char(string="Suffix")
    
    # Relationship
    relationship = fields.Selection([
        ('spouse', 'Spouse/Partner'),
        ('parent', 'Parent'),
        ('child', 'Child'),
        ('sibling', 'Sibling'),
        ('other_relative', 'Other Relative'),
        ('friend', 'Friend'),
        ('caregiver', 'Caregiver'),
        ('guardian', 'Legal Guardian'),
        ('healthcare_proxy', 'Healthcare Proxy'),
        ('power_of_attorney', 'Power of Attorney'),
        ('emergency', 'Emergency Contact'),
        ('other', 'Other'),
    ], string="Relationship to Patient", required=True, tracking=True)
    
    relationship_other = fields.Char(string="Other Relationship")
    
    # Contact Information
    contact_info_id = fields.Many2one('ehr_cdss.contact.info', string="Contact Information")
    
    # Core Contact Fields (for quick access)
    phone = fields.Char(string="Phone", tracking=True)
    email = fields.Char(string="Email", tracking=True)
    
    # Address
    address_id = fields.Many2one('ehr_cdss.address', string="Address")
    
    # Patient Relationship
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient", tracking=True)
    
    # Roles
    is_emergency_contact = fields.Boolean(string="Emergency Contact", default=False, tracking=True)
    is_guardian = fields.Boolean(string="Legal Guardian", default=False, tracking=True)
    is_healthcare_proxy = fields.Boolean(string="Healthcare Proxy", default=False, tracking=True)
    is_power_of_attorney = fields.Boolean(string="Power of Attorney", default=False, tracking=True)
    is_caregiver = fields.Boolean(string="Caregiver", default=False, tracking=True)
    
    # Permissions
    allowed_to_discuss = fields.Boolean(string="Allowed to Discuss Care", default=False, tracking=True)
    allowed_to_pickup = fields.Boolean(string="Allowed for Pickup", default=False, tracking=True)
    
    # Documentation
    # documentation_ids = fields.Many2many('ehr_cdss.document', string="Related Documentation")
    
    # Notes
    notes = fields.Text(string="Notes")
    
    # Status
    active = fields.Boolean(string="Active", default=True, tracking=True)
    
    @api.depends('first_name', 'middle_name', 'last_name', 'suffix')
    def _compute_name(self):
        """Compute the full name based on name parts"""
        for record in self:
            name_parts = [
                part for part in [
                    record.first_name,
                    record.middle_name,
                    record.last_name,
                    record.suffix
                ] if part
            ]
            record.name = " ".join(name_parts)
    
    @api.onchange('relationship')
    def _onchange_relationship(self):
        """Update role flags based on relationship selection"""
        if self.relationship == 'guardian':
            self.is_guardian = True
        elif self.relationship == 'healthcare_proxy':
            self.is_healthcare_proxy = True
        elif self.relationship == 'power_of_attorney':
            self.is_power_of_attorney = True
        elif self.relationship == 'caregiver':
            self.is_caregiver = True
        elif self.relationship == 'emergency':
            self.is_emergency_contact = True
    
    @api.onchange('is_guardian', 'is_healthcare_proxy', 'is_power_of_attorney')
    def _onchange_roles(self):
        """Auto-set allowed to discuss when important roles are checked"""
        if self.is_guardian or self.is_healthcare_proxy or self.is_power_of_attorney:
            self.allowed_to_discuss = True


class SafetyPlanContact(models.Model):
    _name = 'ehr_cdss.safety.plan.contact'
    _inherit = 'ehr_cdss.contact'
    _description = 'Safety Plan Contact'
    
    safety_plan_id = fields.Many2one('ehr_cdss.safety.plan', string="Safety Plan", required=True, ondelete='cascade')
    
    # Safety Plan Specific
    availability = fields.Selection([
        ('24_7', '24/7'),
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
        ('evenings', 'Evenings'),
        ('daytime', 'Daytime'),
        ('limited', 'Limited Availability'),
    ], string="Availability")
    
    availability_notes = fields.Text(string="Availability Notes")
    
    preferred_contact_method = fields.Selection([
        ('call', 'Phone Call'),
        ('text', 'Text Message'),
        ('both', 'Both Call and Text'),
        ('email', 'Email'),
        ('in_person', 'In Person'),
    ], string="Preferred Contact Method", default='call')
    
    distraction_activities = fields.Text(string="Distraction Activities")
    support_type = fields.Selection([
        ('emotional', 'Emotional Support'),
        ('practical', 'Practical Support'),
        ('crisis', 'Crisis Intervention'),
        ('distraction', 'Distraction'),
        ('multiple', 'Multiple Roles'),
    ], string="Type of Support")
