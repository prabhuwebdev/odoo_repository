from odoo import fields,models

class SectionGroupMaster(models.Model):
    _name = "section.group.master"
    _description ="Description about section master"

    section_group_name=fields.Char(string="Section Group Name")

