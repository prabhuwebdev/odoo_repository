from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Provider(models.Model):
    _name = 'ehr_cdss.provider'
    _description = 'Healthcare Provider'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    
    # Basic Information
    name = fields.Char(string="Provider Name", required=True, tracking=True)
    user_id = fields.Many2one('res.users', string="Related User", tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    image = fields.Binary(string="Provider Image")
    
    # Professional Information
    npi = fields.Char(string="NPI Number", tracking=True)
    provider_type = fields.Selection([
        ('physician', 'Physician'),
        ('nurse_practitioner', 'Nurse Practitioner'),
        ('physician_assistant', 'Physician Assistant'),
        ('psychologist', 'Psychologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('counselor', 'Counselor'),
        ('therapist', 'Therapist'),
        ('social_worker', 'Social Worker'),
        ('nurse', 'Nurse'),
        ('other', 'Other'),
    ], string="Provider Type", tracking=True)
    credential_ids = fields.Many2many('ehr_cdss.credential', string="Credentials")
    specialty_ids = fields.Many2many('ehr_cdss.specialty', string="Specialties")
    license_number = fields.Char(string="License Number", tracking=True)
    license_state = fields.Many2one('res.country.state', string="License State")
    license_expiry = fields.Date(string="License Expiration Date")
    
    # Contact Information
    contact_info_id = fields.Many2one('ehr_cdss.contact.info', string="Contact Information")
    address_id = fields.Many2one('ehr_cdss.address', string="Address")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    
    # Practice Information
    organization_id = fields.Many2one('ehr_cdss.organization', string="Organization")
    department_id = fields.Many2one('ehr_cdss.department', string="Department")
    location_ids = fields.Many2many('ehr_cdss.location', string="Practice Locations")
    room_id = fields.Many2one('ehr_cdss.room', string="Primary Room")
    accepting_new_patients = fields.Boolean(string="Accepting New Patients", default=True)
    
    # Service Capabilities
    service_types = fields.Many2many('ehr_cdss.service.type', string="Services Provided")
    treatment_approaches = fields.Many2many('ehr_cdss.treatment.approach', string="Treatment Approaches")
    populations_served = fields.Many2many('ehr_cdss.population', string="Populations Served")
    telehealth_available = fields.Boolean(string="Provides Telehealth Services", default=True)
    
    # Schedule
    working_hours_ids = fields.One2many('ehr_cdss.working.hours', 'provider_id', string="Working Hours")
    appointment_slot_ids = fields.One2many('ehr_cdss.appointment.slot', 'provider_id', string="Appointment Slots")
    appointment_ids = fields.One2many('ehr_cdss.appointment', 'provider_id', string="Appointments")
    
    # Patient Relationships
    patient_ids = fields.One2many('ehr_cdss.patient', 'primary_provider_id', string="Patients")
    patient_count = fields.Integer(string="Patient Count", compute="_compute_patient_count")
    
    # Records
    medical_record_ids = fields.One2many('ehr_cdss.medical.record', 'provider_id', string="Medical Records")
    treatment_plan_ids = fields.One2many('ehr_cdss.treatment.plan', 'provider_id', string="Treatment Plans")
    
    # Administrative
    signature = fields.Binary(string="Signature")
    is_supervisor = fields.Boolean(string="Is Supervisor")
    supervisee_ids = fields.Many2many('ehr_cdss.provider', 'provider_supervisor_rel', 
                                      'supervisor_id', 'supervisee_id', 
                                      string="Supervisees")
    supervisor_ids = fields.Many2many('ehr_cdss.provider', 'provider_supervisor_rel', 
                                     'supervisee_id', 'supervisor_id', 
                                     string="Supervisors")
    
    # Insurance and Billing
    accepted_insurance_ids = fields.Many2many('ehr_cdss.insurance.plan', string="Accepted Insurance Plans")
    billing_rate = fields.Float(string="Hourly Billing Rate")
    
    # State
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
    ], string="Status", default='active', tracking=True)
    
    _sql_constraints = [
        ('npi_unique', 'UNIQUE(npi)', 'NPI Number must be unique!')
    ]
    
    @api.depends('patient_ids')
    def _compute_patient_count(self):
        """Compute number of patients assigned to provider"""
        for record in self:
            record.patient_count = len(record.patient_ids)
    
    def action_activate(self):
        """Activate the provider"""
        return self.write({'state': 'active'})
    
    def action_deactivate(self):
        """Deactivate the provider"""
        return self.write({'state': 'inactive'})
    
    def action_on_leave(self):
        """Mark provider on leave"""
        return self.write({'state': 'on_leave'})
    
    def action_terminate(self):
        """Terminate the provider"""
        return self.write({'state': 'terminated', 'active': False})


class ServiceType(models.Model):
    _name = 'ehr_cdss.service.type'
    _description = 'Provider Service Type'
    
    name = fields.Char(string="Service Type", required=True)
    description = fields.Text(string="Description")
    billing_code_ids = fields.Many2many('ehr_cdss.billing.code', string="Related Billing Codes")


class TreatmentApproach(models.Model):
    _name = 'ehr_cdss.treatment.approach'
    _description = 'Treatment Approach'
    
    name = fields.Char(string="Approach Name", required=True)
    description = fields.Text(string="Description")
    abbreviation = fields.Char(string="Abbreviation")


class Population(models.Model):
    _name = 'ehr_cdss.population'
    _description = 'Population Served'
    
    name = fields.Char(string="Population", required=True)
    description = fields.Text(string="Description")


class WorkingHours(models.Model):
    _name = 'ehr_cdss.working.hours'
    _description = 'Provider Working Hours'
    _order = 'day_of_week,start_time'
    
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", required=True)
    location_id = fields.Many2one('ehr_cdss.location', string="Location")
    
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string="Day of Week", required=True)
    
    start_time = fields.Float(string="Start Time", required=True)
    end_time = fields.Float(string="End Time", required=True)
    
    is_telehealth = fields.Boolean(string="Telehealth Hours")
    notes = fields.Text(string="Notes")
    
    @api.constrains('start_time', 'end_time')
    def _check_times(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError(_("End time must be later than start time"))
