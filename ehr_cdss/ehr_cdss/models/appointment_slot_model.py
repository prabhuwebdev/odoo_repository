from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
import random
import string


class AppointmentSlot(models.Model):
    _name = 'ehr_cdss.appointment.slot'
    _description = 'Appointment Slot'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_datetime'
    
    name = fields.Char(string="Slot ID", readonly=True, default=lambda self: self._generate_patient_id())
    
    # Provider and Location
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", required=True, tracking=True)
    # location_id = fields.Many2one('ehr_cdss.location', string="Location", tracking=True)
    # room_id = fields.Many2one('ehr_cdss.room', string="Room", tracking=True)
    
    # Time Information
    start_datetime = fields.Datetime(string="Start Time", required=True, tracking=True)
    end_datetime = fields.Datetime(string="End Time", required=True, tracking=True)
    duration = fields.Float(string="Duration (minutes)", compute="_compute_duration", store=True)
    
    # Appointment
    appointment_id = fields.Many2one('ehr_cdss.appointment', string="Booked Appointment")
    
    # Service Details
    service_type = fields.Selection([
        ('initial_assessment', 'Initial Assessment'),
        ('individual_therapy', 'Individual Therapy'),
        ('couples_therapy', 'Couples Therapy'),
        ('family_therapy', 'Family Therapy'),
        ('group_therapy', 'Group Therapy'),
        ('medication_management', 'Medication Management'),
        ('crisis_intervention', 'Crisis Intervention'),
        ('other', 'Other'),
    ], string="Service Type")
    
    # service_code_id = fields.Many2one('ehr_cdss.billing.code', string="Service Code")
    
    # Restrictions
    insurance_ids = fields.Many2many('ehr_cdss.insurance.plan', string="Accepted Insurance")
    new_patients_only = fields.Boolean(string="New Patients Only")
    existing_patients_only = fields.Boolean(string="Existing Patients Only")
    # specific_diagnosis_ids = fields.Many2many('ehr_cdss.diagnosis', string="Specific Diagnoses")
    priority_patients = fields.Selection([
        ('crisis', 'Crisis/Urgent'),
        ('high', 'High Priority'),
        ('standard', 'Standard'),
        ('followup', 'Follow-up Only'),
    ], string="Priority Level")
    
    # Telehealth
    is_telehealth = fields.Boolean(string="Telehealth Appointment", default=False)
    telehealth_platform = fields.Char(string="Telehealth Platform")
    
    # Group Slots
    is_group = fields.Boolean(string="Group Appointment", default=False)
    max_attendees = fields.Integer(string="Maximum Attendees")
    current_attendees = fields.Integer(string="Current Attendees", compute="_compute_current_attendees")
    group_name = fields.Char(string="Group Name")
    group_description = fields.Text(string="Group Description")
    
    # Recurrence Information
    is_recurring = fields.Boolean(string="Recurring Slot", default=False)
    recurrence_id = fields.Many2one('ehr_cdss.appointment.slot.recurrence', string="Recurrence Pattern")
    
    # Buffer Time
    buffer_before = fields.Float(string="Buffer Before (minutes)", default=0)
    buffer_after = fields.Float(string="Buffer After (minutes)", default=0)
    
    # Notes and Description
    notes = fields.Text(string="Notes")
    
    # State
    state = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('reserved', 'Reserved'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ], string="Status", default='available', tracking=True)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Slot ID must be unique!'),
    ]
    
    # @api.model
    # def create(self, vals):
    #     """Generate unique slot ID"""
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('ehr_cdss.appointment.slot') or _('New')
    #     return super(AppointmentSlot, self).create(vals)
    
    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'AP-SLOT' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration(self):
        """Compute appointment duration in minutes"""
        for record in self:
            if record.start_datetime and record.end_datetime:
                delta = record.end_datetime - record.start_datetime
                record.duration = delta.total_seconds() / 60
            else:
                record.duration = 0
    
    @api.depends('appointment_id', 'is_group', 'max_attendees')
    def _compute_current_attendees(self):
        """Compute current attendees for group appointments"""
        for record in self:
            if record.is_group:
                # For a group slot, count all appointments linked to this slot
                record.current_attendees = self.env['ehr_cdss.appointment'].search_count([
                    ('appointment_slot_id', '=', record.id),
                    ('state', 'not in', ['cancelled', 'no_show', 'rescheduled']),
                ])
            else:
                # For individual slots, either 0 or 1
                record.current_attendees = 1 if record.appointment_id else 0
    
    @api.constrains('start_datetime', 'end_datetime')
    def _check_times(self):
        """Ensure end time is after start time"""
        for record in self:
            if record.start_datetime >= record.end_datetime:
                raise ValidationError(_("End time must be later than start time"))
    
    @api.constrains('is_group', 'max_attendees')
    def _check_group_settings(self):
        """Ensure group settings are valid"""
        for record in self:
            if record.is_group and (not record.max_attendees or record.max_attendees < 2):
                raise ValidationError(_("Group appointments must allow at least 2 attendees"))
    
    @api.onchange('provider_id')
    def _onchange_provider(self):
        """Update fields based on provider"""
        if self.provider_id:
            # Set location if provider has a primary location
            if self.provider_id.location_ids:
                self.location_id = self.provider_id.location_ids[0].id
            
            # Set room if provider has a primary room
            if self.provider_id.room_id:
                self.room_id = self.provider_id.room_id.id
    
    @api.onchange('service_type')
    def _onchange_service_type(self):
        """Update duration based on service type"""
        if self.service_type:
            # Set default duration based on service type
            if self.service_type == 'initial_assessment':
                self.end_datetime = self.start_datetime + timedelta(minutes=90) if self.start_datetime else False
            elif self.service_type in ['individual_therapy', 'couples_therapy', 'family_therapy']:
                self.end_datetime = self.start_datetime + timedelta(minutes=50) if self.start_datetime else False
            elif self.service_type == 'medication_management':
                self.end_datetime = self.start_datetime + timedelta(minutes=30) if self.start_datetime else False
    
    def action_reserve(self):
        """Reserve the appointment slot"""
        return self.write({'state': 'reserved'})
    
    def action_book(self, appointment_id=False):
        """Book the appointment slot"""
        vals = {'state': 'booked'}
        if appointment_id:
            vals['appointment_id'] = appointment_id
        return self.write(vals)
    
    def action_cancel(self):
        """Cancel the appointment slot"""
        return self.write({'state': 'cancelled'})
    
    def action_reset(self):
        """Reset to available"""
        return self.write({
            'state': 'available', 
            'appointment_id': False
        })
    
    def action_complete(self):
        """Mark as completed"""
        return self.write({'state': 'completed'})
    
    def create_appointment(self):
        """Create an appointment from this slot"""
        self.ensure_one()
        
        if self.state != 'available':
            raise ValidationError(_("Cannot create appointment from a slot that is not available"))
        
        return {
            'name': _('Create Appointment'),
            'view_mode': 'form',
            'res_model': 'ehr_cdss.appointment',
            'context': {
                'default_appointment_slot_id': self.id,
                'default_provider_id': self.provider_id.id,
                'default_start_datetime': self.start_datetime,
                'default_end_datetime': self.end_datetime,
                'default_location_id': self.location_id.id,
                'default_room_id': self.room_id.id,
                'default_service_type': self.service_type,
                'default_service_code_id': self.service_code_id.id,
                'default_is_telehealth': self.is_telehealth,
            },
            'target': 'current',
            'type': 'ir.actions.act_window',
        }


class AppointmentSlotRecurrence(models.Model):
    _name = 'ehr_cdss.appointment.slot.recurrence'
    _description = 'Appointment Slot Recurrence Pattern'
    
    name = fields.Char(string="Recurrence Name", compute="_compute_name", store=True)
    
    # Provider and Slot Information
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", required=True)
    slot_template_id = fields.Many2one('ehr_cdss.appointment.slot', string="Slot Template")
    
    # Time Information
    start_time = fields.Float(string="Start Time", required=True)
    end_time = fields.Float(string="End Time", required=True)
    duration = fields.Float(string="Duration (minutes)", compute="_compute_duration", store=True)
    
    # Service and Location
    service_type = fields.Selection([
        ('initial_assessment', 'Initial Assessment'),
        ('individual_therapy', 'Individual Therapy'),
        ('couples_therapy', 'Couples Therapy'),
        ('family_therapy', 'Family Therapy'),
        ('group_therapy', 'Group Therapy'),
        ('medication_management', 'Medication Management'),
        ('crisis_intervention', 'Crisis Intervention'),
        ('other', 'Other'),
    ], string="Service Type")
    
    location_id = fields.Many2one('ehr_cdss.location', string="Location")
    room_id = fields.Many2one('ehr_cdss.room', string="Room")
    is_telehealth = fields.Boolean(string="Telehealth Appointment", default=False)
    
    # Recurrence Pattern
    recurrence_type = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ], string="Recurrence Type", required=True, default='weekly')
    
    # Interval
    interval = fields.Integer(string="Repeat Every", default=1, help="Interval between appointments")
    
    # Daily Options
    daily_type = fields.Selection([
        ('all', 'Every day'),
        ('weekday', 'Every weekday (Mon-Fri)'),
    ], string="Daily Type", default='all')
    
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
    
    monthly_day = fields.Integer(string="Day of Month", default=1)
    monthly_week = fields.Selection([
        ('first', 'First'),
        ('second', 'Second'),
        ('third', 'Third'),
        ('fourth', 'Fourth'),
        ('last', 'Last'),
    ], string="Week of Month", default='first')
    
    monthly_weekday = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string="Day of Week", default='0')
    
    # End Parameters
    end_type = fields.Selection([
        ('count', 'After'),
        ('end_date', 'On Date'),
        ('forever', 'Forever'),
    ], string="Ends", default='count')
    
    count = fields.Integer(string="Number of Occurrences", default=10)
    end_date = fields.Date(string="End Date")
    
    # Date Range
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    
    # Generated Slots
    slot_ids = fields.One2many('ehr_cdss.appointment.slot', 'recurrence_id', string="Generated Slots")
    
    # Status
    active = fields.Boolean(string="Active", default=True)
    
    @api.depends('provider_id', 'recurrence_type', 'interval')
    def _compute_name(self):
        """Compute a descriptive name for the recurrence pattern"""
        for record in self:
            provider_name = record.provider_id.name if record.provider_id else ""
            
            if record.recurrence_type == 'daily':
                frequency = _("Every day") if record.interval == 1 else _("Every %d days") % record.interval
            elif record.recurrence_type == 'weekly':
                frequency = _("Every week") if record.interval == 1 else _("Every %d weeks") % record.interval
            elif record.recurrence_type == 'monthly':
                frequency = _("Every month") if record.interval == 1 else _("Every %d months") % record.interval
            else:
                frequency = _("Custom recurrence")
            
            record.name = f"{provider_name} - {frequency}"
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        """Compute duration in minutes from start and end time"""
        for record in self:
            if record.start_time < record.end_time:
                # Convert hours to minutes
                duration_hours = record.end_time - record.start_time
                record.duration = duration_hours * 60
            else:
                record.duration = 0
    
    @api.constrains('start_time', 'end_time')
    def _check_times(self):
        """Ensure end time is after start time"""
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError(_("End time must be later than start time"))
    
    @api.onchange('recurrence_type')
    def _onchange_recurrence_type(self):
        """Set default values based on recurrence type"""
        if self.recurrence_type == 'weekly':
            # Default to current weekday
            today_weekday = fields.Date.today().weekday()
            self.weekday_mon = today_weekday == 0
            self.weekday_tue = today_weekday == 1
            self.weekday_wed = today_weekday == 2
            self.weekday_thu = today_weekday == 3
            self.weekday_fri = today_weekday == 4
            self.weekday_sat = today_weekday == 5
            self.weekday_sun = today_weekday == 6
    
    def _prepare_slot_values(self, date):
        """Prepare values for creating a slot"""
        start_hour = int(self.start_time)
        start_minute = int((self.start_time - start_hour) * 60)
        
        end_hour = int(self.end_time)
        end_minute = int((self.end_time - end_hour) * 60)
        
        start_datetime = fields.Datetime.to_datetime(date).replace(
            hour=start_hour, minute=start_minute, second=0
        )
        end_datetime = fields.Datetime.to_datetime(date).replace(
            hour=end_hour, minute=end_minute, second=0
        )
        
        return {
            'provider_id': self.provider_id.id,
            'location_id': self.location_id.id if self.location_id else False,
            'room_id': self.room_id.id if self.room_id else False,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'service_type': self.service_type,
            'is_telehealth': self.is_telehealth,
            'recurrence_id': self.id,
            'is_recurring': True,
            'state': 'available',
        }
    
    def action_generate_slots(self):
        """Generate appointment slots based on recurrence pattern"""
        self.ensure_one()
        
        # Clear any existing generated slots
        self.slot_ids.unlink()
        
        # Determine end date
        if self.end_type == 'count':
            # Calculate end date based on count and frequency
            if self.recurrence_type == 'daily':
                end_date = fields.Date.from_string(self.start_date) + timedelta(days=self.count * self.interval)
            elif self.recurrence_type == 'weekly':
                # For weekly, consider the number of days selected
                weekdays_selected = sum([
                    self.weekday_mon, self.weekday_tue, self.weekday_wed,
                    self.weekday_thu, self.weekday_fri, self.weekday_sat, self.weekday_sun
                ])
                if weekdays_selected == 0:
                    raise ValidationError(_("Please select at least one day of the week"))
                
                # Rough estimate for end date
                weeks_needed = (self.count + weekdays_selected - 1) // weekdays_selected
                end_date = fields.Date.from_string(self.start_date) + timedelta(weeks=weeks_needed * self.interval)
            elif self.recurrence_type == 'monthly':
                end_date = fields.Date.from_string(self.start_date) + timedelta(days=self.count * 31)
            else:
                # Default to 1 year for custom patterns
                end_date = fields.Date.from_string(self.start_date) + timedelta(days=365)
        elif self.end_type == 'end_date':
            end_date = fields.Date.from_string(self.end_date)
        else:  # forever
            # Default to 1 year for indefinite patterns
            end_date = fields.Date.from_string(self.start_date) + timedelta(days=365)
        
        # Generate slots
        slots_to_create = []
        current_date = fields.Date.from_string(self.start_date)
        slot_count = 0
        
        while current_date <= end_date and (self.end_type != 'count' or slot_count < self.count):
            if self.recurrence_type == 'daily':
                if self.daily_type == 'all' or (self.daily_type == 'weekday' and current_date.weekday() < 5):
                    slots_to_create.append(self._prepare_slot_values(current_date))
                    slot_count += 1
                current_date += timedelta(days=self.interval)
            
            elif self.recurrence_type == 'weekly':
                # Check each weekday
                weekday = current_date.weekday()
                weekday_flags = [
                    self.weekday_mon, self.weekday_tue, self.weekday_wed,
                    self.weekday_thu, self.weekday_fri, self.weekday_sat, self.weekday_sun
                ]
                
                if weekday_flags[weekday]:
                    slots_to_create.append(self._prepare_slot_values(current_date))
                    slot_count += 1
                
                # Move to next day
                current_date += timedelta(days=1)
                
                # If we've completed a week, apply the interval
                if current_date.weekday() == 0:
                    current_date += timedelta(days=(self.interval - 1) * 7)
            
            elif self.recurrence_type == 'monthly':
                if self.monthly_by == 'date':
                    # Day of month (e.g., 15th of each month)
                    if current_date.day == self.monthly_day:
                        slots_to_create.append(self._prepare_slot_values(current_date))
                        slot_count += 1
                        
                        # Move to next month
                        next_month = current_date.month + self.interval
                        next_year = current_date.year + (next_month - 1) // 12
                        next_month = ((next_month - 1) % 12) + 1
                        
                        # Try to maintain the same day, but adjust for month length
                        try:
                            current_date = current_date.replace(year=next_year, month=next_month)
                        except ValueError:
                            # Handle edge case (e.g., February 30)
                            last_day = self._get_last_day_of_month(next_year, next_month)
                            current_date = current_date.replace(year=next_year, month=next_month, day=last_day)
                    else:
                        # Move to next day
                        current_date += timedelta(days=1)
                else:  # day of week
                    # Calculate the position (1st, 2nd, etc. Monday, Tuesday, etc.)
                    day_of_week = int(self.monthly_weekday)
                    if current_date.weekday() == day_of_week:
                        week_number = (current_date.day - 1) // 7 + 1
                        is_last_week = current_date.day + 7 > self._get_last_day_of_month(current_date.year, current_date.month)
                        
                        if (self.monthly_week == 'first' and week_number == 1) or \
                           (self.monthly_week == 'second' and week_number == 2) or \
                           (self.monthly_week == 'third' and week_number == 3) or \
                           (self.monthly_week == 'fourth' and week_number == 4) or \
                           (self.monthly_week == 'last' and is_last_week):
                            slots_to_create.append(self._prepare_slot_values(current_date))
                            slot_count += 1
                            
                            # Move to next month
                            next_month = current_date.month + self.interval
                            next_year = current_date.year + (next_month - 1) // 12
                            next_month = ((next_month - 1) % 12) + 1
                            
                            # Set to first day of next month and find the right day
                            current_date = current_date.replace(year=next_year, month=next_month, day=1)
                            while current_date.weekday() != day_of_week:
                                current_date += timedelta(days=1)
                            
                            # Adjust based on week number
                            if self.monthly_week != 'first':
                                if self.monthly_week == 'last':
                                    # Go to last week of the month
                                    while current_date.day + 7 <= self._get_last_day_of_month(current_date.year, current_date.month):
                                        current_date += timedelta(days=7)
                                else:
                                    # Go to specific week
                                    week_offset = {'second': 1, 'third': 2, 'fourth': 3}
                                    current_date += timedelta(days=7 * week_offset[self.monthly_week])
                        else:
                            # Move to next day
                            current_date += timedelta(days=1)
                    else:
                        # Move to next day
                        current_date += timedelta(days=1)
            
            else:  # custom
                # Implementation for custom patterns would go here
                break
        
        # Create the slots
        for vals in slots_to_create:
            self.env['ehr_cdss.appointment.slot'].create(vals)
        
        return True
    
    def _get_last_day_of_month(self, year, month):
        """Get the last day of the given month"""
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        first_day_next_month = fields.Date.to_date(f"{next_year}-{next_month:02d}-01")
        last_day = first_day_next_month - timedelta(days=1)
        return last_day.day
