from odoo import models, fields

class HostelAllocation(models.Model):
    _name = 'school_management.hostel.allocation'
    _description = 'Hostel Allocation'

    student_id = fields.Many2one('school.student', string='Student')
    room_id = fields.Many2one('school_management.hostel.room', string='Room')
    bed_number = fields.Integer(string='Bed Number', default=1)
    allotment_date = fields.Date(string='Allotment Date', default=fields.Date.today)
    vacating_date = fields.Date(string='Vacating Date')
    monthly_fee = fields.Float(string='Monthly Fee', compute='_compute_monthly_fee')
    security_deposit = fields.Float(string='Security Deposit', default=0.0)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('vacated', 'Vacated')
    ], string='Status', default='pending')

    def _compute_monthly_fee(self):
        for rec in self:
            rec.monthly_fee = rec.room_id.monthly_fee if rec.room_id else 0.0