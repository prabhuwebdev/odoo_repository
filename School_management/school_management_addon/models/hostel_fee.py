from odoo import models, fields,api

class HostelFee(models.Model):
    _name = 'school_management.hostel.fee'
    _description = 'Hostel Fee'


    display_name = fields.Char(string="Hostel Fee",compute="_compute_name_display", store=False)
    name = fields.Char(string='Reference', default='New')
    # student_id = fields.Many2one('school.student', string='Student')
    room_id = fields.Many2one('school_management.hostel.room', string='Room')
    month = fields.Date(string='Month')
    amount = fields.Float(string='Amount', default=0.0)
    paid_amount = fields.Float(string='Paid Amount', default=0.0)
    payment_date = fields.Date(string='Payment Date')
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online')
    ], string='Payment Method', default='cash')
    status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid')
    ], string='Status', default='unpaid')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"