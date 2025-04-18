from odoo import models, fields, api

class OnlineAdmission(models.Model):
    _name = 'school_management.online.admission'
    _description = 'Online Admission'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Application Number", default="New")
    student_name = fields.Char(string="Student Name")
    gender = fields.Selection(
        selection=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string="Gender"
    )
    date_of_birth = fields.Date(string="Date of Birth")
    father_name = fields.Char(string="Father's Name")
    mother_name = fields.Char(string="Mother's Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    state_id = fields.Many2one('res.country.state', string="State")
    zip_code = fields.Char(string="ZIP")
    country_id = fields.Many2one('res.country', string="Country")
    class_id = fields.Many2one('school_management.class', string="Applying for Class")
    # academic_year_id = fields.Many2one('school.academic.year', string="Academic Year")
    application_date = fields.Date(string="Application Date", default=fields.Date.today)
    previous_school = fields.Char(string="Previous School")
    previous_class = fields.Char(string="Previous Class")

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('enrolled', 'Enrolled'),
            ('cancelled', 'Cancelled')
        ],
        string="Status",
        default='draft'
    )

    registration_fee = fields.Float(string="Registration Fee", default=0.0)
    fee_paid = fields.Boolean(string="Registration Fee Paid", default=False)
    payment_date = fields.Date(string="Payment Date")

    payment_method = fields.Selection(
        selection=[
            ('cash', 'Cash'),
            ('cheque', 'Cheque'),
            ('bank_transfer', 'Bank Transfer'),
            ('online', 'Online')
        ],
        string="Payment Method",
        default='online'
    )

    payment_reference = fields.Char(string="Payment Reference")
    notes = fields.Text(string="Notes")

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name}"