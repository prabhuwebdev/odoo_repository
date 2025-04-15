# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FamilyHistory(models.Model):
    _name = 'ehr_cdss.medical.family.history'
    _description = 'Family Medical History'
    _rec_name = 'patient_id'
    _table = 'ehr_cdss_medical_family_history'  # Shortened table name

    patient_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True)
    user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
    
    # Cancer history
    family_cancer_history = fields.Many2one(
        'ehr_cdss.medical.family.member.cancer', 
        string='Family Members with Cancer', 
        help='Family Members with Cancer (Type, Age of Onset, and Outcome)',
        ondelete='cascade',  # Ensures proper cleanup of related records
        relation='ehr_cdss_medical_family_member_cancer_rel'  # Shortened table name for the relationship
    )
    family_cancer_details = fields.Text(
        string='Cancer Details',
        help='Details of cancer types and outcomes in family members'
    )
    
    # Genetic predisposition
    genetic_predisposition = fields.Boolean(
        string='Genetic Predisposition', 
        # required=True,
        help='Presence of Genetic Predisposition Syndromes'
    )
    genetic_syndrome_type = fields.Selection([
        ('brca', 'BRCA1/2'),
        ('lynch', 'Lynch Syndrome'),
        ('other', 'Other')
    ], string='Genetic Syndrome Type', help='BRCA1/2, Lynch Syndrome, Other')
    
    genetic_syndrome_details = fields.Text(
        string='Genetic Syndrome Details',
        help='Details of genetic predisposition syndromes'
    )
    
    # Screening history
    hereditary_cancer_screening = fields.Boolean(
        string='Hereditary Cancer Screening',
        help='Hereditary Cancer Screening History'
    )
    screening_details = fields.Text(
        string='Screening Details',
        help='Details of hereditary cancer screening'
    )
    
    # Family disease history
    family_cardiovascular_disease = fields.Boolean(
        string='Cardiovascular Disease',
        help='Family History of Cardiovascular Disease'
    )
    family_diabetes = fields.Boolean(
        string='Diabetes',
        help='Family History of Diabetes'
    )
    family_hypertension = fields.Boolean(
        string='Hypertension',
        help='Family History of Hypertension'
    )
    family_stroke = fields.Boolean(
        string='Stroke',
        help='Family History of Stroke'
    )
    family_autoimmune_disorders = fields.Boolean(
        string='Autoimmune Disorders',
        help='Family History of Autoimmune Disorders'
    )
    family_neurological_disorders = fields.Boolean(
        string='Neurological Disorders',
        help='Family History of Neurological Disorders'
    )
    family_psychiatric_disorders = fields.Boolean(
        string='Psychiatric Disorders',
        help='Family History of Psychiatric Disorders'
    )
    family_substance_abuse = fields.Boolean(
        string='Substance Abuse',
        help='Family History of Substance Abuse'
    )
    family_developmental_disorders = fields.Boolean(
        string='Developmental Disorders',
        help='Family History of Developmental Disorders'
    )
    family_congenital_anomalies = fields.Boolean(
        string='Congenital Anomalies',
        help='Family History of Congenital Anomalies'
    )
    other_hereditary_conditions = fields.Text(
        string='Other Hereditary Conditions',
        help='Other Significant Hereditary Conditions'
    )
    
    # Family structure
    consanguinity = fields.Boolean(
        string='Consanguinity',
        help='Presence of Consanguinity'
    )
    family_longevity = fields.Text(
        string='Family Longevity',
        help='Information on Longevity in Family'
    )
    family_structure = fields.Text(
        string='Family Structure',
        help='Family Structure and Living Arrangements'
    )
    primary_caregiver = fields.Text(
        string='Primary Caregiver',
        help='Primary Caregiver Information'
    )
    family_support_system = fields.Selection([
        ('strong', 'Strong'),
        ('moderate', 'Moderate'),
        ('minimal', 'Minimal'),
        ('none', 'None')
    ], string='Family Support System', help='Strong, Moderate, Minimal, None')
    
    siblings_information = fields.Text(
        string='Siblings Information',
        help='Number and Ages of Siblings'
    )
    parents_health_status = fields.Text(
        string='Parents Health Status',
        help='Health Status of Parents'
    )
    grandparents_health_status = fields.Text(
        string='Grandparents Health Status',
        help='Health Status of Grandparents'
    )
    
    # Additional info
    family_medical_history_unknown = fields.Boolean(
        string='History Unknown',
        help='Family Medical History Unknown (adoption, etc.)'
    )
    family_history_comments = fields.Text(
        string='Additional Comments',
        help='Additional Comments on Family History'
    )
    
    show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')
    
    @api.depends_context('from_patient_form')
    def _compute_show_back_button(self):
        for rec in self:
            print("rec: ",rec)
            rec.show_back_button = self._context.get('from_patient_form', False)
    
    
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
    
    # def action_document(self):
    #     record_id = self.patient_id.id  # Get the ID of the current record (person)
    #     document = self.env['ehr_cdss.document'].search([('patient_id', '=', record_id)], limit=1)
        
    #     if not document:
    #         # Handle case where no medical history exists for the patient
    #         document = self.env['ehr_cdss.document'].create({
    #             'patient_id': record_id,
    #             'user_id': self.env.user.id,  # Associate the current user who is creating the record
    #         })
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'ehr_cdss.document',  # Replace with actual model
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'res_id': document.id,  # Pass the record ID of the person to be displayed
    #         'target': 'current',
    #         'context': {'from_patient_form': True},  # ✅ pass context flag
    #         'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
    #     }
    
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
        
class FamilyMemberCancer(models.Model):
    _name = 'ehr_cdss.medical.family.member.cancer'
    _description = 'Family Member Cancer History'
    _table = 'ehr_cdss_medical_family_member_cancer'  # Manually set the table name to shorten it
    _rec_name = 'relation'  # or whatever field you want shown

    
    # cancer_name = fields.Char(string="Cancer Name")
    relation = fields.Selection([
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('sister', 'Sister'),
        ('brother', 'Brother'),
        ('maternal_grandmother', 'Maternal Grandmother'),
        ('maternal_grandfather', 'Maternal Grandfather'),
        ('paternal_grandmother', 'Paternal Grandmother'),
        ('paternal_grandfather', 'Paternal Grandfather'),
        ('maternal_aunt', 'Maternal Aunt'),
        ('maternal_uncle', 'Maternal Uncle'),
        ('paternal_aunt', 'Paternal Aunt'),
        ('paternal_uncle', 'Paternal Uncle'),
        ('cousin', 'Cousin'),
        ('other', 'Other')
    ], string='Relation', required=True)
    
    cancer_type = fields.Selection([
        ('breast', 'Breast Cancer'),
        ('lung', 'Lung Cancer'),
        ('colorectal', 'Colorectal Cancer'),
        ('prostate', 'Prostate Cancer'),
        ('skin', 'Skin Cancer'),
        ('lymphoma', 'Lymphoma'),
        ('leukemia', 'Leukemia'),
        ('pancreatic', 'Pancreatic Cancer'),
        ('ovarian', 'Ovarian Cancer'),
        ('endometrial', 'Endometrial Cancer'),
        ('cervical', 'Cervical Cancer'),
        ('liver', 'Liver Cancer'),
        ('kidney', 'Kidney Cancer'),
        ('bladder', 'Bladder Cancer'),
        ('thyroid', 'Thyroid Cancer'),
        ('brain', 'Brain Cancer'),
        ('stomach', 'Stomach Cancer'),
        ('esophageal', 'Esophageal Cancer'),
        ('other', 'Other')
    ], string='Cancer Type', required=True)
    
    age_of_onset = fields.Integer(string='Age of Onset')
    
    outcome = fields.Selection([
        ('remission', 'In Remission'),
        ('ongoing', 'Ongoing Treatment'),
        ('deceased', 'Deceased'),
        ('unknown', 'Unknown')
    ], string='Outcome')
    
    additional_notes = fields.Text(string='Additional Notes')
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.relation} - {record.cancer_type}"
            if record.age_of_onset:
                name += f" (Age: {record.age_of_onset})"
            result.append((record.id, name))
        return result
