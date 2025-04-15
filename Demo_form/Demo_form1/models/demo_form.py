# from odoo import fields,models
#
#
# class DemoForm(models.Model):
#     _name ="demo.form"
#     _description = "description about demo.form"
#
#     name=fields.Char(string="Name")
#     age=fields.Integer(string="Age")
#     your_id=fields.Many2many("res.partner",string="Your Id")
#     country=fields.Selection([
#         ("india","India"),
#         ("australia","Australia"),
#         ("newzealand","NewZealand"),
#         ("england","England")
#     ])
#     country_id=fields.One2many("res.country",string="Country Id")
#     date_of_birth=fields.Date(string="Date Of Birth")
#
#     def get_demo(self):
#         return{
#            "your_name":self.name,
#             "your_age":self.age,
#             "your_country":self.country
#         }




from odoo import fields, models

class DemoForm(models.Model):
    _name = "demo.form"
    _description = "Description about demo.form"

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")

    # Many2many must specify a related model
    your_id = fields.Many2many("res.partner", string="Your Id")

    country = fields.Selection([
        ("india", "India"),
        ("australia", "Australia"),
        ("newzealand", "NewZealand"),
        ("england", "England")
    ], string="Country")

    # One2many must specify a related model and an inverse field
    # country_id = fields.One2many("res.country", "id", string="Country Id")

    dob = fields.Date(string="Date Of Birth")

    def get_demo(self):
        return {
            "your_name": self.name,
            "your_age": self.age,
            "your_country": self.country
        }
