from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random
import string
import base64
import logging

_logger = logging.getLogger(__name__)  # ✅ Add this to define _logger


class Document(models.Model):
    _name = 'ehr_cdss.document'
    _description = 'Medical Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'document_number'  # or whatever field you want shown
    
    document_number = fields.Char(string="Document Number", required=True, readonly=True, copy=False, default=lambda self: self._generate_patient_id())
    name = fields.Char(string="Document Name",  tracking=True)
    user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
    # Document Content
    file = fields.Binary(string="Document File", attachment=True, )
    file_name = fields.Char(string="File Name")
    file_type = fields.Selection([
        ('pdf', 'PDF'),
        ('docx', 'Word Document'),
        ('xlsx', 'Excel Spreadsheet'),
        ('jpg', 'JPEG Image'),
        ('png', 'PNG Image'),
        ('txt', 'Text File'),
        ('csv', 'CSV File'),
        ('other', 'Other'),
    ], string="File Type", compute="_compute_file_type", store=True)
    file_size = fields.Integer(string="File Size (KB)", compute="_compute_file_size", store=True)
    content_text = fields.Text(string="Document Content", help="Extracted text content if available")
    
    # Document Type
    document_type = fields.Selection([
        ('soap_note', 'SOAP Note'),
        ('progress_note', 'Progress Note'),
        ('initial_assessment', 'Initial Assessment'),
        ('treatment_plan', 'Treatment Plan'),
        ('safety_plan', 'Safety Plan'),
        ('discharge_summary', 'Discharge Summary'),
        ('clinical_review', 'Clinical Review Update'),
        ('referral', 'Referral'),
        ('consent_form', 'Consent Form'),
        ('lab_result', 'Lab Result'),
        ('imaging_result', 'Imaging Result'),
        ('prescription', 'Prescription'),
        ('insurance', 'Insurance Document'),
        ('correspondence', 'Correspondence'),
        ('other', 'Other'),
    ], string="Document Type", tracking=True)
    
    document_template_id = fields.Many2one('ehr_cdss.document.template', string="Document Template")
    is_template_generated = fields.Boolean(string="Generated from Template")
    
    # Relationships
    patient_id = fields.Many2one('ehr_cdss.patient.info', string="Patient", tracking=True)
    provider_id = fields.Many2one('ehr_cdss.provider', string="Provider", tracking=True)
    organization_id = fields.Many2one('ehr_cdss.organization', string="Organization")
    appointment_id = fields.Many2one('ehr_cdss.appointment', string="Related Appointment")
    medical_record_id = fields.Many2one('ehr_cdss.medical.record', string="Medical Record")
    
    # Document Metadata
    document_date = fields.Date(string="Document Date", default=fields.Date.today, tracking=True)
    tags = fields.Many2many('ehr_cdss.document.tag', string="Tags")
    description = fields.Text(string="Description")
    is_signed = fields.Boolean(string="Is Signed", default=False, tracking=True)
    # signed_by = fields.Many2one('ehr_cdss.provider', string="Signed By")
    signature_date = fields.Datetime(string="Signature Date")
    requires_patient_signature = fields.Boolean(string="Requires Patient Signature")
    patient_signed = fields.Boolean(string="Patient Signed", tracking=True)
    patient_signature_date = fields.Datetime(string="Patient Signature Date")
    
    # Version Control
    is_latest_version = fields.Boolean(string="Latest Version", default=True)
    version_number = fields.Integer(string="Version", default=1)
    parent_document_id = fields.Many2one('ehr_cdss.document', string="Previous Version")
    child_document_ids = fields.One2many('ehr_cdss.document', 'parent_document_id', string="Next Versions")
    
    # Sharing and Access Control
    is_shared = fields.Boolean(string="Shared with Patient", default=False, tracking=True)
    shared_date = fields.Datetime(string="Share Date")
    access_level = fields.Selection([
        ('private', 'Private - Provider Only'),
        ('team', 'Team - Care Team Only'),
        ('patient', 'Patient - Patient Can View'),
        ('public', 'Public - All Authorized Users'),
    ], string="Access Level", default='private', tracking=True)
    
    # State
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_review', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('archived', 'Archived'),
    ], string="Status", default='draft', tracking=True)
    show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')

    
    _sql_constraints = [
        ('document_number_unique', 'UNIQUE(document_number)', 'Document Number must be unique!')
    ]
    
    # @api.model
    # def create(self, vals):
    #     """Generate unique document number"""
    #     if vals.get('document_number', _('New')) == _('New'):
    #         vals['document_number'] = self.env['ir.sequence'].next_by_code('ehr_cdss.document') or _('New')
    #     return super(Document, self).create(vals)
    
    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._compute_file_size()
        return record
    def write(self, vals):
        res = super().write(vals)
        if 'file' in vals:
            self._compute_file_size()
        return res

    def _generate_patient_id(self):
        """ Generate a unique Patient ID """
        return 'PT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    @api.depends_context('from_patient_form')
    def _compute_show_back_button(self):
        for rec in self:
            print("rec: ",rec)
            rec.show_back_button = self._context.get('from_patient_form', False)
    
    @api.depends('file_name')
    def _compute_file_type(self):
        """Determine file type from file name extension"""
        for record in self:
            if record.file_name:
                extension = record.file_name.split('.')[-1].lower() if '.' in record.file_name else ''
                if extension == 'pdf':
                    record.file_type = 'pdf'
                elif extension in ['doc', 'docx']:
                    record.file_type = 'docx'
                elif extension in ['xls', 'xlsx']:
                    record.file_type = 'xlsx'
                elif extension in ['jpg', 'jpeg']:
                    record.file_type = 'jpg'
                elif extension == 'png':
                    record.file_type = 'png'
                elif extension == 'txt':
                    record.file_type = 'txt'
                elif extension == 'csv':
                    record.file_type = 'csv'
                else:
                    record.file_type = 'other'
            else:
                record.file_type = 'other'
    
    @api.depends('file')
    def _compute_file_size(self):
        """Calculate file size in KB"""
        for record in self:
            if record.file:
                try:
                    file_str = record.file
                    # Fix padding
                    missing_padding = len(file_str) % 4
                    if missing_padding:
                        file_str += '=' * (4 - missing_padding)

                    record.file_size = len(base64.b64decode(file_str)) / 1024
                    print("Record File Size:", record.file_size)
                except Exception as e:
                    _logger.error(f"Failed to decode file: {e}")
                    record.file_size = 0
            else:
                record.file_size = 0

    
    def action_sign_document(self):
        """Sign the document by the provider"""
        return self.write({
            'is_signed': True,
            'signed_by': self.env.user.provider_id.id if self.env.user.provider_id else False,
            'signature_date': fields.Datetime.now(),
            'state': 'approved' if self.state == 'pending_review' else self.state
        })
    
    def action_patient_sign(self):
        """Record patient signature"""
        return self.write({
            'patient_signed': True,
            'patient_signature_date': fields.Datetime.now()
        })
    
    def action_submit_for_review(self):
        """Submit document for review"""
        return self.write({'state': 'pending_review'})
    
    def action_approve(self):
        """Approve the document"""
        return self.write({'state': 'approved'})
    
    def action_reject(self):
        """Reject the document"""
        return self.write({'state': 'rejected'})
    
    def action_archive(self):
        """Archive the document"""
        return self.write({'state': 'archived'})
    
    def action_share_with_patient(self):
        """Share document with patient"""
        return self.write({
            'is_shared': True,
            'shared_date': fields.Datetime.now(),
            'access_level': 'patient'
        })
        
    def action_back_to_patient(self):
        """ Redirect back to the Patient form """
        print("self Tage",self)
        print("Medical History partner_id: ",self.patient_id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.info',
            'view_mode': 'form',
            'res_id': self.patient_id.id,  # Open the related patient record
            'target': 'current',
        }
        
    def action_demographic(self):
        record_id = self.patient_id.id  # Get the ID of the current record (person)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.info',  # Replace with actual model
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': record_id,  # Pass the record ID of the person to be displayed
            'target': 'current',  # Open in a new window
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
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
    def dummy_action(self):
        pass  # Do nothing
        
    # def action_create_new_version(self):
    #     """Create a new version of this document"""
    #     # Mark current as not latest
    #     self.write({'is_latest_version': False})
        
    #     # Create new version
    #     new_doc = self.copy({
    #         'version_number': self.version_number + 1,
    #         'parent_document_id': self.id,
    #         'is_latest_version': True,
    #         'is_signed': False,
    #         'signed_by': False,
    #         'signature_date': False,
    #         'patient_signed': False,
    #         'patient_signature_date': False,
    #         'state': 'draft',
    #     })
        
    #     return {
    #         'name': _('New Document Version'),
    #         'view_mode': 'form',
    #         'res_model': 'ehr_cdss.document',
    #         'res_id': new_doc.id,
    #         'type': 'ir.actions.act_window',
    #     }


class DocumentTag(models.Model):
    _name = 'ehr_cdss.document.tag'
    _description = 'Document Tag'
    
    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color Index")
    description = fields.Text(string="Description")
    document_ids = fields.Many2many('ehr_cdss.document', string="Tagged Documents")
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Tag name must be unique!')
    ]
