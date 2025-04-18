from odoo import models, fields,api

class ReportTemplateField(models.Model):
    _name = 'school_management.report.field'
    _description = 'Report Template Field'


    display_name = fields.Char(string="Report Field",compute="_compute_name_display", store=False)
    template_id = fields.Many2one(
        'school_management.report.template',
        string='Report Template',
        required=True,
        ondelete='cascade'
    )

    field_name = fields.Char(string='Field Name')
    field_label = fields.Char(string='Field Label')
    sequence = fields.Integer(string='Sequence', default=10)
    visible = fields.Boolean(string='Visible', default=True)

    aggregate = fields.Selection(
        selection=[
            ('none', 'None'),
            ('sum', 'Sum'),
            ('avg', 'Average'),
            ('min', 'Minimum'),
            ('max', 'Maximum'),
            ('count', 'Count'),
        ],
        string='Aggregate Function',
        default='none'
    )

    width = fields.Integer(string='Width (%)', default=0)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.field_name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.field_name}"
