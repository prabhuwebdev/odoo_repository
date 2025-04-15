# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PatientImmunizationRecord(models.Model):
    _name = 'ehr_cdss.patient.immunization.record'
    _description = 'Patient Immunization and Infectious Disease Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('ehr_cdss.patient.info', string='Patient', required=True, tracking=True,domain=[('is_patient', '=', True)])
    user_id = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
    # Immunization Status
    immunization_status = fields.Selection([
        ('complete', 'Complete'),
        ('incomplete', 'Incomplete'),
        ('unknown', 'Unknown')
    ], string='Immunization Status', tracking=True)
    
    immunization_records_available = fields.Boolean(string='Immunization Records Available', tracking=True)
    
    immunization_record_source = fields.Selection([
        ('personal', 'Personal records'),
        ('healthcare', 'Healthcare provider'),
        ('registry', 'Electronic registry'),
        ('school', 'School records'),
        ('other', 'Other')
    ], string='Immunization Record Source', tracking=True)
    
    childhood_immunizations_complete = fields.Boolean(string='Childhood Immunization Series Complete', tracking=True)
    adult_immunizations_complete = fields.Boolean(string='Adult Immunization Series Complete', tracking=True)
    
    # Vaccination History - Simple Multiselection fields
    childhood_vaccine_history = fields.Selection([
        ('dtap_tdap', 'DTaP/Tdap'),
        ('ipv_opv', 'IPV/OPV'),
        ('mmr', 'MMR'),
        ('hib', 'Hib'),
        ('hepb', 'HepB'),
        ('varicella', 'Varicella'),
        ('pcv', 'PCV'),
        ('rv', 'RV')
    ], string='Childhood Vaccine History', tracking=True)
    
    adult_vaccine_history = fields.Selection([
        ('td_tdap', 'Td/Tdap'),
        ('influenza', 'Influenza'),
        ('pneumococcal', 'Pneumococcal'),
        ('shingles', 'Shingles'),
        ('hepa', 'HepA'),
        ('hepb', 'HepB'),
        ('hpv', 'HPV'),
        ('meningococcal', 'Meningococcal')
    ], string='Adult Vaccine History', tracking=True)
    
    # COVID-19 Vaccination
    covid19_vaccination = fields.Boolean(string='COVID-19 Vaccination', tracking=True)
    covid19_vaccine_type = fields.Selection([
        ('pfizer', 'Pfizer'),
        ('moderna', 'Moderna'),
        ('johnson', 'Johnson & Johnson'),
        ('astrazeneca', 'AstraZeneca'),
        ('novavax', 'Novavax'),
        ('other', 'Other')
    ], string='COVID-19 Vaccine Type', tracking=True)
    covid19_doses = fields.Integer(string='Number of COVID-19 Vaccine Doses', tracking=True)
    covid19_last_dose_date = fields.Date(string='Date of Last COVID-19 Vaccine Dose', tracking=True)
    covid19_booster = fields.Boolean(string='COVID-19 Booster Received', tracking=True)
    
    # Influenza Vaccination
    influenza_vaccination = fields.Boolean(string='Annual Influenza Vaccination', tracking=True)
    influenza_last_date = fields.Date(string='Date of Last Influenza Vaccine', tracking=True)
    
    # Pneumococcal Vaccination
    pneumococcal_vaccination = fields.Boolean(string='Pneumococcal Vaccination', tracking=True)
    pneumococcal_type = fields.Selection([
        ('pcv13', 'PCV13'),
        ('ppsv23', 'PPSV23'),
        ('both', 'Both')
    ], string='Pneumococcal Type', tracking=True)
    pneumococcal_date = fields.Date(string='Date of Pneumococcal Vaccine', tracking=True)
    
    # Tetanus Vaccination
    tetanus_vaccination = fields.Boolean(string='Tetanus Vaccination', tracking=True)
    tetanus_last_date = fields.Date(string='Date of Last Tetanus Vaccine', tracking=True)
    tetanus_type = fields.Selection([
        ('td', 'Td'),
        ('tdap', 'Tdap')
    ], string='Tetanus Type', tracking=True)
    
    # HPV Vaccination
    hpv_vaccination = fields.Boolean(string='HPV Vaccination', tracking=True)
    hpv_completion = fields.Boolean(string='HPV Series Completion Status', tracking=True)
    hpv_dates = fields.Text(string='Dates of HPV Vaccines', tracking=True)
    
    # Hepatitis A Vaccination
    hepatitis_a_vaccination = fields.Boolean(string='Hepatitis A Vaccination', tracking=True)
    hepatitis_a_completion = fields.Boolean(string='Hepatitis A Series Completion Status', tracking=True)
    hepatitis_a_dates = fields.Text(string='Dates of Hepatitis A Vaccines', tracking=True)
    
    # Hepatitis B Vaccination
    hepatitis_b_vaccination = fields.Boolean(string='Hepatitis B Vaccination', tracking=True)
    hepatitis_b_completion = fields.Boolean(string='Hepatitis B Series Completion Status', tracking=True)
    hepatitis_b_dates = fields.Text(string='Dates of Hepatitis B Vaccines', tracking=True)
    
    # MMR Vaccination
    mmr_vaccination = fields.Boolean(string='MMR Vaccination', tracking=True)
    mmr_dates = fields.Text(string='Dates of MMR Vaccines', tracking=True)
    
    # Varicella Vaccination
    varicella_vaccination = fields.Boolean(string='Varicella Vaccination', tracking=True)
    varicella_dates = fields.Text(string='Dates of Varicella Vaccines', tracking=True)
    
    # Herpes Zoster (Shingles) Vaccination
    zoster_vaccination = fields.Boolean(string='Herpes Zoster (Shingles) Vaccination', tracking=True)
    zoster_type = fields.Selection([
        ('zostavax', 'Zostavax'),
        ('shingrix', 'Shingrix')
    ], string='Zoster Type', tracking=True)
    zoster_dates = fields.Text(string='Dates of Zoster Vaccines', tracking=True)
    
    # Meningococcal Vaccination
    meningococcal_vaccination = fields.Boolean(string='Meningococcal Vaccination', tracking=True)
    meningococcal_type = fields.Selection([
        ('menacwy', 'MenACWY'),
        ('menb', 'MenB'),
        ('both', 'Both')
    ], string='Meningococcal Type', tracking=True)
    meningococcal_dates = fields.Text(string='Dates of Meningococcal Vaccines', tracking=True)
    
    # Travel Vaccines
    travel_vaccines_received = fields.Selection([
        ('yellow_fever', 'Yellow Fever'),
        ('typhoid', 'Typhoid'),
        ('japanese_encephalitis', 'Japanese Encephalitis'),
        ('rabies', 'Rabies'),
        ('cholera', 'Cholera'),
        ('other', 'Other')
    ], string='Travel Vaccines Received', tracking=True)
    travel_vaccine_dates = fields.Text(string='Dates of Travel Vaccines', tracking=True)
    
    # Vaccine Reactions
    vaccine_reactions = fields.Boolean(string='History of Vaccine Reactions', tracking=True)
    vaccine_reaction_details = fields.Text(string='Details of Vaccine Reactions', tracking=True)
    
    # Vaccine Exemptions
    vaccine_exemptions = fields.Boolean(string='Vaccine Exemptions', tracking=True)
    exemption_type = fields.Selection([
        ('medical', 'Medical'),
        ('religious', 'Religious'),
        ('philosophical', 'Philosophical'),
        ('other', 'Other')
    ], string='Exemption Type', tracking=True)
    exemption_details = fields.Text(string='Details of Vaccine Exemptions', tracking=True)
    
    # Infectious Disease History
    infectious_disease_history = fields.Boolean(string='History of Infectious Diseases', tracking=True)
    childhood_diseases = fields.Selection([
        ('measles', 'Measles'),
        ('mumps', 'Mumps'),
        ('rubella', 'Rubella'),
        ('chickenpox', 'Chickenpox'),
        ('whooping_cough', 'Whooping cough'),
        ('other', 'Other')
    ], string='Childhood Diseases', tracking=True)
    childhood_disease_dates = fields.Text(string='Dates of Childhood Diseases', tracking=True)
    
    # COVID-19 Infection
    covid19_infection = fields.Boolean(string='History of COVID-19 Infection', tracking=True)
    covid19_infection_date = fields.Date(string='Date of COVID-19 Infection', tracking=True)
    covid19_severity = fields.Selection([
        ('asymptomatic', 'Asymptomatic'),
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('critical', 'Critical')
    ], string='COVID-19 Severity', tracking=True)
    covid19_long_term_effects = fields.Text(string='Long-term Effects from COVID-19', tracking=True)
    
    # Influenza History
    influenza_history = fields.Boolean(string='History of Influenza Infection', tracking=True)
    influenza_dates = fields.Text(string='Dates of Influenza Infections', tracking=True)
    
    # Tuberculosis Screening
    tuberculosis_screening = fields.Boolean(string='Tuberculosis Screening History', tracking=True)
    tuberculosis_test_type = fields.Selection([
        ('tst_ppd', 'TST/PPD'),
        ('igra_quantiferon', 'IGRA/Quantiferon'),
        ('chest_xray', 'Chest X-ray')
    ], string='Tuberculosis Test Type', tracking=True)
    tuberculosis_test_date = fields.Date(string='Date of Last TB Test', tracking=True)
    tuberculosis_test_result = fields.Selection([
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('indeterminate', 'Indeterminate')
    ], string='Tuberculosis Test Result', tracking=True)
    tuberculosis_infection = fields.Boolean(string='History of Tuberculosis Infection', tracking=True)
    tuberculosis_treatment = fields.Text(string='Tuberculosis Treatment Details', tracking=True)
    
    # HIV Screening
    hiv_screening = fields.Boolean(string='HIV Screening History', tracking=True)
    hiv_test_date = fields.Date(string='Date of Last HIV Test', tracking=True)
    hiv_status = fields.Selection([
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('unknown', 'Unknown')
    ], string='HIV Status', tracking=True)
    hiv_treatment = fields.Text(string='HIV Treatment Details', tracking=True)
    
    # Hepatitis B Infection
    hepatitis_b_infection = fields.Boolean(string='History of Hepatitis B Infection', tracking=True)
    hepatitis_b_status = fields.Selection([
        ('acute', 'Acute'),
        ('chronic', 'Chronic'),
        ('resolved', 'Resolved'),
        ('unknown', 'Unknown')
    ], string='Hepatitis B Status', tracking=True)
    hepatitis_b_treatment = fields.Text(string='Hepatitis B Treatment Details', tracking=True)
    
    # Hepatitis C Screening
    hepatitis_c_screening = fields.Boolean(string='Hepatitis C Screening History', tracking=True)
    hepatitis_c_test_date = fields.Date(string='Date of Last Hepatitis C Test', tracking=True)
    hepatitis_c_status = fields.Selection([
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('unknown', 'Unknown')
    ], string='Hepatitis C Status', tracking=True)
    hepatitis_c_treatment = fields.Text(string='Hepatitis C Treatment Details', tracking=True)
    
    # Sexually Transmitted Infections
    sexually_transmitted_infections = fields.Selection([
        ('chlamydia', 'Chlamydia'),
        ('gonorrhea', 'Gonorrhea'),
        ('syphilis', 'Syphilis'),
        ('herpes', 'Herpes'),
        ('hpv', 'HPV'),
        ('trichomoniasis', 'Trichomoniasis'),
        ('other', 'Other')
    ], string='Sexually Transmitted Infections', tracking=True)
    sti_dates = fields.Text(string='Dates of STI Diagnoses', tracking=True)
    sti_treatments = fields.Text(string='STI Treatment Details', tracking=True)
    
    # MRSA History
    mrsa_history = fields.Boolean(string='History of MRSA Infection', tracking=True)
    mrsa_infection_site = fields.Text(string='Site of MRSA Infection', tracking=True)
    mrsa_treatment = fields.Text(string='MRSA Treatment Details', tracking=True)
    
    # C. Difficile History
    c_diff_history = fields.Boolean(string='History of C. difficile Infection', tracking=True)
    c_diff_dates = fields.Text(string='Dates of C. difficile Infections', tracking=True)
    c_diff_treatment = fields.Text(string='C. difficile Treatment Details', tracking=True)
    
    # Recurrent Infections
    recurrent_infections = fields.Boolean(string='History of Recurrent Infections', tracking=True)
    recurrent_infection_type = fields.Text(string='Type of Recurrent Infections', tracking=True)
    
    # Opportunistic Infections
    opportunistic_infections = fields.Boolean(string='History of Opportunistic Infections', tracking=True)
    opportunistic_infection_details = fields.Text(string='Details of Opportunistic Infections', tracking=True)
    
    # Tropical Diseases
    tropical_diseases = fields.Selection([
        ('malaria', 'Malaria'),
        ('dengue', 'Dengue'),
        ('zika', 'Zika'),
        ('chikungunya', 'Chikungunya'),
        ('leishmaniasis', 'Leishmaniasis'),
        ('schistosomiasis', 'Schistosomiasis'),
        ('other', 'Other')
    ], string='Tropical Diseases', tracking=True)
    tropical_disease_details = fields.Text(string='Details of Tropical Diseases', tracking=True)
    
    # Parasitic Infections
    parasitic_infections = fields.Boolean(string='History of Parasitic Infections', tracking=True)
    parasitic_infection_details = fields.Text(string='Details of Parasitic Infections', tracking=True)
    
    # Recent Antibiotic Use
    recent_antibiotic_use = fields.Boolean(string='Recent Antibiotic Use (within 3 months)', tracking=True)
    antibiotic_details = fields.Text(string='Details of Recent Antibiotic Use', tracking=True)
    
    # Isolation Precautions History
    isolation_precautions_history = fields.Boolean(string='History of Isolation Precautions', tracking=True)
    isolation_type = fields.Selection([
        ('contact', 'Contact'),
        ('droplet', 'Droplet'),
        ('airborne', 'Airborne'),
        ('other', 'Other')
    ], string='Isolation Type', tracking=True)
    isolation_reason = fields.Text(string='Reason for Isolation Precautions', tracking=True)
    
    # Additional Fields
    infectious_exposure_contacts = fields.Text(string='Known Exposure to Infectious Diseases', tracking=True)
    current_infectious_symptoms = fields.Text(string='Current Infectious Disease Symptoms', tracking=True)
    infection_risk_factors = fields.Text(string='Risk Factors for Infections', tracking=True)
    antimicrobial_resistance = fields.Boolean(string='History of Antimicrobial-Resistant Infections', tracking=True)
    resistant_organism = fields.Text(string='Type of Resistant Organism', tracking=True)
    infectious_disease_education_needs = fields.Text(string='Education Needs Regarding Infectious Disease Prevention', tracking=True)
    form_date = fields.Date(string='Form Date')
    to_date = fields.Date(string='To Date')
    vaccine_name = fields.Char(string='Vaccine Name')
    vaccine_type_id = fields.Many2one('ehr_cdss.vaccine.type', string='Vaccine Type')

    show_back_button = fields.Boolean(string='Show Back Button', compute='_compute_show_back_button')
    
    @api.depends_context('from_patient_form')
    def _compute_show_back_button(self):
        for rec in self:
            print("rec: ",rec)
            rec.show_back_button = self._context.get('from_patient_form', False)
            
    def action_back_to_patient(self):
        """ Redirect back to the Patient form """
        print("self Tage",self)
        print("Medical History partner_id: ",self.partner_id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ehr_cdss.patient.info',
            'view_mode': 'form',
            'res_id': self.partner_id.id,  # Open the related patient record
            'target': 'current',
        }
        
    
    def action_demographic(self):
        record_id = self.partner_id.id  # Get the ID of the current record (person)
        
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
        record_id = self.partner_id.id  # Get the ID of the current record (person)
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
        record_id = self.partner_id.id  # Get the ID of the current record (person)
        
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
        record_id = self.partner_id.id  # Get the ID of the current record (person)
        
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
        record_id = self.partner_id.id  # Get the ID of the current record (person)
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
    
    def action_document(self):
        record_id = self.partner_id.id  # Get the ID of the current record (person)
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
        self.ensure_one()
        record_id = self.partner_id.id  # Get the ID of the current record (person)
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
        record_id = self.partner_id.id  # Get the ID of the current record (person)
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

    def action_medication(self):
        record_id = self.partner_id.id  # Get the ID of the current record (person)
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
        record_id = self.partner_id.id # Get the ID of the current record (person)
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
        record_id = self.partner_id.id  # Get the ID of the current record (person)
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
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        

    def action_medication(self):
        record_id = self.partner_id.id  # Get the ID of the current record (person)
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
            'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
        }
        

    # def action_document(self):
    #     record_id = self.patient_id.id  # Get the ID of the current record (person)
    #     medication = self.env['ehr_cdss.document'].search([('patient_id', '=', record_id)], limit=1)
        
    #     if not medication:
    #         # Handle case where no medical history exists for the patient
    #         medication = self.env['ehr_cdss.document'].create({
    #             'patient_id': record_id,
    #             'user_id': self.env.user.id,  # Associate the current user who is creating the record
    #         })
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'ehr_cdss.document',  # Replace with actual model
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'res_id': medication.id,  # Pass the record ID of the person to be displayed
    #         'target': 'current',
    #         'flags': {'form': {'action': 'open_in_new_tab'}},  # Custom flag to trigger JS
    #     }