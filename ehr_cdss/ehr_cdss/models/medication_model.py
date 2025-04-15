# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import random
import string

class MedicationReconciliation(models.Model):
    _name = 'ehr_cdss.medical.medication.reconciliation'
    _description = 'Medication Reconciliation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_reconciliation desc, id desc'

    name = fields.Char(string='Reference', readonly=True, default=lambda self: self._generate_patient_id())
    patient_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True, tracking=True,)
    date_reconciliation = fields.Datetime(string='Reconciliation Date', default=fields.Datetime.now, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('verified', 'Verified'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    active = fields.Boolean(default=True)
    
    medication_line_ids = fields.One2many('ehr_cdss.medical.medication.line', 'reconciliation_id', 
                                          string='Medications')
    
    # pharmacy_id = fields.Many2one('res.partner', string='Pharmacy', domain=[('is_pharmacy', '=', True)])
    pharmacy_verification = fields.Boolean(string='Pharmacy Data Verification', default=False,
                                           help="Use electronic verification from pharmacy")
    pharmacy_verification_date = fields.Datetime(string='Verification Date')
    
    total_medications = fields.Integer(string='Total Medications', compute='_compute_medication_counts')
    total_verified = fields.Integer(string='Verified Medications', compute='_compute_medication_counts')
    total_discrepancies = fields.Integer(string='Discrepancies', compute='_compute_medication_counts')
    
    notes = fields.Text(string='Notes')
    practitioner_id = fields.Many2one('res.users', string='Healthcare Provider', 
                                     default=lambda self: self.env.user.id)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'Medication -' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    @api.depends('medication_line_ids', 'medication_line_ids.is_verified', 'medication_line_ids.has_discrepancy')
    def _compute_medication_counts(self):
        for rec in self:
            rec.total_medications = len(rec.medication_line_ids)
            rec.total_verified = len(rec.medication_line_ids.filtered(lambda m: m.is_verified))
            rec.total_discrepancies = len(rec.medication_line_ids.filtered(lambda m: m.has_discrepancy))
    
    def action_verify_with_pharmacy(self):
        """Attempt electronic verification with pharmacy"""
        for rec in self:
            if not rec.pharmacy_id:
                raise UserError(_("Please select a pharmacy for verification."))
            
            # Placeholder for API integration with pharmacy systems
            # In a real implementation, this would connect to pharmacy API
            
            # For demo purposes, we'll just update the status
            rec.pharmacy_verification = True
            rec.pharmacy_verification_date = fields.Datetime.now()
            rec.state = 'in_progress'
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Verification Request'),
                    'message': _('Verification request sent to %s') % rec.pharmacy_id.name,
                    'type': 'success',
                    'sticky': False,
                }
            }
    
    def action_complete_reconciliation(self):
        """Mark the reconciliation as completed"""
        for rec in self:
            if rec.total_discrepancies > 0:
                # Allow completion but show warning about discrepancies
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Warning'),
                        'message': _('There are %s discrepancies that have not been resolved. Are you sure you want to complete the reconciliation?') % rec.total_discrepancies,
                        'type': 'warning',
                        'sticky': True,
                        'next': {
                            'type': 'ir.actions.act_window',
                            'res_model': 'ehr_cdss.medical.medication.reconciliation.confirm',
                            'view_mode': 'form',
                            'target': 'new',
                            'context': {'default_reconciliation_id': rec.id}
                        }
                    }
                }
            else:
                rec.state = 'completed'
                
    def action_cancel(self):
        """Cancel the reconciliation"""
        for rec in self:
            rec.state = 'cancelled'
    
    def action_reset_to_draft(self):
        """Reset to draft state"""
        for rec in self:
            rec.state = 'draft'
            rec.pharmacy_verification = False
            rec.pharmacy_verification_date = False


class MedicationLine(models.Model):
    _name = 'ehr_cdss.medical.medication.line'
    _description = 'Medication Line'
    
    reconciliation_id = fields.Many2one('ehr_cdss.medical.medication.reconciliation', string='Reconciliation', 
                                        ondelete='cascade')
    medication_id = fields.Many2one('ehr_cdss.medical.medication', string='Medication', required=True)
    medication_type = fields.Selection([
        ('prescription', 'Prescription'),
        ('otc', 'Over-the-Counter'),
        ('supplement', 'Supplement')
    ], string='Type', required=True)
    dosage = fields.Char(string='Dosage', required=True)
    frequency = fields.Char(string='Frequency')
    route = fields.Selection([
        ('oral', 'Oral'),
        ('topical', 'Topical'),
        ('injection', 'Injection'),
        ('inhalation', 'Inhalation'),
        ('other', 'Other')
    ], string='Route')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    is_active = fields.Boolean(string='Active', default=True)
    
    # Verification fields
    pharmacy_data = fields.Char(string='Pharmacy Data')
    is_verified = fields.Boolean(string='Verified', default=False)
    has_discrepancy = fields.Boolean(string='Has Discrepancy', compute='_compute_discrepancy', store=True)
    discrepancy_notes = fields.Text(string='Discrepancy Notes')
    
    @api.depends('pharmacy_data', 'dosage', 'is_verified')
    def _compute_discrepancy(self):
        for rec in self:
            if rec.is_verified and rec.pharmacy_data and rec.pharmacy_data != rec.dosage:
                rec.has_discrepancy = True
            else:
                rec.has_discrepancy = False
    
    @api.onchange('medication_id')
    def _onchange_medication(self):
        if self.medication_id:
            self.medication_type = self.medication_id.medication_type
            
    def action_verify(self):
        """Mark medication as verified"""
        for rec in self:
            rec.is_verified = True
    
    def action_resolve_discrepancy(self):
        """Open wizard to resolve discrepancy"""
        self.ensure_one()
        return {
            'name': _('Resolve Medication Discrepancy'),
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.medication.discrepancy.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_medication_line_id': self.id}
        }


class Medication(models.Model):
    _name = 'ehr_cdss.medical.medication'
    _description = 'Medication'
    _rec_name = 'patient_id'
    
    patient_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True, tracking=True,)
    user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
    name = fields.Char(string='Medication Name')
    active_ingredient = fields.Char(string='Active Ingredient')
    medication_type = fields.Selection([
        ('prescription', 'Prescription'),
        ('otc', 'Over-the-Counter'),
        ('supplement', 'Supplement'),
        ('add_the_dosage', 'Add the dosage')        
    ], string='Type',)
    unit = fields.Char(string='Unit', )
    cb_code = fields.Char(string='CB Code', )
    
    frequency = fields.Char(string='Frequency')
    route = fields.Selection([
        ('oral', 'Oral'),
        ('topical', 'Topical'),
        ('injection', 'Injection'),
        ('inhalation', 'Inhalation'),
        ('other', 'Other')
    ], string='Route')

    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)
    form_date = fields.Date(string='Form Date')
    to_date = fields.Date(string='To Date')
    show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Medication name must be unique!')
    ]
    
    

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            # Assuming patient_name is a field in 'ehr_cdss.patient.info'
            self.name = self.patient_id.full_name
        else:
            self.name = ''
            
    @api.depends_context('from_patient_form')
    def _compute_show_back_button(self):
        for rec in self:
            print("rec: ",rec)
            rec.show_back_button = self._context.get('from_patient_form', False)
            
    def action_back_to_patient(self):
        """ Redirect back to the Patient form """
        print("self Tage",self)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.info',
            'view_mode': 'form',
            'res_id': self.patient_id.id,  # Open the related patient record
            'target': 'current',
        }
        
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
        
        
    def open_insurance_record(self):
        self.ensure_one()
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
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
        self.ensure_one()
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
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
        
    def dummy_action(self):
        pass  # Do nothing

class MedicationDiscrepancyWizard(models.TransientModel):
    _name = 'ehr_cdss.medical.medication.discrepancy.wizard'
    _description = 'Medication Discrepancy Resolution Wizard'
    
    medication_line_id = fields.Many2one('ehr_cdss.medical.medication.line', string='Medication')
    medication_name = fields.Char(related='medication_line_id.medication_id.name', readonly=True)
    current_dosage = fields.Char(related='medication_line_id.dosage', readonly=True)
    pharmacy_data = fields.Char(related='medication_line_id.pharmacy_data', readonly=True)
    resolution = fields.Selection([
        ('keep_current', 'Keep Current Dosage'),
        ('use_pharmacy', 'Use Pharmacy Data'),
        ('update_both', 'Update to New Value')
    ], string='Resolution', required=True)
    new_dosage = fields.Char(string='New Dosage')
    notes = fields.Text(string='Resolution Notes')
    
    def action_resolve(self):
        """Apply the resolution"""
        for wizard in self:
            if wizard.resolution == 'keep_current':
                # Keep current, just mark as verified
                wizard.medication_line_id.is_verified = True
                wizard.medication_line_id.discrepancy_notes = wizard.notes
            elif wizard.resolution == 'use_pharmacy':
                # Update to pharmacy data
                wizard.medication_line_id.dosage = wizard.pharmacy_data
                wizard.medication_line_id.is_verified = True
                wizard.medication_line_id.discrepancy_notes = wizard.notes
            elif wizard.resolution == 'update_both':
                # Update to new value
                if not wizard.new_dosage:
                    raise UserError(_("Please provide a new dosage value."))
                wizard.medication_line_id.dosage = wizard.new_dosage
                wizard.medication_line_id.is_verified = True
                wizard.medication_line_id.discrepancy_notes = wizard.notes
                
        return {'type': 'ir.actions.act_window_close'}


class MedicationReconciliationConfirm(models.TransientModel):
    _name = 'ehr_cdss.medical.medication.reconciliation.confirm'
    _description = 'Confirm Medication Reconciliation'
    
    reconciliation_id = fields.Many2one('ehr_cdss.medical.medication.reconciliation', string='Reconciliation')
    confirmation_note = fields.Text(string='Confirmation Note', required=True,
                                   default="I confirm that I have reviewed all discrepancies and approve completing the medication reconciliation.")
    # active = fields.Boolean(default=True)
    def action_confirm(self):
        """Confirm and complete the reconciliation"""
        self.ensure_one()
        if self.reconciliation_id:
            self.reconciliation_id.state = 'completed'
            return {'type': 'ir.actions.act_window_close'}
