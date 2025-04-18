from odoo import models, fields, api

class TransportAssignment(models.Model):
    _name = 'school_management.transport.assignment'
    _description = 'Transport Assignment'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    student_id = fields.Many2one('school_management.student', string="Student")
    route_id = fields.Many2one('school_management.transport.route', string="Route")
    stop_id = fields.Many2one('school_management.transport.stop', string="Stop")
    effective_date = fields.Date(string="Effective From", default=fields.Date.context_today)
    monthly_fee = fields.Float(string="Monthly Fee", default=0.0)
    active = fields.Boolean(default=True)



    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.monthly_fee:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.monthly_fee}"
