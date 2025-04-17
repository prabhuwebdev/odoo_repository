from odoo import models, fields,api

class MobileAppSetting(models.Model):
    _name = 'school_management.mobile.app.setting'
    _description = 'Mobile App Setting'


    display_name = fields.Char(string="Mobile App", compute="_compute_name_display", store=False)
    name = fields.Char(string='Setting Name')
    app_version = fields.Char(string='App Version', default='1.0.0')
    fcm_server_key = fields.Char(string='FCM Server Key')
    enable_notifications = fields.Boolean(string='Enable Notifications', default=True)
    student_features = fields.Text(string='Student Features')
    parent_features = fields.Text(string='Parent Features')
    teacher_features = fields.Text(string='Teacher Features')
    maintenance_mode = fields.Boolean(string='Maintenance Mode', default=False)
    maintenance_message = fields.Text(string='Maintenance Message')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"