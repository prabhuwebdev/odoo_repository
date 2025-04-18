from odoo import models, fields, api

class SchoolGlobalSetting(models.Model):
    _name = 'school_management.global.setting'
    _description = 'Global Settings for School'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='School Name')
    code = fields.Char(string='School Code')
    tagline = fields.Char(string='Tagline')
    logo = fields.Binary(string='Logo')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')
    currency_id = fields.Many2one('res.currency', string='Currency')
    language = fields.Selection(
        selection=[
            ('english', 'English'),
            ('hindi', 'Hindi'),
            ('spanish', 'Spanish'),
            ('french', 'French'),
            ('arabic', 'Arabic')
        ],
        string='Default Language',
        default='english'
    )
    academic_year_id = fields.Many2one('school_management.academic.year', string='Current Academic Year')
    date_format = fields.Selection(
        selection=[
            ('%d/%m/%Y', '%d/%m/%Y'),
            ('%d/%m/AY', '%d/%m/AY'),
            ('%m/%d/%Y', '%m/%d/%Y'),
            ('BY-%m-%d', 'BY-%m-%d')
        ],
        string='Date Format',
        default='%d/%m/%Y'
    )
    time_format = fields.Selection(
        selection=[
            ('12', '12-hour'),
            ('24', '24-hour')
        ],
        string='Time Format',
        default='24'
    )
    timezone = fields.Selection(
        selection=[
            ('UTC', 'UTC')
        ],
        string='Timezone',
        default='UTC'
    )
    admission_number_prefix = fields.Char(string='Admission Number Prefix', default='ADM')
    employee_number_prefix = fields.Char(string='Employee Number Prefix', default='EMP')
    default_attendance_type = fields.Selection(
        selection=[
            ('daily', 'Daily'),
            ('subject_wise', 'Subject Wise')
        ],
        string='Attendance Type',
        default='daily'
    )
    working_days = fields.Char(string='Working Days', default='1-5')
    grading_system_id = fields.Many2one('school_management.grading.system', string='Default Grading System')


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.code:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.code}"

