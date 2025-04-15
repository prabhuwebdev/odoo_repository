from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Location(models.Model):
    _name = 'ehr_cdss.location'
    _description = 'Healthcare Location'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Location Name", required=True, tracking=True)
    code = fields.Char(string="Location Code", tracking=True)
    
    # Relationships
    organization_id = fields.Many2one('ehr_cdss.organization', string="Organization", required=True, tracking=True)
    parent_id = fields.Many2one('ehr_cdss.location', string="Parent Location")
    child_ids = fields.One2many('ehr_cdss.location', 'parent_id', string="Child Locations")
    
    # department_ids = fields.One2many('ehr_cdss.department', 'location_id', string="Departments")
    # room_ids = fields.One2many('ehr_cdss.room', 'location_id', string="Rooms")
    
    # Type
    location_type = fields.Selection([
        ('building', 'Building'),
        ('floor', 'Floor'),
        ('wing', 'Wing'),
        ('unit', 'Unit'),
        ('office', 'Office'),
        ('clinic', 'Clinic'),
        ('satellite', 'Satellite Location'),
        ('pharmacy', 'Pharmacy'),
        ('lab', 'Laboratory'),
        ('other', 'Other'),
    ], string="Location Type", required=True, tracking=True)
    
    specialty = fields.Char(string="Specialty")
    description = fields.Text(string="Description")
    
    # Address
    # address_id = fields.Many2one('ehr_cdss.address', string="Address")
    
    # Contact Information
    # contact_info_id = fields.Many2one('ehr_cdss.contact.info', string="Contact Information")
    phone = fields.Char(string="Phone")
    fax = fields.Char(string="Fax")
    email = fields.Char(string="Email")
    
    # Hours of Operation
    # operating_hours_ids = fields.One2many('ehr_cdss.operating.hours', 'location_id', string="Operating Hours")
    is_24_hours = fields.Boolean(string="Open 24 Hours")
    
    # Services
    service_ids = fields.Many2many('ehr_cdss.service', string="Services Available")
    accepts_new_patients = fields.Boolean(string="Accepting New Patients", default=True)
    telehealth_available = fields.Boolean(string="Telehealth Available", default=True)
    wheelchair_accessible = fields.Boolean(string="Wheelchair Accessible", default=True)
    has_parking = fields.Boolean(string="Has Parking")
    has_public_transport = fields.Boolean(string="Public Transport Access")
    
    # Capacity
    capacity = fields.Integer(string="Maximum Capacity")
    
    # Coordinates
    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")
    
    # Notes
    directions = fields.Text(string="Directions")
    notes = fields.Text(string="Notes")
    
    # Image
    image = fields.Binary(string="Location Image")
    
    # Status
    active = fields.Boolean(string="Active", default=True, tracking=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('under_construction', 'Under Construction'),
        ('temporarily_closed', 'Temporarily Closed'),
        ('renovating', 'Renovating'),
    ], string="Status", default='active', tracking=True)
    
    def action_activate(self):
        """Activate the location"""
        return self.write({'state': 'active', 'active': True})
    
    def action_deactivate(self):
        """Deactivate the location"""
        return self.write({'state': 'inactive', 'active': False})
    
    def action_under_construction(self):
        """Set as under construction"""
        return self.write({'state': 'under_construction'})
    
    def action_temporarily_close(self):
        """Mark as temporarily closed"""
        return self.write({'state': 'temporarily_closed'})
    
    def action_renovating(self):
        """Mark as renovating"""
        return self.write({'state': 'renovating'})
