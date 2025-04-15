# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class first_module(models.Model):
#     _name = 'first_module.first_module'
#     _description = 'first_module.first_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models,fields,api

class CustomModule(models.Model):
    _name = "first_module.custom_module"
    _description = "Custom Module"

    name=fields.Char()
    age=fields.Integer()
    department=fields.Char()

class PriceRangeMaster(models.Model):
    _name = "price.range.master"
    _description = "Price Range Master"

    price_range=fields.Char()

class SectionMaster(models.Model):
    _name="section.master"
    _description = "Section Master"

    section=fields.Char()