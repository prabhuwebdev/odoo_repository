from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
import random
import string

class TreatmentPlan(models.Model):
    _name = 'ehr_cdss.treatment.plan'
    _description = 'Treatment Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Plan ID", readonly=True, default=lambda self: self._generate_patient_id())
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient", required=True, tracking=True)
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", required=True, tracking=True)
    
    # Dates
    create_date = fields.Datetime(string="Creation Date", readonly=True)
    date = fields.Date(string="Plan Date", default=fields.Date.today, tracking=True)
    last_update_date = fields.Date(string="Last Updated", tracking=True)
    
    # Treatment Goals
    goal_ids = fields.One2many('ehr_cdss.goal', 'treatment_plan_id', string="Treatment Goals")
    
    # Plan Details
    frequency = fields.Selection([
        ('twice_week', 'Twice a week'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Every other week'),
        ('monthly', 'Monthly'),
        ('other', 'Other'),
    ], string="Frequency of Treatment", tracking=True)
    
    anticipated_duration = fields.Selection([
        ('less_than_3', 'Less than 3 months'),
        ('3_to_6', '3-6 months'),
        ('6_to_12', '6 months - 1 year'),
        ('1_year_plus', '1 year or more'),
    ], string="Anticipated Length of Treatment", tracking=True)
    
    comments = fields.Text(string="Comments")
    
    # Validation
    reviewed_with_client = fields.Boolean(string="Reviewed with Client", default=False, tracking=True)
    client_participation = fields.Boolean(string="Client Participated in Development", default=False, tracking=True)
    
    # Next Visit
    next_visit_timing = fields.Selection([
        ('within_7', 'Within 7 days of this appt'),
        ('within_10', 'Within 10 days of this appt'),
        ('more_than_10_full', 'More than 10 days- therapist full/unavailable'),
        ('more_than_10_other', 'More than 10 days- other'),
        ('more_than_10_no_necessity', 'More than 10 days- no medical necessity'),
        ('more_than_10_client', 'More than 10 days- client request'),
        ('other_unknown', 'Other/Unknown'),
    ], string="Next Visit Info", tracking=True)
    
    # Related Records
    # diagnosis_ids = fields.Many2many('ehr_cdss.diagnosis', string="Related Diagnoses")
    medical_record_id = fields.Many2one('ehr_cdss.medical.record', string="Medical Record")
    # document_id = fields.Many2one('ehr_cdss.document', string="Related Document")
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], string="Status", default='draft', tracking=True)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Plan ID must be unique!')
    ]
    
    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'TP-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def write(self, vals):
        """Update last_update_date when changed"""
        if any(field not in ['last_update_date', 'state'] for field in vals.keys()):
            vals['last_update_date'] = fields.Date.today()
        return super(TreatmentPlan, self).write(vals)
    
    def action_activate(self):
        """Activate the treatment plan"""
        return self.write({'state': 'active'})
    
    def action_complete(self):
        """Mark the treatment plan as completed"""
        return self.write({'state': 'completed'})
    
    def action_cancel(self):
        """Cancel the treatment plan"""
        return self.write({'state': 'canceled'})
    
    def action_draft(self):
        """Set the treatment plan back to draft"""
        return self.write({'state': 'draft'})


class Goal(models.Model):
    _name = 'ehr_cdss.goal'
    _description = 'Treatment Goal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'
    
    name = fields.Char(string="Goal ID", readonly=True, copy=False, default=lambda self: _('New'))
    sequence = fields.Integer(string="Sequence", default=10)
    
    # Relations
    treatment_plan_id = fields.Many2one('ehr_cdss.treatment.plan', string="Treatment Plan", required=True, ondelete='cascade')
    patient_id = fields.Many2one('ehr_cdss.patient.info', related='treatment_plan_id.patient_id', string="Patient", store=True)
    provider_id = fields.Many2one('ehr_cdss.provider', related='treatment_plan_id.provider_id', string="Provider", store=True)
    
    # Goal Content
    client_goal = fields.Text(string="Client's Goal", required=True, tracking=True, 
                             help="What the client reports their goal is, in their own words")
    
    clinical_goal_type = fields.Selection([
        ('symptom_reduction', 'Symptom Reduction'),
        ('skill_acquisition', 'Skill Acquisition'),
        ('coping', 'Learn/improve coping'),
        ('health', 'Improve health'),
        ('reduce_behaviors', 'Reduce ineffective behaviors'),
        ('maintain_gains', 'Maintain previous gains'),
        ('other', 'Other'),
    ], string="Clinical Goal Type", required=True, tracking=True)
    clinical_goal_other = fields.Char(string="Other Clinical Goal")
    
    # Objectives
    objective_ids = fields.One2many('ehr_cdss.objective', 'goal_id', string="Objectives/Short-term Goals")
    
    # Progress Measurement
    progress_measure_ids = fields.Many2many('ehr_cdss.progress.measure', string="Progress Will Be Measured By")
    
    # Timeline
    estimated_completion_time = fields.Selection([
        ('two_weeks', 'Within the next 2 weeks or 2 visits'),
        ('one_month', 'Within the next month or 4 visits'),
        ('two_months', 'Within the next 2 months or 8 visits'),
        ('three_months', 'Within the next 3 months or 12 visits'),
    ], string="Estimated Time to Achieve Goal", tracking=True)
    
    start_date = fields.Date(string="Start Date", default=fields.Date.today)
    target_date = fields.Date(string="Target Date")
    completion_date = fields.Date(string="Completion Date")
    
    # Status
    state = fields.Selection([
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('achieved', 'Achieved'),
        ('discontinued', 'Discontinued'),
    ], string="Status", default='active', tracking=True)
    
    progress = fields.Float(string="Progress (%)", default=0.0)
    
    # Comments
    comments = fields.Text(string="Comments")
    discontinued_reason = fields.Text(string="Reason for Discontinuation")
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Goal ID must be unique!')
    ]
    
    @api.model
    def create(self, vals):
        """Generate unique goal ID"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('ehr_cdss.goal') or _('New')
        return super(Goal, self).create(vals)
    
    def action_mark_in_progress(self):
        """Mark goal as in progress"""
        return self.write({'state': 'in_progress'})
    
    def action_mark_achieved(self):
        """Mark goal as achieved"""
        return self.write({
            'state': 'achieved',
            'progress': 100.0,
            'completion_date': fields.Date.today()
        })
    
    def action_discontinue(self):
        """Discontinue the goal"""
        return self.write({'state': 'discontinued'})


class Objective(models.Model):
    _name = 'ehr_cdss.objective'
    _description = 'Treatment Objective'
    _order = 'sequence, id'
    
    name = fields.Char(string="Objective ID", readonly=True, copy=False, default=lambda self: _('New'))
    sequence = fields.Integer(string="Sequence", default=10)
    
    # Relations
    goal_id = fields.Many2one('ehr_cdss.goal', string="Related Goal", required=True, ondelete='cascade')
    treatment_plan_id = fields.Many2one('ehr_cdss.treatment.plan', related='goal_id.treatment_plan_id', string="Treatment Plan", store=True)
    patient_id = fields.Many2one('ehr_cdss.patient.info', related='goal_id.patient_id', string="Patient", store=True)
    
    # Objective Content
    description = fields.Text(string="Objective Description", required=True, 
                             help="What are the measurable steps, behavior shifts, and/or skills needed to progress toward the goal")
    
    # Progress Measurement
    progress_measure_ids = fields.Many2many('ehr_cdss.progress.measure', string="Progress Will Be Measured By")
    
    # Timeline
    start_date = fields.Date(string="Start Date", default=fields.Date.today)
    target_date = fields.Date(string="Target Date")
    completion_date = fields.Date(string="Completion Date")
    
    # Status
    state = fields.Selection([
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('achieved', 'Achieved'),
        ('discontinued', 'Discontinued'),
    ], string="Status", default='active')
    
    progress = fields.Float(string="Progress (%)", default=0.0)
    
    # Comments
    comments = fields.Text(string="Comments")
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Objective ID must be unique!')
    ]
    
    @api.model
    def create(self, vals):
        """Generate unique objective ID"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('ehr_cdss.objective') or _('New')
        return super(Objective, self).create(vals)
    
    def action_mark_in_progress(self):
        """Mark objective as in progress"""
        return self.write({'state': 'in_progress'})
    
    def action_mark_achieved(self):
        """Mark objective as achieved"""
        return self.write({
            'state': 'achieved',
            'progress': 100.0,
            'completion_date': fields.Date.today()
        })
    
    def action_discontinue(self):
        """Discontinue the objective"""
        return self.write({'state': 'discontinued'})


class ProgressMeasure(models.Model):
    _name = 'ehr_cdss.progress.measure'
    _description = 'Progress Measurement Method'
    
    name = fields.Char(string="Measure Name", required=True)
    description = fields.Text(string="Description")
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Measure name must be unique!')
    ]
