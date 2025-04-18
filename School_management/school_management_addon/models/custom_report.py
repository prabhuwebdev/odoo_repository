from odoo import models, fields,api

class CustomReport(models.Model):
    _name = 'school_management.custom.report'
    _description = 'Custom Report'
    _table = 'school_management_custom_report'


    display_name = fields.Char(string="Custom Report",compute="_compute_name_display", store=False)
    name = fields.Char(string='Report Name', required=True)
    template_id = fields.Many2one('school_management.report.template', string='Based on Template')
    # user_id = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    filter_domain = fields.Char(string='Filter Domain')
    sort_by = fields.Char(string='Sort By')
    is_favorite = fields.Boolean(string='Favorite', default=False)
    last_run = fields.Datetime(string='Last Run')
    run_count = fields.Integer(string='Run Count', default=0)
    description = fields.Text(string='Description')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
