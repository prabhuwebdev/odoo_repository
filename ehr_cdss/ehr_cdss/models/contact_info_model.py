from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ContactInfo(models.Model):
    _name = 'ehr_cdss.contact.info'
    _description = 'Contact Information'
    
    name = fields.Char(string="Contact Name", compute="_compute_name", store=True)
    
    # Phone Numbers
    phone = fields.Char(string="Primary Phone")
    phone_type = fields.Selection([
        ('mobile', 'Mobile'),
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ], string="Phone Type", default='mobile')
    phone_extension = fields.Char(string="Extension")
    
    alternate_phone = fields.Char(string="Alternate Phone")
    alternate_phone_type = fields.Selection([
        ('mobile', 'Mobile'),
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ], string="Alternate Phone Type")
    alternate_phone_extension = fields.Char(string="Alternate Extension")
    
    fax = fields.Char(string="Fax")
    
    # Email Addresses
    email = fields.Char(string="Primary Email")
    email_type = fields.Selection([
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('other', 'Other'),
    ], string="Email Type", default='personal')
    
    alternate_email = fields.Char(string="Alternate Email")
    alternate_email_type = fields.Selection([
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('other', 'Other'),
    ], string="Alternate Email Type")
    
    # Web Presence
    website = fields.Char(string="Website")
    social_media = fields.Char(string="Social Media")
    
    # Communication Preferences
    preferred_contact_method = fields.Selection([
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('mail', 'Mail'),
        ('portal', 'Patient Portal'),
        ('other', 'Other'),
    ], string="Preferred Contact Method", default='phone')
    
    preferred_language_id = fields.Many2one('res.lang', string="Preferred Language")
    needs_interpreter = fields.Boolean(string="Needs Interpreter")
    has_hearing_impairment = fields.Boolean(string="Has Hearing Impairment")
    has_vision_impairment = fields.Boolean(string="Has Vision Impairment")
    
    # Communication Time Preferences
    preferred_time = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('anytime', 'Anytime'),
    ], string="Preferred Contact Time", default='anytime')
    
    # Contact Restrictions
    do_not_call = fields.Boolean(string="Do Not Call")
    do_not_email = fields.Boolean(string="Do Not Email")
    do_not_text = fields.Boolean(string="Do Not Text")
    do_not_leave_message = fields.Boolean(string="Do Not Leave Message")
    
    # Related Addresses
    address_ids = fields.One2many('ehr_cdss.contact.address.rel', 'contact_info_id', string="Addresses")
    primary_address_id = fields.Many2one('ehr_cdss.address', string="Primary Address")
    
    # Relations
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient")
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider")
    organization_id = fields.Many2one('ehr_cdss.organization', string="Organization")
    location_id = fields.Many2one('ehr_cdss.location', string="Location")
    # department_id = fields.Many2one('ehr_cdss.department', string="Department")
    contact_id = fields.Many2one('ehr_cdss.contact', string="Contact")
    
    # Notes
    notes = fields.Text(string="Notes")
    
    # @api.depends('patient_id', 'provider_id', 'organization_id', 'location_id', 'department_id', 'contact_id', 'phone')
    @api.depends('patient_id', 'provider_id', 'organization_id', 'location_id', 'contact_id', 'phone')
    def _compute_name(self):
        """Compute a descriptive name for the contact info"""
        for record in self:
            if record.patient_id:
                record.name = f"Contact Info for {record.patient_id.name}"
            elif record.provider_id:
                record.name = f"Contact Info for {record.provider_id.name}"
            elif record.organization_id:
                record.name = f"Contact Info for {record.organization_id.name}"
            elif record.location_id:
                record.name = f"Contact Info for {record.location_id.name}"
            # elif record.department_id:
            #     record.name = f"Contact Info for {record.department_id.name}"
            elif record.contact_id:
                record.name = f"Contact Info for {record.contact_id.name}"
            else:
                record.name = f"Contact Info ({record.phone or 'No Phone'})"


class ContactAddressRel(models.Model):
    _name = 'ehr_cdss.contact.address.rel'
    _description = 'Contact-Address Relationship'
    
    contact_info_id = fields.Many2one('ehr_cdss.contact.info', string="Contact Info", required=True, ondelete='cascade')
    address_id = fields.Many2one('ehr_cdss.address', string="Address", required=True, ondelete='cascade')
    
    address_type = fields.Selection([
        ('home', 'Home'),
        ('work', 'Work'),
        ('mailing', 'Mailing'),
        ('billing', 'Billing'),
        ('emergency', 'Emergency'),
        ('other', 'Other'),
    ], string="Address Type", required=True, default='home')
    
    is_primary = fields.Boolean(string="Primary Address")
    
    notes = fields.Text(string="Notes")
    
    @api.constrains('is_primary')
    def _check_primary_address(self):
        """Ensure only one primary address per contact"""
        for record in self:
            if record.is_primary:
                other_primary = self.search([
                    ('contact_info_id', '=', record.contact_info_id.id),
                    ('is_primary', '=', True),
                    ('id', '!=', record.id)
                ])
                if other_primary:
                    other_primary.write({'is_primary': False})
                    
                # Update the primary address in contact_info
                record.contact_info_id.primary_address_id = record.address_id.id
