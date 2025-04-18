from odoo import models, fields, api

class AttendanceStudent(models.Model):
    _name = 'school_management.attendance.student'
    _description = 'Student Attendance'

    date = fields.Date(string="Date", default=fields.Date.today)
    student_id = fields.Many2one('school_management.student', string="Student")
    class_id = fields.Many2one('school_management.class', string="Class")
    section_id = fields.Many2one('school_management.section', string="Section")
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')
    ], string="Status", default='present')
    reason = fields.Char(string="Reason")
    marked_by = fields.Many2one('res.users', string="Marked By")
