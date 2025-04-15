from odoo import fields,models

class SectionMaster(models.Model):
    _name = "section.master1"
    _description ="Description about section master"

    section_name=fields.Char(string="Section Name")