from odoo import models, fields, api

class SalaryComponent(models.Model):
    _name = 'school_management.salary.component'
    _description = 'Salary Component'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    # employee_payroll_id = fields.Many2one('school_management.employee.payroll', string="Employee Payroll")
    name = fields.Char(string="Component Name")
    type = fields.Selection([
        ('allowance', 'Allowance'),
        ('deduction', 'Deduction')],
        string="Type"
    )
    amount = fields.Float(string="Amount", default=0.0)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.amount:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.amount}"
