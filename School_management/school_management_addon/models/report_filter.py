from odoo import models, fields,api

class ReportFilter(models.Model):
    _name = 'school_management.report.filter'
    _description = 'Report Filter'
    _order = 'sequence'

    display_name = fields.Char(string="Report Filter",compute="_compute_name_display", store=False)
    template_id = fields.Many2one('school_management.report.template', string='Report Template')
    field_name = fields.Char(string='Field Name', required=True)
    field_label = fields.Char(string='Field Label')
    filter_type = fields.Selection([
        ('exact', 'Exact'),
        ('contains', 'Contains'),
        ('greater', 'Greater'),
        ('less', 'Less'),
        ('between', 'Between'),
        ('in', 'In'),
    ], string='Filter Type', default='exact')
    default_value = fields.Char(string='Default Value')
    is_required = fields.Boolean(string='Required', default=False)
    sequence = fields.Integer(string='Sequence', default=10)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.field_name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.field_name}"
