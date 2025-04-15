from odoo import fields, models,api


class FloorMaster(models.Model):
    _name ="floor.floor"
    _description = "Description about floor master"

    floor_name=fields.Char(string="Floor Name")