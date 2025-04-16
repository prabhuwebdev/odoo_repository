from odoo import models, fields, api

class EmployeePayroll(models.Model):
    _name = 'school_management.employee.payroll'
    _description = 'Employee Payroll'
    #
    payroll_id = fields.Many2one('school_management.payroll', string="Payroll")
    employee_id = fields.Many2one('school_management.employee', string="Employee")
    worked_days = fields.Float(string="Worked Days", default=0.0)
    basic_salary = fields.Float(string="Basic Salary", default=0.0)
    allowances = fields.Float(string="Total Allowances", compute="_compute_totals")
    deductions = fields.Float(string="Total Deductions", compute="_compute_totals")
    net_salary = fields.Float(string="Net Salary", compute="_compute_totals")
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('bank_transfer', 'Bank Transfer')],
        string="Payment Method", default='bank_transfer'
    )
    payment_status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid')],
        default='unpaid', string="Payment Status"
    )
    payment_date = fields.Date(string="Payment Date")

    # @api.depends('allowances', 'deductions', 'basic_salary')
    # def _compute_totals(self):
    #     for rec in self:
    #         allowance = sum(rec.salary_component_ids.filtered(lambda r: r.type == 'allowance').mapped('amount'))
    #         deduction = sum(rec.salary_component_ids.filtered(lambda r: r.type == 'deduction').mapped('amount'))
    #         rec.allowances = allowance
    #         rec.deductions = deduction
    #         rec.net_salary = rec.basic_salary + allowance - deduction
    #
    # salary_component_ids = fields.One2many('school_management.salary.component', 'employee_payroll_id', string="Salary Components")
    #
