from odoo import models, fields,api

class LibraryFine(models.Model):
    _name = 'school_management.library.fine'
    _description = 'Library Fine'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    # name = fields.Char(string='Reference', default='New')
    issue_id = fields.Many2one('school_management.library.issue', string='Library Issue')
    member_type = fields.Selection([('student', 'Student'), ('employee', 'Employee')], string='Member Type')
    student_id = fields.Many2one('school_management.student', string='Student')
    # employee_id = fields.Many2one('school_management.hr.employee', string='Employee')
    fine_amount = fields.Float(string='Fine Amount', default=0.0)
    payment_date = fields.Date(string='Payment Date')
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online')
    ], string='Payment Method', default='cash')
    received_by = fields.Many2one('res.users', string='Received By')
    state = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid')
    ], string='Status', default='unpaid')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not  record.fine_amount:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.fine_amount}"
