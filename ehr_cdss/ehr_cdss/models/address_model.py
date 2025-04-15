from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Address(models.Model):
    _name = 'ehr_cdss.address'
    _description = 'Address'
    
    name = fields.Char(string="Address Name", compute="_compute_name", store=True)
    
    # Street Address
    street = fields.Char(string="Street", required=True)
    street2 = fields.Char(string="Street 2")
    city = fields.Char(string="City", required=True)
    state_id = fields.Many2one('res.country.state', string="State", required=True)
    zip = fields.Char(string="ZIP/Postal Code", required=True)
    country_id = fields.Many2one('res.country', string="Country", required=True, 
                                default=lambda self: self.env.ref('base.main_company').country_id.id)
    
    # Additional Address Information
    county = fields.Char(string="County")
    district = fields.Char(string="District")
    apartment = fields.Char(string="Apartment/Unit Number")
    building = fields.Char(string="Building")
    floor = fields.Char(string="Floor")
    
    # Geographic Coordinates
    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")
    
    # Validation and Status
    is_valid = fields.Boolean(string="Address Validated", default=False)
    validation_date = fields.Date(string="Validation Date")
    validation_method = fields.Selection([
        ('manual', 'Manual Verification'),
        ('usps', 'USPS Verification'),
        ('ups', 'UPS Verification'),
        ('fedex', 'FedEx Verification'),
        ('google', 'Google Maps Verification'),
        ('other', 'Other Verification'),
    ], string="Validation Method")
    
    # Address Types and Relationships
    address_type = fields.Selection([
        ('residential', 'Residential'),
        ('business', 'Business'),
        ('institutional', 'Institutional'),
        ('rural', 'Rural'),
        ('pobox', 'PO Box'),
        ('military', 'Military'),
        ('other', 'Other'),
    ], string="Address Type", default='residential')
    
    # Relationships (inverse fields will be defined in the respective models)
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient")
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider")
    organization_id = fields.Many2one('ehr_cdss.organization', string="Organization")
    location_id = fields.Many2one('ehr_cdss.location', string="Location")
    
    # Contact Information Relationships
    # contact_info_ids = fields.One2many('ehr_cdss.contact.address.rel', 'address_id', string="Contact Info")
    
    # Notes
    notes = fields.Text(string="Notes")
    
    # Active Status
    active = fields.Boolean(string="Active", default=True)
    
    _sql_constraints = [
        ('unique_patient_address', 'unique(patient_id, street, city, state_id, zip)', 
         'This address already exists for this patient!')
    ]
    
    @api.depends('street', 'city', 'state_id', 'zip')
    def _compute_name(self):
        """Compute a readable name for the address"""
        for record in self:
            if record.street and record.city and record.state_id:
                record.name = f"{record.street}, {record.city}, {record.state_id.code} {record.zip}"
            else:
                record.name = "New Address"
    
    def action_validate_address(self):
        """Mark address as validated"""
        return self.write({'is_valid': True, 'validation_date': fields.Date.today(), 'validation_method': 'manual'})
    
    def action_invalidate_address(self):
        """Mark address as not validated"""
        return self.write({'is_valid': False, 'validation_date': False, 'validation_method': False})
    
    def action_geocode(self):
        """Geocode the address to get lat/long (placeholder for integration)"""
        # This would typically connect to a geocoding service like Google Maps
        self.ensure_one()
        return True