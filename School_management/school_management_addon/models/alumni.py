from odoo import models, fields,api

class AlumniRecord(models.Model):
    _name = 'school_management.alumni'
    _description = 'Alumni Record'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Alumni Name')
    student_id = fields.Many2one('school_management.student', string='Student Record')
    graduation_year = fields.Char(string='Graduation Year')
    current_occupation = fields.Char(string='Current Occupation')
    organization = fields.Char(string='Organization')
    designation = fields.Char(string='Designation')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    linkedin_profile = fields.Char(string='LinkedIn Profile')
    higher_education = fields.Text(string='Higher Education')
    achievements = fields.Text(string='Achievements')
    is_active = fields.Boolean(string='Active Member', default=True)
    mentor = fields.Boolean(string='Available as Mentor', default=False)
    show_in_website = fields.Boolean(string='Show in Website', default=False)
    photo = fields.Binary(string='Photo')


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.student_id:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.student_id}"
