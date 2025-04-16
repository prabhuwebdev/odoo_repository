from odoo import models, fields, api

class SchoolEmployee(models.Model):
    _name = 'school_management.employee'
    _description = 'Employee'

    display_name = fields.Char(string="Employee",compute="_compute_name_display", store=False)
    name = fields.Char(string='Employee Name')
    employee_code = fields.Char(string='Employee Code')
    joining_date = fields.Date(string='Joining Date')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    date_of_birth = fields.Date(string='Date of Birth')
    job_position_id = fields.Many2one('school.job.position', string='Job Position')
    department_id = fields.Many2one('school_management.department', string='Department')
    work_email = fields.Char(string='Work Email')
    work_phone = fields.Char(string='Work Phone')
    mobile = fields.Char(string='Mobile')
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    zip = fields.Char(string='ZIP')
    country_id = fields.Many2one('res.country', string='Country')
    qualification = fields.Char(string='Qualification')
    experience = fields.Float(string='Experience', default=0.0)
    resume = fields.Binary(string='Resume')
    photo = fields.Binary(string='Photo')
    contract_type = fields.Selection([
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('part_time', 'Part Time')
    ], string='Contract Type')
    contract_end_date = fields.Date(string='Contract End Date')
    bank_account_number = fields.Char(string='Bank Account Number')
    bank_name = fields.Char(string='Bank Name')
    ifsc_code = fields.Char(string='IFSC Code')
    emergency_contact = fields.Char(string='Emergency Contact')
    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one('res.users', string='Portal User')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"