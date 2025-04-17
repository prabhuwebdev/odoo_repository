from odoo import fields, models,api

class SchoolNotice(models.Model):
    _name = 'school_management.notice'
    _description = 'School Notice'

    display_name = fields.Char(string="Notice", compute="_compute_name_display", store=False)


    name = fields.Char(string='Notice Title')
    notice_date = fields.Date(string='Notice Date', default=fields.Date.today)
    notice_type = fields.Selection([
        ('general', 'General'),
        ('exam', 'Exam'),
        ('event', 'Event'),
        ('holiday', 'Holiday'),
        ('fee', 'Fee')
    ], string='Notice Type', default='general')
    content = fields.Html(string='Content')
    recipient_type = fields.Selection([
        ('all', 'All'),
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('parent', 'Parent')
    ], string='Recipient Type', default='all')
    # applicable_classes = fields.Many2many('school_management.class', string='Applicable Classes')
    # applicable_departments = fields.Many2many('school_management.department', string='Applicable Departments')
    published = fields.Boolean(string='Published', default=False)
    publish_date = fields.Date(string='Publish Date')
    expiry_date = fields.Date(string='Expiry Date')
    # attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    # created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
