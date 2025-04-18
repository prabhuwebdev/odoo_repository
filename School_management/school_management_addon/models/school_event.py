from odoo import models, fields, api

class SchoolEvent(models.Model):
    _name = 'school_management.event'
    _description = 'School Event'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Event Name')
    # calendar_id = fields.Many2one('school_management.academic.calendar', string='Calendar')

    event_type = fields.Selection(
        selection=[
            ('holiday', 'Holiday'),
            ('exam', 'Exam'),
            ('sports', 'Sports'),
            ('cultural', 'Cultural'),
            ('meeting', 'Meeting'),
            ('other', 'Other'),
        ],
        string='Event Type'
    )

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    all_day = fields.Boolean(string='All Day', default=True)
    start_time = fields.Float(string='Start Time')
    end_time = fields.Float(string='End Time')
    venue = fields.Char(string='Venue')
    description = fields.Text(string='Description')

    participant_type = fields.Selection(
        selection=[
            ('all', 'All'),
            ('student', 'Student'),
            ('employee', 'Employee'),
            ('parent', 'Parent'),
        ],
        string='Participant Type',
        default='all'
    )

    applicable_classes = fields.Many2many('school_management.class', string='Applicable Classes')
    is_holiday = fields.Boolean(string='Is Holiday', default=False)
    create_notice = fields.Boolean(string='Create Notice', default=False)
    # notice_id = fields.Many2one('school_management.notice', string='Related Notice')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.start_date:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.start_date}"
