from odoo import models, fields,api

class AlumniEvent(models.Model):
    _name = 'school_management.alumni.event'
    _description = 'Alumni Event'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Event Name')
    event_date = fields.Date(string='Event Date')
    event_time = fields.Float(string='Event Time')  # Can also be changed to fields.Datetime if needed
    venue = fields.Char(string='Venue')
    description = fields.Html(string='Description')
    registration_deadline = fields.Date(string='Registration Deadline')
    max_participants = fields.Integer(string='Maximum Participants')
    registration_fee = fields.Float(string='Registration Fee')
    organizer_id = fields.Many2one('res.partner', string='Organizer')
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        default='draft'
    )


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.event_date:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.event_date}"

