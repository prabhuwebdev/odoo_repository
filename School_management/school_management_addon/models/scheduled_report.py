from odoo import models, fields, api
from datetime import datetime, timedelta

class ReportSchedule(models.Model):
    _name = 'school_management.schedule.report'
    _description = 'Report Schedule'

    display_name=fields.Char(string="Scheduled Report",compute="_compute_name_display",store=False)
    name = fields.Char(string='Schedule Name', required=True)
    report_id = fields.Many2one('school_management.custom.report', string='Report', required=True)
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ], string='Frequency', default='monthly', required=True)
    day_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Day of Week')
    day_of_month = fields.Integer(string='Day of Month', default=1)
    time_of_day = fields.Float(string='Time of Day', default=9.0)  # Example: 9.5 = 9:30 AM
    recipient_ids = fields.Many2many('res.partner', string='Recipients')
    email_subject = fields.Char(string='Email Subject')
    email_body = fields.Html(string='Email Body')
    active = fields.Boolean(string='Active', default=True)
    last_run = fields.Datetime(string='Last Run')
    next_run = fields.Datetime(string='Next Run', compute='_compute_next_run', store=True)

    @api.depends('last_run', 'frequency', 'day_of_week', 'day_of_month', 'time_of_day')
    def _compute_next_run(self):
        for record in self:
            next_time = datetime.now()

            if record.frequency == 'daily':
                next_time = next_time + timedelta(days=1)
            elif record.frequency == 'weekly' and record.day_of_week:
                days_map = {
                    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                    'friday': 4, 'saturday': 5, 'sunday': 6
                }
                target_day = days_map.get(record.day_of_week, 0)
                delta = (target_day - next_time.weekday()) % 7
                if delta == 0:
                    delta = 7
                next_time += timedelta(days=delta)
            elif record.frequency == 'monthly':
                next_month = next_time.replace(day=1) + timedelta(days=32)
                try:
                    next_time = next_month.replace(day=record.day_of_month)
                except ValueError:
                    next_time = next_month.replace(day=1) - timedelta(days=1)
            elif record.frequency == 'quarterly':
                month = ((next_time.month - 1) // 3 + 1) * 3 + 1
                if month > 12:
                    month -= 12
                    year = next_time.year + 1
                else:
                    year = next_time.year
                try:
                    next_time = next_time.replace(year=year, month=month, day=record.day_of_month)
                except ValueError:
                    next_time = next_time.replace(year=year, month=month, day=1) - timedelta(days=1)

            # Apply time_of_day
            hour = int(record.time_of_day)
            minutes = int((record.time_of_day - hour) * 60)
            next_time = next_time.replace(hour=hour, minute=minutes, second=0, microsecond=0)

            record.next_run = next_time

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
