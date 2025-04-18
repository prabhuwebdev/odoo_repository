from odoo import models, fields, api
from datetime import date

class AlumniEventRegistration(models.Model):
    _name = 'school_management.alumni.event.registration'
    _description = 'Alumni Event Registration'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    event_id = fields.Many2one('school_management.alumni.event', string='Event')
    alumni_id = fields.Many2one('school_management.alumni', string='Alumni')
    registration_date = fields.Date(string='Registration Date', default=fields.Date.today)
    attendance = fields.Boolean(string='Attended', default=False)
    fee_paid = fields.Boolean(string='Fee Paid', default=False)
    payment_method = fields.Selection(
        selection=[
            ('cash', 'Cash'),
            ('cheque', 'Cheque'),
            ('bank_transfer', 'Bank Transfer'),
            ('online', 'Online')
        ],
        string='Payment Method',
        default='online'
    )
    payment_reference = fields.Char(string='Payment Reference')
    notes = fields.Text(string='Notes')


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.registration_date:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.registration_date}"

