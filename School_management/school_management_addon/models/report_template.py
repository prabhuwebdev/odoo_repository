from odoo import models, fields,api


class ReportTemplate(models.Model):
    _name = 'school_management.report.template'
    _description = 'Report Template'
    _table = 'school_management_report_template'

    display_name = fields.Char(string="Report Template",compute="_compute_name_display", store=False)
    name = fields.Char(string='Template Name')
    # model_id = fields.Many2one('ir.model', string='Model')
    report_type = fields.Selection(
        selection=[
            ('tabular', 'Tabular'),
            ('chart', 'Chart'),
            ('matrix', 'Matrix'),
            ('summary', 'Summary'),
        ],
        string='Report Type',
        default='tabular'
    )

    template_file = fields.Binary(string='Template File', attachment=True)
    description = fields.Text(string='Description')

    is_system = fields.Boolean(string='System Template', default=False)
    active = fields.Boolean(string='Active', default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
