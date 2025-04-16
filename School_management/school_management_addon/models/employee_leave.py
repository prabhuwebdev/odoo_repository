from odoo import models, fields, api

class EmployeeLeave(models.Model):
    _name = 'school_management.employee.leave'
    _description = 'Employee Leave'

    display_name = fields.Char(string="Employee Leave",compute="_compute_name_display", store=False)
    name = fields.Char(string="Reference", default="New")
    employee_id = fields.Many2one('school_management.employee', string="Employee")
    leave_type_id = fields.Many2one('school_management.leave.type', string="Leave Type")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    days = fields.Float(string="Number of Days", compute="_compute_days", store=True)
    reason = fields.Text(string="Reason")
    attachment = fields.Binary(string="Attachment")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')],
        string="Status", default='draft'
    )
    approved_by = fields.Many2one('res.users', string="Approved By")

    @api.depends('from_date', 'to_date')
    def _compute_days(self):
        for rec in self:
            if rec.from_date and rec.to_date:
                rec.days = (rec.to_date - rec.from_date).days + 1
            else:
                rec.days = 0


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"