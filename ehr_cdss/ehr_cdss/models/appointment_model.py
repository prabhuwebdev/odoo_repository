from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
import random
import string

class Appointment(models.Model):
    _name = 'ehr_cdss.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_datetime'
    _rec_name = 'name'  # or whatever field you want shown
    
    # patient_id = fields.Char("Patient ID", readonly=True, default=lambda self: self._generate_patient_id())
    name = fields.Char(string="Appointment ID", readonly=True, default=lambda self: self._generate_patient_id())
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient", required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
    show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider",  tracking=True)
    
    # Scheduling Information
    appointment_slot_id = fields.Many2one('ehr_cdss.appointment.slot', string="Appointment Slot")
    start_datetime = fields.Datetime(string="Start Time",  tracking=True)
    end_datetime = fields.Datetime(string="End Time",  tracking=True)
    duration = fields.Float(string="Duration (minutes)", compute="_compute_duration", store=True)
    all_day = fields.Boolean(string="All Day Appointment")
    
    # Service Information
    service_type = fields.Selection([
        ('initial_assessment', 'Initial Assessment'),
        ('individual_therapy', 'Individual Therapy'),
        ('couples_therapy', 'Couples Therapy'),
        ('family_therapy', 'Family Therapy'),
        ('group_therapy', 'Group Therapy'),
        ('medication_management', 'Medication Management'),
        ('crisis_intervention', 'Crisis Intervention'),
        ('other', 'Other'),
    ], string="Service Type", tracking=True)
    # service_code_id = fields.Many2one('ehr_cdss.billing.code', string="Service Code")
    
    # Location
    # location_id = fields.Many2one('ehr_cdss.location', string="Location")
    # room_id = fields.Many2one('ehr_cdss.room', string="Room")
    is_telehealth = fields.Boolean(string="Telehealth Appointment")
    
    # Appointment Details
    purpose = fields.Text(string="Appointment Purpose")
    notes = fields.Text(string="Notes")
    medical_record_id = fields.Many2one('ehr_cdss.medical.record', string="Related Medical Record")
    
    auth_re = fields.Boolean(string='Auth Re')

    # Auth date (Date)
    auth_date = fields.Date(string='Auth Date')

    # Referral date (Date)
    referral_date = fields.Date(string='Referral Date')

    # Referral provider (Many2one to res.partner for referral provider)
    referral_provider = fields.Char( string='Referral Provider')

    # Appointment Status
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ('rescheduled', 'Rescheduled'),
    ], string="Status", default='scheduled', tracking=True)
    
    # Reminders
    reminder_sent = fields.Boolean(string="Reminder Sent")
    reminder_datetime = fields.Datetime(string="Reminder Time", compute="_compute_reminder_time", store=True)
    
    # Billing Info
    insurance_id = fields.Many2one('ehr_cdss.insurance', string="Insurance Used")
    is_billable = fields.Boolean(string="Billable Appointment", default=True)
    billing_status = fields.Selection([
        ('not_billed', 'Not Billed'),
        ('billed', 'Billed'),
        ('paid', 'Paid'),
        ('denied', 'Denied'),
        ('not_billable', 'Not Billable'),
    ], string="Billing Status", default='not_billed')
    
    # Check-in/Check-out
    checked_in = fields.Boolean(string="Checked In")
    check_in_time = fields.Datetime(string="Check-in Time")
    checked_out = fields.Boolean(string="Checked Out")
    check_out_time = fields.Datetime(string="Check-out Time")
    
    # Recurrence
    is_recurrent = fields.Boolean(string="Recurring Appointment")
    recurrence_id = fields.Many2one('ehr_cdss.appointment.recurrence', string="Recurrence Pattern")
    
    # Follow-up
    follow_up_appointment_id = fields.Many2one('ehr_cdss.appointment', string="Follow-up Appointment")
    is_follow_up = fields.Boolean(string="Is Follow-up Appointment")
    parent_appointment_id = fields.Many2one('ehr_cdss.appointment', string="Parent Appointment")
    
    # Calendar Integration
    calendar_event_id = fields.Many2one('calendar.event', string="Calendar Event")
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Appointment ID must be unique!')
    ]
    
    # @api.model
    # def create(self, vals):
    #     """Generate a unique appointment ID"""
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('ehr_cdss.appointment') or _('New')
    #     return super(Appointment, self).create(vals)
    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'AP-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration(self):
        """Compute appointment duration in minutes"""
        for record in self:
            if record.start_datetime and record.end_datetime:
                delta = record.end_datetime - record.start_datetime
                record.duration = delta.total_seconds() / 60
            else:
                record.duration = 0
    
    @api.depends('start_datetime')
    def _compute_reminder_time(self):
        """Compute reminder time (24 hours before appointment)"""
        for record in self:
            if record.start_datetime:
                record.reminder_datetime = record.start_datetime - timedelta(days=1)
            else:
                record.reminder_datetime = False
    
    @api.depends_context('from_patient_form')
    def _compute_show_back_button(self):
        for rec in self:
            print("rec: ",rec)
            rec.show_back_button = self._context.get('from_patient_form', False)
    
    @api.onchange('appointment_slot_id')
    def _onchange_appointment_slot(self):
        """Update appointment details based on slot selection"""
        if self.appointment_slot_id:
            self.provider_id = self.appointment_slot_id.provider_id
            self.start_datetime = self.appointment_slot_id.start_datetime
            self.end_datetime = self.appointment_slot_id.end_datetime
            self.location_id = self.appointment_slot_id.location_id
            self.room_id = self.appointment_slot_id.room_id
            self.is_telehealth = self.appointment_slot_id.is_telehealth
    
    @api.constrains('start_datetime', 'end_datetime')
    def _check_times(self):
        """Ensure end time is after start time"""
        for record in self:
            if record.start_datetime and record.end_datetime and record.start_datetime >= record.end_datetime:
                raise ValidationError(_("End time must be later than start time"))
    
    @api.constrains('provider_id', 'start_datetime', 'end_datetime')
    def _check_provider_availability(self):
        """Check if the provider is available for this appointment time"""
        for record in self:
            domain = [
                ('id', '!=', record.id),
                ('provider_id', '=', record.provider_id.id),
                ('state', 'not in', ['cancelled', 'rescheduled']),
                '|',
                '&', ('start_datetime', '<=', record.start_datetime), ('end_datetime', '>', record.start_datetime),
                '&', ('start_datetime', '<', record.end_datetime), ('end_datetime', '>=', record.end_datetime)
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(_("Provider is already booked for this time slot"))
            
    
    def action_progress_notes(self):
        # Assuming 'self' is a record for a person or patient.
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        progress_notes = self.env['ehr_cdss.medical.progress.note'].search([('patient_id', '=', record_id)], limit=1)
        
        if not progress_notes:
            # Handle case where no medical history exists for the patient
            progress_notes = self.env['ehr_cdss.medical.progress.note'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        return { 
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': progress_notes.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag

            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
    
    
    def action_back_to_patient(self):
        """ Redirect back to the Patient form """
        print("patient_id: ",self.patient_id.id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.info',
            'view_mode': 'form',
            'res_id': self.patient_id.id,  # Open the related patient record
            'target': 'current',
        }
        
        
    def action_medical_history(self):
        # Assuming 'self' is a record for a person or patient.
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        medical_history = self.env['ehr_cdss.medical.history'].search([('patient_id', '=', record_id)], limit=1)
        
        if not medical_history:
            # Handle case where no medical history exists for the patient
            medical_history = self.env['ehr_cdss.medical.history'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        return { 
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.history',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': medical_history.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag

            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
    
    def action_family_history(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        family_history = self.env['ehr_cdss.medical.family.history'].search([('patient_id', '=', record_id)], limit=1)
        
        if not family_history:
            # Handle case where no medical history exists for the patient
            family_history = self.env['ehr_cdss.medical.family.history'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.family.history',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': family_history.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trig
        }
        
    
    def open_insurance_record(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        self.ensure_one()
        insurance = self.env['ehr_cdss.patient.insurance_patient'].search([
            ('patient_id', '=', record_id)
        ], limit=1)

        if not insurance:
            insurance = self.env['ehr_cdss.patient.insurance_patient'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.insurance_patient',
            'view_mode': 'form',
            'res_id': insurance.id,
            'target': 'current',
            'context': {'from_patient_form': True},
        }
        
    def open_allergy_record(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        self.ensure_one()
        allergy = self.env['ehr_cdss.patient.allergy'].search([
            ('patient_id', '=', record_id)
        ], limit=1)

        if not allergy:
            allergy = self.env['ehr_cdss.patient.allergy'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.allergy',
            'view_mode': 'form',
            'res_id': allergy.id,
            'target': 'current',
            'context': {'from_patient_form': True},
        }
    def action_document(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        document = self.env['ehr_cdss.document'].search([('patient_id', '=', record_id)], limit=1)
        
        if not document:
            # Handle case where no medical history exists for the patient
            document = self.env['ehr_cdss.document'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.document',  # Replace with actual model
            'view_mode': 'kanban,form',
            'view_type': 'form',
            'res_id': document.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'domain': [('patient_id', '=', record_id)],  # Filter documents by patient
            'context': {'search_default_filter_by_patient': 1, 'default_patient_id': record_id},
        }
        
    def action_immunization_infectious_disease(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        immunization_id = self.env['ehr_cdss.patient.immunization.record'].search([('partner_id', '=', record_id)], limit=1)
        
        if not immunization_id:
            # Handle case where no medical history exists for the patient
            immunization_id = self.env['ehr_cdss.patient.immunization.record'].create({
                'partner_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.immunization.record',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': immunization_id.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }

    
    def action_medical_patient_allergy(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].search([('patient_id', '=', record_id)], limit=1)
        
        if not patient_allergy:
            # Handle case where no medical history exists for the patient
            patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.patient.allergy',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': patient_allergy.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        

    def action_medication(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        medication = self.env['ehr_cdss.medical.medication'].search([('patient_id', '=', record_id)], limit=1)
        
        if not medication:
            # Handle case where no medical history exists for the patient
            medication = self.env['ehr_cdss.medical.medication'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.medication',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': medication.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
    
    # def action_document(self):
    #     record_id = self.patient_id.id  # Get the ID of the current record (person)
    #     document = self.env['ehr_cdss.document'].search([('patient_id', '=', record_id)], limit=1)
        
    #     if not document:
    #         # Handle case where no medical history exists for the patient
    #         document = self.env['ehr_cdss.document'].create({
    #             'patient_id': record_id,
    #             'user_id': self.env.user.id,  # Associate the current user who is creating the record
    #         })
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'ehr_cdss.document',  # Replace with actual model
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'res_id': document.id,  # Pass the record ID of the person to be displayed
    #         'target': 'current',
    #         'context': {'from_patient_form': True},  # ✅ pass context flag
    #         'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
    #     }
        
    def dummy_action(self):
        pass  # Do nothing
    
    def action_confirm(self):
        """Confirm the appointment"""
        return self.write({'state': 'confirmed'})
    
    def action_start(self):
        """Start the appointment"""
        return self.write({
            'state': 'in_progress',
            'checked_in': True,
            'check_in_time': fields.Datetime.now()
        })
    
    def action_complete(self):
        """Complete the appointment"""
        return self.write({
            'state': 'completed',
            'checked_out': True,
            'check_out_time': fields.Datetime.now()
        })
    
    def action_cancel(self):
        """Cancel the appointment"""
        return self.write({'state': 'cancelled'})
    
    def action_no_show(self):
        """Mark as no show"""
        return self.write({'state': 'no_show'})
    
    def action_reschedule(self):
        """Mark as rescheduled and create a new appointment record"""
        self.write({'state': 'rescheduled'})
        
        # Create a copy for the rescheduled appointment
        new_appointment = self.copy({
            'state': 'scheduled',
            'is_follow_up': True,
            'parent_appointment_id': self.id,
            'medical_record_id': False,
            'check_in_time': False,
            'check_out_time': False,
            'checked_in': False,
            'checked_out': False,
            'reminder_sent': False,
        })
        
        self.follow_up_appointment_id = new_appointment.id
        return {
            'name': _('Reschedule Appointment'),
            'view_mode': 'form',
            'res_model': 'ehr_cdss.appointment',
            'res_id': new_appointment.id,
            'type': 'ir.actions.act_window',
        }
    
    def action_send_reminder(self):
        """Send appointment reminder to patient"""
        # Implementation would depend on notification system
        self.write({'reminder_sent': True})
        return True


class AppointmentRecurrence(models.Model):
    _name = 'ehr_cdss.appointment.recurrence'
    _description = 'Appointment Recurrence Pattern'
    
    name = fields.Char(string="Name", compute="_compute_name", store=True)
    
    # Recurrence Pattern
    recurrence_type = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ], string="Recurrence Type", required=True, default='weekly')
    
    interval = fields.Integer(string="Repeat Every", default=1, help="Interval between appointments")
    
    # Weekly Options
    weekday_mon = fields.Boolean(string="Monday")
    weekday_tue = fields.Boolean(string="Tuesday")
    weekday_wed = fields.Boolean(string="Wednesday")
    weekday_thu = fields.Boolean(string="Thursday")
    weekday_fri = fields.Boolean(string="Friday")
    weekday_sat = fields.Boolean(string="Saturday")
    weekday_sun = fields.Boolean(string="Sunday")
    
    # Monthly Options
    monthly_by = fields.Selection([
        ('date', 'Day of Month'),
        ('day', 'Day of Week'),
    ], string="Monthly By", default='date')
    
    # End Parameters
    end_type = fields.Selection([
        ('count', 'After'),
        ('end_date', 'On Date'),
        ('forever', 'Forever'),
    ], string="Ends", default='count')
    
    count = fields.Integer(string="Number of Occurrences", default=4)
    end_date = fields.Date(string="End Date")
    
    # Related Appointments
    appointment_ids = fields.One2many('ehr_cdss.appointment', 'recurrence_id', string="Appointments")
    
    @api.depends('recurrence_type', 'interval')
    def _compute_name(self):
        """Compute a descriptive name for the recurrence pattern"""
        for record in self:
            if record.recurrence_type == 'daily':
                name = _("Every day") if record.interval == 1 else _("Every %d days") % record.interval
            elif record.recurrence_type == 'weekly':
                name = _("Every week") if record.interval == 1 else _("Every %d weeks") % record.interval
            elif record.recurrence_type == 'monthly':
                name = _("Every month") if record.interval == 1 else _("Every %d months") % record.interval
            else:
                name = _("Custom recurrence")
            
            record.name = name
