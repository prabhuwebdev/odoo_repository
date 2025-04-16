from odoo import models, fields, api

class Appraisal(models.Model):
    _name = 'school_management.appraisal'
    _description = 'Employee Appraisal'

    display_name=fields.Char(string="Appraisal ",compute="_compute_name_display",store=False)
    name = fields.Char(string="Reference", default="New")
    employee_id = fields.Many2one('school_management.employee', string="Employee")
    appraisal_date = fields.Date(string="Appraisal Date")
    evaluation_period = fields.Char(string="Evaluation Period")
    appraiser_id = fields.Many2one('res.users', string="Appraiser")
    overall_rating = fields.Float(string="Overall Rating", default=0.0)
    strengths = fields.Text(string="Strengths")
    areas_for_improvement = fields.Text(string="Areas for Improvement")
    goals = fields.Text(string="Future Goals")
    employee_remarks = fields.Text(string="Employee Remarks")
    appraiser_remarks = fields.Text(string="Appraiser Remarks")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')],
        default='draft', string="Status"
    )

    # @api.depends("name")
    # def _onchange_name(self):
    #     self.title=self.name

    # @api.depends()
    # def _compute_name_display(self):
    #     for record in self:
    #         record.title="NEW" if not record._origin.name else f"Edit {record.name}"

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"