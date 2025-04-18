from odoo import models, fields, api

class AttendanceStaff(models.Model):
    _name = 'school_management.attendance.staff'
    _description = 'Staff Attendance'

    date = fields.Date(string='Date', default=fields.Date.today)
    # employee_id = fields.Many2one('hr.employee', string='Employee')
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('leave', 'Leave')
    ], string='Status', default='present')
    reason = fields.Char(string='Reason')
    check_in = fields.Datetime(string='Check In Time')
    check_out = fields.Datetime(string='Check Out Time')
    working_hours = fields.Float(string='Working Hours', compute='_compute_working_hours', store=True)
    # marked_by = fields.Many2one('hr.employee', string='Marked By')

    @api.depends('check_in', 'check_out')
    def _compute_working_hours(self):
        for record in self:
            if record.check_in and record.check_out:
                record.working_hours = (record.check_out - record.check_in).seconds / 3600
