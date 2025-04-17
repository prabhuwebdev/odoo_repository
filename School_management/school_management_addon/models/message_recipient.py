from odoo import fields, models,api

class MessageRecipient(models.Model):
    _name = 'school_management.message.recipient'
    _description = 'Message Recipient'

    display_name = fields.Char(string="Message Recipient", compute="_compute_name_display", store=False)

    message_id = fields.Many2one('school_management.message', string='Message')
    recipient_type = fields.Selection([
        ('user', 'User'),
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('parent', 'Parent'),
        ('class', 'Class'),
        ('department', 'Department')
    ], string='Recipient Type', default='user')

    # user_id = fields.Many2one('res.users', string='User')
    # student_id = fields.Many2one('school.student', string='Student')
    employee_id = fields.Many2one('school_management.employee', string='Employee')
    # parent_id = fields.Many2one('res.partner', string='Parent')
    # class_id = fields.Many2one('school.class', string='Class')
    department_id = fields.Many2one('school_management.department', string='Department')

    state = fields.Selection([
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read')
    ], string='Status', default='sent')

    read_date = fields.Datetime(string='Read Date')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.recipient_type:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.recipient_type}"
