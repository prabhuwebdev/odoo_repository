from odoo import models, fields,api


class DashboardWidget(models.Model):
    _name = 'school_management.dashboard.widget'
    _description = 'Dashboard Widget'
    _order = 'sequence'

    display_name = fields.Char(string="Dashboard Widget",compute="_compute_name_display", store=False)

    name = fields.Char(string="Widget Name", required=True)
    widget_type = fields.Selection([
        ('chart', 'Chart'),
        ('kpi', 'KPI'),
        ('table', 'Table'),
        ('list', 'List'),
        ('calendar', 'Calendar')
    ], string="Widget Type", required=True)

    # model_id = fields.Many2one('ir.model', string="Data Model", required=True)

    domain_filter = fields.Char(string="Domain Filter")

    chart_type = fields.Selection([
        ('bar', 'Bar'),
        ('line', 'Line'),
        ('pie', 'Pie'),
        ('doughnut', 'Doughnut'),
        ('polar', 'Polar Area'),
        ('radar', 'Radar')
    ], string="Chart Type")

    measure_field = fields.Char(string="Measure Field")
    group_by_field = fields.Char(string="Group By Field")

    limit = fields.Integer(string="Record Limit", default=10)
    refresh_interval = fields.Integer(string="Auto Refresh (minutes)", default=0)

    color_scheme = fields.Char(string="Color Scheme")
    height = fields.Integer(string="Height (px)", default=300)
    width = fields.Integer(string="Width (columns)", default=4)

    sequence = fields.Integer(string="Sequence", default=10)
    # user_id = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user)
    active = fields.Boolean(string="Active", default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"

