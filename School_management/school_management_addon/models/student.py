from odoo import models, fields, api
from datetime import date

class Student(models.Model):
    _name = 'school_management.student'
    _description = 'Student'

    name = fields.Char(string="Student Name")
    registration_number = fields.Char(string="Registration Number")
    admission_date = fields.Date(string="Admission Date", default=fields.Date.today)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    date_of_birth = fields.Date(string="Date of Birth")
    blood_group = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ], string="Blood Group")
    nationality = fields.Char(string="Nationality", default="Indian")
    religion = fields.Char(string="Religion")
    caste = fields.Char(string="Caste")
    category = fields.Selection([
        ('general', 'General'),
        ('obc', 'OBC'),
        ('sc', 'SC'),
        ('st', 'ST'),
        ('other', 'Other')
    ], string="Category")
    father_name = fields.Char(string="Father's Name")
    mother_name = fields.Char(string="Mother's Name")
    parent_id = fields.Many2one('res.partner', string="Parent")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    state_id = fields.Many2one('res.country.state', string="State")
    zip_code = fields.Char(string="ZIP")
    country_id = fields.Many2one('res.country', string="Country")
    class_id = fields.Many2one('school_management.class', string="Class")
    section_id = fields.Many2one('school_management.section', string="Section")
    roll_number = fields.Char(string="Roll Number")
    photo = fields.Binary(string="Photo")
    active = fields.Boolean(string="Active", default=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('enrolled', 'Enrolled'),
        ('alumnus', 'Alumnus'),
        ('terminated', 'Terminated')
    ], string="Status")
    transport_route_id = fields.Many2one('school_management.transport.route', string="Transport Route")
    # hostel_room_id = fields.Many2one('school_management.hostel.room', string="Hostel Room")
    user_id = fields.Many2one('res.users', string="Portal User")
