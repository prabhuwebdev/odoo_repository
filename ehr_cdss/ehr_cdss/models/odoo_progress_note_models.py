# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import random
import string

class CPTCodesMaster(models.Model):
    _name = 'ehr_cdss.medical.cpt.code'
    _description = 'CPT Codes Master'
    _rec_name = 'code'
    
    code = fields.Char(string='CPT Code', required=True, index=True)
    name = fields.Char(string='Description', required=True)
    category = fields.Selection([
        ('evaluation', 'Evaluation and Management'),
        ('surgery', 'Surgery'),
        ('radiology', 'Radiology'),
        ('pathology', 'Pathology'),
        ('medicine', 'Medicine'),
        ('anesthesia', 'Anesthesia'),
        ('other', 'Other'),
    ], string='Category', default='other')
    standard_price = fields.Float(string='Standard Fee', digits=(10, 2))
    is_active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')
    
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'The CPT code must be unique!')
    ]
    
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, f"{record.code} - {record.name}"))
        return result


class ICD10CodesMaster(models.Model):
    _name = 'ehr_cdss.medical.icd10.code'
    _description = 'ICD-10 Codes Master'
    _rec_name = 'code'
    
    code = fields.Char(string='ICD-10 Code', required=True, index=True)
    name = fields.Char(string='Description', required=True)
    category = fields.Selection([
        ('infectious', 'Infectious Diseases'),
        ('neoplasms', 'Neoplasms'),
        ('endocrine', 'Endocrine and Metabolic Diseases'),
        ('mental', 'Mental and Behavioral Disorders'),
        ('nervous', 'Nervous System Diseases'),
        ('circulatory', 'Circulatory System Diseases'),
        ('respiratory', 'Respiratory System Diseases'),
        ('digestive', 'Digestive System Diseases'),
        ('musculoskeletal', 'Musculoskeletal System Diseases'),
        ('other', 'Other'),
    ], string='Category', default='other')
    is_active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'The ICD-10 code must be unique!')
    ]
    
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, f"{record.code} - {record.name}"))
        return result


class ProgressNote(models.Model):
    _name = 'ehr_cdss.medical.progress.note'
    _description = 'Medical Progress Note'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'
    
    name = fields.Char(string='Reference',  readonly=True, default=lambda self: self._generate_patient_id())
    patient_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True)
    provider_id = fields.Many2one('ehr_cdss.provider', string='Provider')
    user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
    show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')
    
    appointment_ids = fields.Many2one('ehr_cdss.appointment', string='Appointment')
    date = fields.Datetime(string='Date & Time', default=fields.Datetime.now,required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('signed', 'Signed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    # SUBJECTIVE Section - Child Form Items
    chief_complaint_ids = fields.One2many('ehr_cdss.medical.progress.note.chief.complaint', 
                                         'progress_note_id', string='Chief Complaints')
    chief_complaint_display = fields.Text(string='Chief Complaint Display', compute='_compute_chief_complaint_display')
    
    hpi_id = fields.Many2one('ehr_cdss.medical.progress.note.hpi', string='History of Present Illness')
    history_present_illness = fields.Text(related='hpi_id.description', string='HPI', readonly=True)
    
    pmh_id = fields.Many2one('ehr_cdss.medical.progress.note.pmh', string='Past Medical History')
    past_medical_history = fields.Text(related='pmh_id.description', string='PMH', readonly=True)
    
    family_history_id = fields.Many2one('ehr_cdss.medical.progress.note.family.history', string='Family History')
    family_history = fields.Text(related='family_history_id.description', string='Family History', readonly=True)
    
    social_history_id = fields.Many2one('ehr_cdss.medical.progress.note.social.history', string='Social History')
    social_history = fields.Text(related='social_history_id.description', string='Social History', readonly=True)
    
    # Review of Systems - Child Form/Sections
    ros_ids = fields.One2many('ehr_cdss.medical.progress.note.ros', 'progress_note_id', string='Review of Systems')
    
    # OBJECTIVE Section - Child Form Items
    vital_signs_id = fields.Many2one('ehr_cdss.medical.progress.note.vital.signs', string='Vital Signs')
    vital_signs_ids = fields.One2many('ehr_cdss.medical.progress.note.vital.signs', 'progress_note_id', string='Vital Signs')

    blood_pressure = fields.Char(related='vital_signs_id.blood_pressure', readonly=True)
    heart_rate = fields.Integer(related='vital_signs_id.heart_rate', readonly=True)
    respiratory_rate = fields.Integer(related='vital_signs_id.respiratory_rate', readonly=True)
    temperature = fields.Float(related='vital_signs_id.temperature', readonly=True)
    oxygen_saturation = fields.Float(related='vital_signs_id.oxygen_saturation', readonly=True)
    
    general_appearance_id = fields.Many2one('ehr_cdss.medical.progress.note.appearance', string='General Appearance')
    general_appearance = fields.Text(related='general_appearance_id.description', string='General Appearance', readonly=True)
    
    physical_exam_ids = fields.One2many('ehr_cdss.medical.progress.note.physical.exam', 
                                       'progress_note_id', string='Physical Examination')
    
    diagnostic_tests_id = fields.Many2one('ehr_cdss.medical.progress.note.diagnostic.tests', string='Diagnostic Tests')
    diagnostic_tests = fields.Text(related='diagnostic_tests_id.description', string='Diagnostic Tests', readonly=True)
    
    # ASSESSMENT Section
    primary_diagnosis_id = fields.Many2one('ehr_cdss.medical.progress.note.primary.diagnosis', string='Primary Diagnosis')
    primary_diagnosis = fields.Text(related='primary_diagnosis_id.description', string='Primary Diagnosis', readonly=True)
    
    # Diagnosis line items linked to ICD-10 codes
    diagnosis_ids = fields.One2many('ehr_cdss.medical.progress.note.diagnosis', 
                                   'progress_note_id', string='Diagnoses')
    
    # PLAN Section
    medication_ids = fields.One2many('ehr_cdss.medical.progress.note.medication', 
                                    'progress_note_id', string='Medications')
    
    lifestyle_modification_id = fields.Many2one('ehr_cdss.medical.progress.note.lifestyle', string='Lifestyle Modifications')
    lifestyle_modification_ids = fields.One2many( 'ehr_cdss.medical.progress.note.lifestyle', 'progress_note_id', string='Lifestyle Modifications')

    lifestyle_modifications = fields.Text(related='lifestyle_modification_id.description', 
                                          string='Lifestyle Modifications', readonly=True)
    
    # Treatment plan line items linked to CPT codes
    treatment_ids = fields.One2many('ehr_cdss.medical.progress.note.treatment', 
                                   'progress_note_id', string='Treatments')
    
    followup_id = fields.Many2one('ehr_cdss.medical.progress.note.followup', string='Follow-up')
    follow_up = fields.Text(related='followup_id.description', string='Follow-up Recommendations', readonly=True)
    next_appointment = fields.Date(related='followup_id.next_appointment', readonly=True)
    
    # Electronic signature fields
    signature_date = fields.Datetime(string='Signature Date')
    signature_user_id = fields.Many2one('res.users', string='Signed By')
    signature_image = fields.Binary(string='Signature Image')
    
    # Attachment documents
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    
    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'Progress Notes -' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    @api.depends('chief_complaint_ids', 'chief_complaint_ids.description')
    def _compute_chief_complaint_display(self):
        for record in self:
            complaints = []
            for complaint in record.chief_complaint_ids:
                complaints.append(complaint.description)
            record.chief_complaint_display = '\n'.join(complaints) if complaints else ''
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_sign(self):
        self.write({
            'state': 'signed',
            'signature_date': fields.Datetime.now(),
            'signature_user_id': self.env.user.id,
        })
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
    
    def action_open_chief_complaint_form(self):
        return {
            'name': _('Add Chief Complaint'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.chief.complaint',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_hpi_form(self):
        return {
            'name': _('History of Present Illness'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.hpi',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_pmh_form(self):
        return {
            'name': _('Past Medical History'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.pmh',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_family_history_form(self):
        return {
            'name': _('Family History'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.family.history',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_social_history_form(self):
        return {
            'name': _('Social History'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.social.history',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_ros_form(self):
        return {
            'name': _('Review of Systems'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.ros',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_vital_signs_form(self):
        return {
            'name': _('Vital Signs'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.vital.signs',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_general_appearance_form(self):
        return {
            'name': _('General Appearance'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.appearance',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_physical_exam_form(self):
        return {
            'name': _('Physical Examination'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.physical.exam',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_diagnostic_tests_form(self):
        return {
            'name': _('Diagnostic Tests'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.diagnostic.tests',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_primary_diagnosis_form(self):
        return {
            'name': _('Primary Diagnosis'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.primary.diagnosis',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_diagnosis_form(self):
        return {
            'name': _('Add Diagnosis'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.diagnosis',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_medication_form(self):
        return {
            'name': _('Add Medication'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.medication',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_lifestyle_form(self):
        return {
            'name': _('Lifestyle Modifications'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.lifestyle',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_treatment_form(self):
        return {
            'name': _('Add Treatment'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.treatment',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
    
    def action_open_followup_form(self):
        return {
            'name': _('Follow-up Recommendations'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.progress.note.followup',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_progress_note_id': self.id},
        }
        

    @api.depends_context('from_patient_form')
    def _compute_show_back_button(self):
        for rec in self:
            print("rec: ",rec)
            rec.show_back_button = self._context.get('from_patient_form', False)
    
    # def action_back_to_patient(self):
    #     """ Redirect back to the Patient form """
    #     print("patient_id: ",self.patient_id.id)
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'ehr_cdss.appointment',
    #         'view_mode': 'form',
    #         'res_id': self.patient_id.id,  # Open the related patient record
    #         'target': 'current',
    #     }
    
    def action_back_to_patient(self):
        """ Redirect back to the Patient form """
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        appointment_ids = self.env['ehr_cdss.appointment'].search([('patient_id', '=', record_id)], limit=1)
        print("self Tage",self.appointment_ids.id,self.patient_id.id)
        print("appointment_ids: ",appointment_ids)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.appointment',
            'view_mode': 'form',
            'res_id': appointment_ids.id,  # Open the related patient record
            'target': 'current',
        }
    #  def action_(self):
    #     # Assuming 'self' is a record for a person or patient.
    #     record_id = self.patient_id.id  # Get the ID of the current record (person)
    #     progress_notes = self.env['ehr_cdss.medical.history'].search([('patient_id', '=', record_id)], limit=1)
        
    #     if not progress_notes:
    #         # Handle case where no medical history exists for the patient
    #         progress_notes = self.env['ehr_cdss.medical.history'].create({
    #             'patient_id': record_id,
    #             'user_id': self.env.user.id,  # Associate the current user who is creating the record
    #         })
    #         # raise UserError("No medical history record found for this patient.")
    #     print("record_id",record_id)
    #     return { 
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'ehr_cdss.medical.history',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'res_id': progress_notes.id,  # Pass the record ID of the person to be displayed
    #         'target': 'current',  # Open in the same window or use 'new' for a popup
    #         'context': {'from_patient_form': True},  # ✅ pass context flag

    #         'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
    #     }
        
    def action_print_report(self):
        return self.env.ref('ehr_cdss.medical_progress_notes.action_report_progress_note').report_action(self)


# Subjective Section Models
class ProgressNoteChiefComplaint(models.Model):
    _name = 'ehr_cdss.medical.progress.note.chief.complaint'
    _description = 'Progress Note Chief Complaint'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', 
                                       required=True, ondelete='cascade')
    description = fields.Text(string='Chief Complaint', required=True)
    sequence = fields.Integer(string='Sequence', default=10)


class ProgressNoteHPI(models.Model):
    _name = 'ehr_cdss.medical.progress.note.hpi'
    _description = 'Progress Note History of Present Illness'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    description = fields.Text(string='History of Present Illness', required=True)
    onset = fields.Char(string='Onset')
    duration = fields.Char(string='Duration')
    location = fields.Char(string='Location')
    severity = fields.Selection([
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ], string='Severity')
    characteristics = fields.Text(string='Characteristics')
    aggravating_factors = fields.Text(string='Aggravating Factors')
    relieving_factors = fields.Text(string='Relieving Factors')
    treatment_response = fields.Text(string='Response to Treatment')
    recent_changes = fields.Text(string='Recent Changes')


class ProgressNotePMH(models.Model):
    _name = 'ehr_cdss.medical.progress.note.pmh'
    _description = 'Progress Note Past Medical History'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    description = fields.Text(string='Past Medical History', required=True)
    medical_history = fields.Text(string='Medical History')
    surgical_history = fields.Text(string='Surgical History')
    psychiatric_history = fields.Text(string='Psychiatric History')
    current_medications = fields.Text(string='Current Medications')
    allergies = fields.Text(string='Allergies')


class ProgressNoteFamilyHistory(models.Model):
    _name = 'ehr_cdss.medical.progress.note.family.history'
    _description = 'Progress Note Family History'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    description = fields.Text(string='Family History', required=True)


class ProgressNoteSocialHistory(models.Model):
    _name = 'ehr_cdss.medical.progress.note.social.history'
    _description = 'Progress Note Social History'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    description = fields.Text(string='Social History', required=True)
    smoking = fields.Selection([
        ('never', 'Never Smoker'),
        ('former', 'Former Smoker'),
        ('current', 'Current Smoker')
    ], string='Smoking Status')
    alcohol_use = fields.Selection([
        ('none', 'None'),
        ('occasional', 'Occasional'),
        ('moderate', 'Moderate'),
        ('heavy', 'Heavy')
    ], string='Alcohol Use')
    drug_use = fields.Text(string='Drug Use')
    occupation = fields.Char(string='Occupation')
    exercise = fields.Text(string='Exercise')


class ProgressNoteROS(models.Model):
    _name = 'ehr_cdss.medical.progress.note.ros'
    _description = 'Progress Note Review of Systems'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    system = fields.Selection([
        ('cardiovascular', 'Cardiovascular'),
        ('pulmonary', 'Pulmonary'),
        ('gastrointestinal', 'Gastrointestinal'),
        ('musculoskeletal', 'Musculoskeletal'),
        ('neurological', 'Neurological'),
        ('genitourinary', 'Genitourinary/Pelvic'),
        ('integumentary', 'Integumentary'),
        ('mental', 'Mental Status and Behavioral'),
        ('other', 'Other')
    ], string='System', required=True)
    findings = fields.Text(string='Findings', required=True)
    sequence = fields.Integer(string='Sequence', default=10)


# Objective Section Models
class ProgressNoteVitalSigns(models.Model):
    _name = 'ehr_cdss.medical.progress.note.vital.signs'
    _description = 'Progress Note Vital Signs'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    blood_pressure = fields.Char(string='Blood Pressure', help="Format: 120/80 mmHg")
    heart_rate = fields.Integer(string='Heart Rate', help="Beats per minute")
    respiratory_rate = fields.Integer(string='Respiratory Rate', help="Breaths per minute")
    temperature = fields.Float(string='Temperature', help="In degrees Fahrenheit")
    oxygen_saturation = fields.Float(string='Oxygen Saturation', help="Percentage")
    pain_score = fields.Integer(string='Pain Score', help="0-10 scale")
    height = fields.Float(string='Height', help="In inches or centimeters")
    weight = fields.Float(string='Weight', help="In pounds or kilograms")
    bmi = fields.Float(string='BMI', compute='_compute_bmi', store=True)
    notes = fields.Text(string='Additional Notes')
    date = fields.Date(string='Date')

    
    @api.depends('height', 'weight')
    def _compute_bmi(self):
        for record in self:
            if record.height and record.weight and record.height > 0:
                # Simple BMI calculation (assuming weight in kg and height in meters)
                # Adjust calculation based on your units
                record.bmi = record.weight / ((record.height / 100) ** 2)
            else:
                record.bmi = 0


class ProgressNoteAppearance(models.Model):
    _name = 'ehr_cdss.medical.progress.note.appearance'
    _description = 'Progress Note General Appearance'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    description = fields.Text(string='General Appearance', required=True)


class ProgressNotePhysicalExam(models.Model):
    _name = 'ehr_cdss.medical.progress.note.physical.exam'
    _description = 'Progress Note Physical Examination'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    system = fields.Selection([
        ('heent', 'HEENT'),
        ('cardiovascular', 'Cardiovascular'),
        ('respiratory', 'Respiratory'),
        ('gastrointestinal', 'Gastrointestinal'),
        ('musculoskeletal', 'Musculoskeletal'),
        ('neurological', 'Neurological'),
        ('genitourinary', 'Genitourinary'),
        ('skin', 'Skin'),
        ('lymphatic', 'Lymphatic'),
        ('psychiatric', 'Psychiatric'),
        ('other', 'Other')
    ], string='Body System', required=True)
    findings = fields.Text(string='Findings', required=True)
    sequence = fields.Integer(string='Sequence', default=10)


class ProgressNoteDiagnosticTests(models.Model):
    _name = 'ehr_cdss.medical.progress.note.diagnostic.tests'
    _description = 'Progress Note Diagnostic Tests'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    description = fields.Text(string='Diagnostic Tests and Imaging', required=True)


# Assessment Section Models
class ProgressNotePrimaryDiagnosis(models.Model):
    _name = 'ehr_cdss.medical.progress.note.primary.diagnosis'
    _description = 'Progress Note Primary Diagnosis'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    description = fields.Text(string='Primary Diagnosis', required=True)


class ProgressNoteDiagnosis(models.Model):
    _name = 'ehr_cdss.medical.progress.note.diagnosis'
    _description = 'Progress Note Diagnosis Lines'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', 
                                       required=True, ondelete='cascade')
    cd_code = fields.Char(string='CPT Code')
    cp_name = fields.Char(string='CPT Name')
    unit = fields.Char(string='Unit')
    modifier = fields.Char(string='Modifier')
    
    icd10_id = fields.Many2one('ehr_cdss.medical.icd10.code', string='ICD-10 Code', 
                              required=True, domain=[('is_active', '=', True)])
    name = fields.Char(string='Diagnosis Name', related='icd10_id.name', store=True, readonly=True)
    notes = fields.Text(string='Diagnosis Notes')
    sequence = fields.Integer(string='Sequence', default=10)
    is_primary = fields.Boolean(string='Primary Diagnosis', default=False)
    
    @api.onchange('is_primary')
    def _onchange_is_primary(self):
        if self.is_primary:
            # Ensure only one primary diagnosis per progress note
            other_primary = self.search([
                ('progress_note_id', '=', self.progress_note_id.id),
                ('is_primary', '=', True),
                ('id', '!=', self._origin.id)
            ])
            if other_primary:
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _('Only one primary diagnosis is allowed per progress note.')
                    }
                }


# Plan Section Models
class ProgressNoteMedication(models.Model):
    _name = 'ehr_cdss.medical.progress.note.medication'
    _description = 'Progress Note Medication Lines'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', 
                                      required=True, ondelete='cascade')
    name = fields.Char(string='Medication Name', required=True)
    dosage = fields.Char(string='Dosage', required=True)
    route = fields.Selection([
        ('oral', 'Oral'),
        ('iv', 'Intravenous'),
        ('im', 'Intramuscular'),
        ('sc', 'Subcutaneous'),
        ('topical', 'Topical'),
        ('inhalation', 'Inhalation'),
        ('other', 'Other')
    ], string='Route', required=True)
    frequency = fields.Char(string='Frequency', required=True)
    duration = fields.Char(string='Duration')
    cd_code = fields.Char(string='CPT Code')
    cp_name = fields.Char(string='CPT Name')
    unit = fields.Char(string='Unit')
    modifier = fields.Char(string='Modifier')
    
    notes = fields.Text(string='Instructions/Notes')
    sequence = fields.Integer(string='Sequence', default=10)


class ProgressNoteLifestyle(models.Model):
    _name = 'ehr_cdss.medical.progress.note.lifestyle'
    _description = 'Progress Note Lifestyle Modifications'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    description = fields.Text(string='Lifestyle Modifications', required=True)


class ProgressNoteTreatment(models.Model):
    _name = 'ehr_cdss.medical.progress.note.treatment'
    _description = 'Progress Note Treatment Lines'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', 
                                      required=True, ondelete='cascade')
    cpt_id = fields.Many2one('ehr_cdss.medical.cpt.code', string='CPT Code', 
                           required=True, domain=[('is_active', '=', True)])
    name = fields.Char(string='Treatment Name', related='cpt_id.name', store=True, readonly=True)
    notes = fields.Text(string='Treatment Notes')
    cd_code = fields.Char(string='CPT Code')
    cp_name = fields.Char(string='CPT Name')
    unit = fields.Char(string='Unit')
    modifier = fields.Char(string='Modifier')
    sequence = fields.Integer(string='Sequence', default=10)
    price = fields.Float(string='Fee', digits=(10, 2))
    
    @api.onchange('cpt_id')
    def _onchange_cpt_id(self):
        if self.cpt_id:
            self.price = self.cpt_id.standard_price


class ProgressNoteFollowup(models.Model):
    _name = 'ehr_cdss.medical.progress.note.followup'
    _description = 'Progress Note Follow-up Recommendations'
    
    progress_note_id = fields.Many2one('ehr_cdss.medical.progress.note', string='Progress Note', required=True, ondelete='cascade')
    description = fields.Text(string='Follow-up Recommendations', required=True)
    next_appointment = fields.Date(string='Next Appointment')
    specialist_referral = fields.Boolean(string='Specialist Referral')
    referral_to = fields.Char(string='Refer To', help="Specialist or department for referral")
    referral_reason = fields.Text(string='Referral Reason')
    escalation_criteria = fields.Text(string='Criteria for Escalation')
