# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class MedicalHistory(models.Model):
    _name = 'ehr_cdss.medical.history'
    _description = 'Patient Medical History'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_id'
    
    patient_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)

    date_recorded = fields.Date(string='Record Date', default=fields.Date.today(), tracking=True)
    notes = fields.Text(string='General Notes')
    active = fields.Boolean(default=True)
    
    # One-to-many relationships with specific medical history components
    hospitalization_ids = fields.One2many('ehr_cdss.medical.hospitalization', 'medical_history_id', 
                                        string='Hospitalizations')
    illness_ids = fields.One2many('ehr_cdss.medical.illness', 'medical_history_id', 
                                string='Major Illnesses')
    surgery_ids = fields.One2many('ehr_cdss.medical.surgery', 'medical_history_id', 
                                string='Surgeries')
    
    show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')
    
    
    _sql_constraints = [
        ('patient_unique', 'unique(patient_id)', 'A medical history record already exists for this patient!')
    ]
    
    def name_get(self):
        result = []
        for record in self:
            name = _('Medical History - %s') % (record.patient_id.name)
            result.append((record.id, name))
        return result
    
    def action_back_to_patient(self):
        """ Redirect back to the Patient form """
        print("patient_id: ",self.patient_id.id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.info',
            'view_mode': 'form',
            'res_id': self.patient_id.id,  # Open the related patient record
            'target': 'current',
        }
    
    
    @api.model
    def default_get(self, fields_list):
        res = super(MedicalHistory, self).default_get(fields_list)
        if self.env.context.get('from_patient_form'):
            print("Model functions")
            res['patient_id'] = self.env.context.get('default_patient_id') or self.env.context.get('active_id')
        return res
        
    @api.depends_context('from_patient_form')
    def _compute_show_back_button(self):
        for rec in self:
            print("rec: ",rec)
            rec.show_back_button = self._context.get('from_patient_form', False)
            
    
    
    def action_medical_history(self):
        # Assuming 'self' is a record for a person or patient.
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        medical_history = self.env['ehr_cdss.medical.history'].search([('patient_id', '=', record_id)], limit=1)
        
        if not medical_history:
            # Handle case where no medical history exists for the patient
            medical_history = self.env['ehr_cdss.medical.history'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        return { 
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.history',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': medical_history.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag

            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
    
    def action_family_history(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        family_history = self.env['ehr_cdss.medical.family.history'].search([('patient_id', '=', record_id)], limit=1)
        
        if not family_history:
            # Handle case where no medical history exists for the patient
            family_history = self.env['ehr_cdss.medical.family.history'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
            # raise UserError("No medical history record found for this patient.")
        print("record_id",record_id)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.family.history',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': family_history.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trig
        }
        
        
    def action_immunization_infectious_disease(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        immunization_id = self.env['ehr_cdss.patient.immunization.record'].search([('partner_id', '=', record_id)], limit=1)
        
        if not immunization_id:
            # Handle case where no medical history exists for the patient
            immunization_id = self.env['ehr_cdss.patient.immunization.record'].create({
                'partner_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.immunization.record',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': immunization_id.id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in the same window or use 'new' for a popup
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }

    
    def action_appointment(self):
        record_id = self.patient_id.id # Get the ID of the current record (person)
        appointment = self.env['ehr_cdss.appointment'].search([('patient_id', '=', record_id)], limit=1)
        
        if not appointment:
            # Handle case where no medical history exists for the patient
            appointment = self.env['ehr_cdss.appointment'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.appointment',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': appointment.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        
    def action_medical_patient_allergy(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].search([('patient_id', '=', record_id)], limit=1)
        
        if not patient_allergy:
            # Handle case where no medical history exists for the patient
            patient_allergy = self.env['ehr_cdss.medical.patient.allergy'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.patient.allergy',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': patient_allergy.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        

    def action_medication(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        medication = self.env['ehr_cdss.medical.medication'].search([('patient_id', '=', record_id)], limit=1)
        
        if not medication:
            # Handle case where no medical history exists for the patient
            medication = self.env['ehr_cdss.medical.medication'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.medication',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': medication.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'context': {'from_patient_form': True},  # ✅ pass context flag
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        
    def action_document(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        document = self.env['ehr_cdss.document'].search([('patient_id', '=', record_id)], limit=1)
        
        if not document:
            # Handle case where no medical history exists for the patient
            document = self.env['ehr_cdss.document'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,  # Associate the current user who is creating the record
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.document',  # Replace with actual model
            'view_mode': 'kanban,form',
            'view_type': 'form',
            'res_id': document.id,  # Pass the record ID of the person to be displayed
            'target': 'current',
            'domain': [('patient_id', '=', record_id)],  # Filter documents by patient
            'context': {'search_default_filter_by_patient': 1, 'default_patient_id': record_id},
        }
        
        
    def open_insurance_record(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        self.ensure_one()
        insurance = self.env['ehr_cdss.patient.insurance_patient'].search([
            ('patient_id', '=', record_id)
        ], limit=1)

        if not insurance:
            insurance = self.env['ehr_cdss.patient.insurance_patient'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.insurance_patient',
            'view_mode': 'form',
            'res_id': insurance.id,
            'target': 'current',
            'context': {'from_patient_form': True},
        }
    
    def open_allergy_record(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        self.ensure_one()
        allergy = self.env['ehr_cdss.patient.allergy'].search([
            ('patient_id', '=', record_id)
        ], limit=1)

        if not allergy:
            allergy = self.env['ehr_cdss.patient.allergy'].create({
                'patient_id': record_id,
                'user_id': self.env.user.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.allergy',
            'view_mode': 'form',
            'res_id': allergy.id,
            'target': 'current',
            'context': {'from_patient_form': True},
        }
    
    def dummy_action(self):
        pass  # Do nothing



class MedicalHospitalization(models.Model):
    _name = 'ehr_cdss.medical.hospitalization'
    _description = 'Patient Hospitalization Record'
    _order = 'admission_date desc'
    
    medical_history_id = fields.Many2one('ehr_cdss.medical.history', string='Medical History', required=True, ondelete='cascade')
    patient_id = fields.Many2one(related='medical_history_id.patient_id', store=True, readonly=True)
    hospital = fields.Char(string='Hospital Name', required=True)
    admission_date = fields.Date(string='Admission Date', required=True)
    discharge_date = fields.Date(string='Discharge Date')
    reason = fields.Char(string='Reason for Admission', required=True)
    diagnosis = fields.Text(string='Diagnosis')
    treatment = fields.Text(string='Treatment Received')
    attending_physician = fields.Char(string='Attending Physician')
    documents = fields.Binary(string='Medical Documents')
    notes = fields.Text(string='Notes')
    
    @api.constrains('admission_date', 'discharge_date')
    def _check_dates(self):
        for record in self:
            if record.discharge_date and record.admission_date > record.discharge_date:
                raise ValidationError(_("Discharge date cannot be earlier than admission date."))


class MedicalIllness(models.Model):
    _name = 'ehr_cdss.medical.illness'
    _description = 'Major Illness Record'
    _order = 'diagnosis_date desc'
    
    medical_history_id = fields.Many2one('ehr_cdss.medical.history', string='Medical History', required=True, ondelete='cascade')
    patient_id = fields.Many2one(related='medical_history_id.patient_id', store=True, readonly=True)
    name = fields.Char(string='Illness Name', required=True)
    diagnosis_date = fields.Date(string='Date of Diagnosis')
    state = fields.Selection([
        ('active', 'Active'),
        ('managed', 'Managed'),
        ('resolved', 'Resolved')
    ], string='Status', default='active')
    severity = fields.Selection([
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ], string='Severity')
    treating_physician = fields.Char(string='Treating Physician')
    treatment = fields.Text(string='Treatment Plan')
    notes = fields.Text(string='Notes')


class MedicalSurgery(models.Model):
    _name = 'ehr_cdss.medical.surgery'
    _description = 'Surgery Record'
    _order = 'date desc'
    
    medical_history_id = fields.Many2one('ehr_cdss.medical.history', string='Medical History', required=True, ondelete='cascade')
    patient_id = fields.Many2one(related='medical_history_id.patient_id', store=True, readonly=True)
    name = fields.Char(string='Surgery Name', required=True)
    date = fields.Date(string='Surgery Date', required=True)
    surgeon = fields.Char(string='Surgeon Name')
    hospital = fields.Char(string='Hospital')
    reason = fields.Text(string='Reason for Surgery')
    outcome = fields.Selection([
        ('successful', 'Successful'),
        ('complications', 'With Complications'),
        ('failed', 'Failed')
    ], string='Outcome', default='successful')
    complications = fields.Text(string='Complications')
    notes = fields.Text(string='Notes')
    documents = fields.Binary(string='Surgery Documents')