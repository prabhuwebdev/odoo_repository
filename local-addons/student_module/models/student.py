from odoo import fields,models

class Student(models.Model):
    _name = "student.student"
    _description = 'information about students'

    std_name=fields.Char(string='Student_name')
    std_age=fields.Integer(string='Student_age')
    book_price=fields.Float(string="Book Price")
    Read_book=fields.Boolean(string="Interest in Reading Books")
    dob=fields.Date(string="Enter Your Date Of Birthdate")
    your_country=fields.Selection([
        ("india", "India"),
        ("australia", "Australia"),
        ("england","England"),
        ("south africa", "South Africa")
    ])
    your_image=fields.Binary(string="upload your image")
    student_group = fields.One2many("student.profile", "student_id", string="Student Profiles")
    category_color=fields.Integer(string="Category Color")





from odoo import fields, models

class StudentProfile(models.Model):
    _name = "student.profile"
    _description = "Student Profile"

    student_id = fields.Many2one('student.student', string="Student", required=True, ondelete="cascade")
    profile_description = fields.Text(string="Profile Description")
    address = fields.Char(string="Address")
    student_photo = fields.Binary(string="Student Photo")
