from odoo import models, fields, api
from datetime import datetime


class AllergyType(models.Model):
    _name = 'ehr_cdss.medical.allergy.type'
    _description = 'Allergy Type'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Allergy type name must be unique!')
    ]


class AllergySeverity(models.Model):
    _name = 'ehr_cdss.medical.allergy.severity'
    _description = 'Allergy Severity'
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Severity name must be unique!')
    ]


class AllergyCategory(models.Model):
    _name = 'ehr_cdss.medical.allergy.category'
    _description = 'Allergy Category'
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Category name must be unique!')
    ]


class PatientAllergy(models.Model):
    _name = 'ehr_cdss.medical.patient.allergy'
    _description = 'Patient Allergies'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'patient_id'  # or whatever field you want shown
    
    patient_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True, tracking=True)
    name = fields.Char(string='Allergy Name', tracking=True)
    user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
    
    category_id = fields.Many2one('ehr_cdss.medical.allergy.category', string='Category', tracking=True,
                                help="Category of allergy - Medication, Food, or Environmental")
    type_id = fields.Many2one('ehr_cdss.medical.allergy.type', string='Type', tracking=True,help="Specific type of the allergy")
    severity_id = fields.Many2one('ehr_cdss.medical.allergy.severity', string='Severity', tracking=True)
    
    reaction = fields.Text(string='Reaction', tracking=True,
                        help="Description of allergic reaction")
    first_observed = fields.Date(string='First Observed', tracking=True)
    is_intolerance = fields.Boolean(string='Is Intolerance', tracking=True,
                                 help="Check if this is an intolerance rather than an allergy")
    
    notes = fields.Text(string='Notes', tracking=True)
    allergy_band_applied = fields.Boolean(string='Allergy Band Applied', tracking=True)
    
    active = fields.Boolean(default=True, string='Active', tracking=True)
    verified = fields.Boolean(string='Verified in EMR', tracking=True,
                           help="Allergy has been verified against the EMR system")
    verified_by = fields.Many2one('res.users', string='Verified By', tracking=True)
    verification_date = fields.Datetime(string='Verification Date', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('verified', 'Verified'),
        ('inactive', 'Inactive'),
    ], string='Status', default='draft', tracking=True)
    show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')

    @api.model
    def create(self, vals):
        record = super(PatientAllergy, self).create(vals)
        # When creating a new allergy record, automatically create an activity for verification
        if record.patient_id:
            self.env['mail.activity'].create({
                'res_id': record.id,
                'res_model_id': self.env['ir.model'].search([('model', '=', 'ehr_cdss.medical.patient.allergy')], limit=1).id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': f'Verify {record.name} allergy in EMR',
                'note': f'Please verify this allergy against the EMR system for patient {record.patient_id.name}',
                'user_id': self.env.user.id,
                'date_deadline': fields.Date.context_today(self),
            })
        return record

    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_verify(self):
        self.write({
            'state': 'verified',
            'verified': True,
            'verified_by': self.env.user.id,
            'verification_date': fields.Datetime.now(),
        })
    
    def action_set_inactive(self):
        self.write({
            'state': 'inactive',
            'active': False
        })
    
    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
    
    def action_apply_allergy_band(self):
        self.write({'allergy_band_applied': True})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Allergy Band Applied',
                'message': f'Allergy band has been applied for {self.name}',
                'sticky': False,
                'type': 'success'
            }
        }
        
    @api.depends_context('from_patient_form')
    def _compute_show_back_button(self):
        for rec in self:
            print("rec: ",rec)
            rec.show_back_button = self._context.get('from_patient_form', False)
    
    def action_back_to_patient(self):
        """ Redirect back to the Patient form """
        print("self Tage",self)
        print("Medical History patient_id: ",self.patient_id)
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
        


class PatientAllergyBand(models.Model):
    _name = 'ehr_cdss.medical.patient.allergy.band'
    _description = 'Patient Allergy Band'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True, tracking=True)
    application_date = fields.Datetime(string='Application Date', default=fields.Datetime.now, required=True, tracking=True)
    applied_by = fields.Many2one('res.users', string='Applied By', default=lambda self: self.env.user.id, required=True, tracking=True)
    # allergy_ids = fields.Many2many('ehr_cdss.medical.patient.allergy', string='Allergies', tracking=True, 
    #                                help="List of allergies for this patient", table="ehr_cdss_patient_allergy_band_allergy_rel")
    
    allergy_ids = fields.Many2many('ehr_cdss.medical.patient.allergy', string='Allergies', tracking=True, relation='ehr_cdss_patient_allergy_band_rel')

    band_number = fields.Char(string='Band Number', tracking=True)
    notes = fields.Text(string='Notes', tracking=True)
    
    state = fields.Selection([
        ('applied', 'Applied'),
        ('removed', 'Removed'),
    ], string='Status', default='applied', tracking=True)
    
    removal_date = fields.Datetime(string='Removal Date', tracking=True)
    removed_by = fields.Many2one('res.users', string='Removed By', tracking=True)
    removal_reason = fields.Text(string='Removal Reason', tracking=True)
    
    def action_remove_band(self):
        return {
            'name': 'Remove Allergy Band',
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.allergy.band.removal.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_band_id': self.id,
                'default_patient_id': self.patient_id.id,
            }
        }

class Patient(models.Model):
    _inherit = 'ehr_cdss.patient.info'
    
    allergy_ids = fields.One2many('ehr_cdss.medical.patient.allergy', 'patient_id', string='Allergies')
    allergy_count = fields.Integer(compute='_compute_allergy_count', string='Allergy Count')
    has_critical_allergies = fields.Boolean(compute='_compute_has_critical_allergies', string='Has Critical Allergies', store=True)
    allergy_band_ids = fields.One2many('ehr_cdss.medical.patient.allergy.band', 'patient_id', string='Allergy Bands')
    current_allergy_band = fields.Many2one('ehr_cdss.medical.patient.allergy.band', compute='_compute_current_allergy_band', string='Current Allergy Band')
    
    @api.depends('allergy_ids')
    def _compute_allergy_count(self):
        for patient in self:
            patient.allergy_count = len(patient.allergy_ids.filtered(lambda a: a.active))
    
    @api.depends('allergy_ids', 'allergy_ids.severity_id', 'allergy_ids.active')
    def _compute_has_critical_allergies(self):
        critical_severity = self.env['ehr_cdss.medical.allergy.severity'].search([('name', 'in', ['Severe', 'Critical', 'Life-threatening'])])
        for patient in self:
            patient.has_critical_allergies = bool(patient.allergy_ids.filtered(lambda a: a.active and a.severity_id in critical_severity))
    
    @api.depends('allergy_band_ids', 'allergy_band_ids.state')
    def _compute_current_allergy_band(self):
        for patient in self:
            current_band = patient.allergy_band_ids.filtered(lambda b: b.state == 'applied')
            patient.current_allergy_band = current_band[0] if current_band else False
    
    def action_view_allergies(self):
        self.ensure_one()
        return {
            'name': 'Patient Allergies',
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.patient.allergy',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }
    
    def action_apply_allergy_band(self):
        self.ensure_one()
        return {
            'name': 'Apply Allergy Band',
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.allergy.band.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_allergy_ids': self.allergy_ids.filtered(lambda a: a.active).ids,
            }
        }
    
    def action_verify_emr_allergies(self):
        self.ensure_one()
        return {
            'name': 'Verify EMR Allergies',
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.medical.emr.allergy.verification.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
            }
        }
