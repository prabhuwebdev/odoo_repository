from odoo import models, fields, api

class LibraryIssue(models.Model):
    _name = 'school_management.library.issue'
    _description = 'Library Issue'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    # name = fields.Char(string='Reference', default='New')
    book_id = fields.Many2one('school_management.library.book', string='Book')
    member_type = fields.Selection([('student', 'Student'), ('employee', 'Employee')], string='Member Type')
    student_id = fields.Many2one('school_management.student', string='Student')
    # employee_id = fields.Many2one('hr.employee', string='Employee')
    issue_date = fields.Date(string='Issue Date', default=fields.Date.today)
    due_date = fields.Date(string='Due Date')
    return_date = fields.Date(string='Return Date')
    actual_return_date = fields.Date(string='Actual Return Date')
    fine_amount = fields.Float(string='Fine Amount', default=0.0)
    fine_paid = fields.Boolean(string='Fine Paid', default=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('lost', 'Lost'),
        ('overdue', 'Overdue')
    ], string='Status', default='draft')
    issued_by = fields.Many2one('res.users', string='Issued By')
    returned_to = fields.Many2one('res.users', string='Returned To')
    notes = fields.Text(string='Notes')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not  record.issue_date:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.issue_date}"
