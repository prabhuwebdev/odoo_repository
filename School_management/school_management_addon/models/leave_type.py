from odoo import models, fields, api

class LeaveType(models.Model):
    _name = 'school_management.leave.type'
    _description = 'Leave Type'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Leave Type")
    code = fields.Char(string="Code")
    days_allowed = fields.Float(string="Days Allowed Per Year", default=0.0)
    is_paid = fields.Boolean(string="Is Paid Leave", default=True)
    carry_forward = fields.Boolean(string="Allow Carry Forward", default=False)
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.code:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.code}"
