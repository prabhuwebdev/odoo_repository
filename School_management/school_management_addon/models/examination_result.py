from odoo import models, fields, api

class ExaminationResult(models.Model):
    _name = 'school_management.examination.result'
    _description = 'Examination Result'

    student_id = fields.Many2one('school_management.student', string='Student')
    examination_id = fields.Many2one('school_management.examination', string='Examination')
    class_id = fields.Many2one('school_management.class', string='Class')
    section_id = fields.Many2one('school_management.section', string='Section')
    subject_id = fields.Many2one('school_management.subject', string='Subject')
    marks_obtained = fields.Float(string='Marks Obtained', default=0.0)
    max_marks = fields.Float(string='Maximum Marks', default=100.0)
    percentage = fields.Float(string='Percentage', compute='_compute_percentage', store=True)
    grade = fields.Char(string='Grade', compute='_compute_grade', store=True)
    pass_status = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ], string='Pass Status', compute='_compute_pass_status', store=True)
    remarks = fields.Char(string='Remarks')
    # evaluated_by = fields.Many2one('hr.employee', string='Evaluated By')

    @api.depends('marks_obtained', 'max_marks')
    def _compute_percentage(self):
        for record in self:
            record.percentage = (record.marks_obtained / record.max_marks) * 100

    @api.depends('percentage')
    def _compute_grade(self):
        for record in self:
            if record.percentage >= 90:
                record.grade = 'A'
            elif record.percentage >= 75:
                record.grade = 'B'
            elif record.percentage >= 50:
                record.grade = 'C'
            else:
                record.grade = 'D'

    @api.depends('percentage')
    def _compute_pass_status(self):
        for record in self:
            if record.percentage >= 35:
                record.pass_status = 'pass'
            else:
                record.pass_status = 'fail'
