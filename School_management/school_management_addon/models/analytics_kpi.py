from odoo import models, fields, api

class AnalyticsKPI(models.Model):
    _name = 'school_management.analytics.kpi'
    _description = 'Analytics KPI'

    display_name = fields.Char(string="Analytics KPI",compute="_compute_name_display", store=False)
    name = fields.Char(string='KPI Name', required=True)
    # model_id = fields.Many2one('ir.model', string='Model', required=True)
    measure_field = fields.Char(string='Measure Field')
    calculation_method = fields.Selection(
        selection=[
            ('count', 'Count'),
            ('sum', 'Sum'),
            ('average', 'Average'),
            ('min', 'Minimum'),
            ('max', 'Maximum'),
            ('custom', 'Custom'),
        ],
        string='Calculation Method',
        required=True
    )
    domain_filter = fields.Char(string='Domain Filter')
    comparison_period = fields.Selection(
        selection=[
            ('none', 'None'),
            ('previous_day', 'Previous Day'),
            ('previous_week', 'Previous Week'),
            ('previous_month', 'Previous Month'),
            ('previous_year', 'Previous Year'),
            ('custom', 'Custom'),
        ],
        string='Comparison Period',
        default='none'
    )
    target_value = fields.Float(string='Target Value', default=0.0)
    actual_value = fields.Float(string='Actual Value', compute='_compute_kpi_values', store=True)
    variance = fields.Float(string='Variance', compute='_compute_kpi_values', store=True)
    variance_percentage = fields.Float(string='Variance %', compute='_compute_kpi_values', store=True)

    direction = fields.Selection(
        selection=[
            ('up', 'Up'),
            ('down', 'Down')
        ],
        string='Positive Direction',
        default='up'
    )
    color_positive = fields.Char(string='Positive Color', default='green')
    color_negative = fields.Char(string='Negative Color', default='red')

    user_id = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    active = fields.Boolean(string='Active', default=True)

    @api.depends('target_value')
    def _compute_kpi_values(self):
        for record in self:
            # Placeholder logic, should be replaced with actual computation
            record.actual_value = 100.0  # mock value
            record.variance = record.actual_value - record.target_value
            if record.target_value:
                record.variance_percentage = (record.variance / record.target_value) * 100.0
            else:
                record.variance_percentage = 0.0

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
