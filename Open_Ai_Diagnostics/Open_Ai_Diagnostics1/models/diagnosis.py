# models/diagnosis.py
from odoo import models, fields, api
import os
import json
import logging
import requests
from datetime import datetime

_logger = logging.getLogger(__name__)


class Diagnosis(models.Model):
    _name = 'medical.diagnosis'
    _description = 'Medical Diagnosis'
    _rec_name = 'name'
    _order = 'create_date desc'

    name = fields.Char(string='Diagnosis Name', compute='_compute_name', store=True)
    patient_id = fields.Many2one('medical.patient', string='Patient', required=True)

    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    symptoms = fields.Text(string='Symptoms', required=True)

    # Diagnosis information
    diagnosis_result = fields.Text(string='Differential Diagnosis')
    selected_diagnosis = fields.Char(string='Selected Diagnosis')
    treatment_plan = fields.Text(string='Treatment Plan')

    # OpenAI API configuration
    api_key = fields.Char(string='OpenAI API Key')
    openai_model = fields.Selection([
        ('gpt-4', 'GPT-4'),
        ('gpt-3.5-turbo', 'GPT-3.5 Turbo')
    ], string='AI Model', default='gpt-4')

    # Diagnosis state
    state = fields.Selection([
        ('draft', 'Draft'),
        ('diagnosed', 'Diagnosed'),
        ('treated', 'Treatment Plan Created'),
        ('completed', 'Completed')
    ], string='Status', default='draft')

    @api.depends('patient_id', 'date')
    def _compute_name(self):
        for record in self:
            if record.patient_id and record.date:
                record.name = f"Diagnosis for {record.patient_id.name} - {record.date.strftime('%Y-%m-%d %H:%M')}"
            else:
                record.name = "New Diagnosis"

    def action_generate_diagnosis(self):
        """Generate differential diagnosis using OpenAI API"""
        self.ensure_one()

        if not self.api_key:
            # Try to get API key from system parameters
            api_key = self.env['ir.config_parameter'].sudo().get_param('medical_diagnosis.openai_api_key')
            if not api_key:
                raise models.UserError(
                    "OpenAI API key is not configured. Please set it in the system parameters or in the diagnosis form.")
            self.api_key = api_key

        # Get patient data
        patient = self.patient_id

        # Construct patient data for API call
        patient_data = {
            "name": patient.name,
            "age": str(patient.age),
            "sex": dict(patient._fields['sex'].selection).get(patient.sex),
            "symptoms": self.symptoms,
            "current_medications": patient.current_medications or "None reported",
            "medical_history": patient.medical_history or "None reported",
            "allergies": patient.allergies or "None reported"
        }

        try:
            # Call OpenAI API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            # Construct the prompt for differential diagnosis
            diagnosis_prompt = self._construct_diagnosis_prompt(patient_data)

            payload = {
                "model": self.openai_model,
                "messages": [
                    {"role": "system",
                     "content": "You are a medical diagnostic assistant. Analyze the patient information and provide 3-5 most likely diagnoses. For each diagnosis, assign a likelihood percentage based on how well it matches the patient's presentation. Then clearly indicate which symptoms/factors match perfectly, which information is missing that would strengthen the diagnosis, and which symptoms/factors contradict this diagnosis. Number each diagnosis clearly and include the likelihood percentage prominently."},
                    {"role": "user", "content": diagnosis_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                diagnosis_result = result['choices'][0]['message']['content']

                # Update diagnosis result
                self.diagnosis_result = diagnosis_result
                self.state = 'diagnosed'

                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'medical.diagnosis',
                    'res_id': self.id,
                    'view_mode': 'form',
                    'target': 'current',
                }
            else:
                _logger.error(f"OpenAI API Error: {response.text}")
                raise models.UserError(f"Error calling OpenAI API: {response.text}")

        except Exception as e:
            _logger.error(f"Error generating treatment plan: {str(e)}")
            raise models.UserError(f"Error generating treatment plan: {str(e)}")

    def action_mark_completed(self):
        """Mark the diagnosis and treatment as completed"""
        self.ensure_one()
        self.state = 'completed'

    def action_reset_to_draft(self):
        """Reset diagnosis to draft state"""
        self.ensure_one()
        self.state = 'draft'
        self.diagnosis_result = False
        self.selected_diagnosis = False
        self.treatment_plan = False

    def _construct_diagnosis_prompt(self, patient_data):
        """Construct a prompt for differential diagnosis based on patient data"""
        prompt = f"""
Patient Information:
- Name: {patient_data['name']}
- Age: {patient_data['age']}
- Sex: {patient_data['sex']}
- Symptoms: {patient_data['symptoms']}
- Current Medications: {patient_data['current_medications']}
- Medical History: {patient_data['medical_history']}
- Allergies: {patient_data['allergies']}
- Health Habits: {self.patient_id.health_habits or 'Not reported'}

Based on this information, please provide 3-5 possible diagnoses. For each diagnosis:
1. Number the diagnosis clearly (1, 2, 3, etc.)
2. State the diagnosis name
3. Provide a likelihood percentage (e.g., "Likelihood: 85%") indicating how well the patient's presentation matches this diagnosis
4. List all symptoms/factors that perfectly match this diagnosis
5. List any information that is missing that would strengthen this diagnosis
6. List any symptoms/factors that contradict or don't align with this diagnosis

Provide each diagnosis in a clear, numbered format that a user could select from. The likelihood percentages should reflect your clinical assessment of probability - they do not need to add up to 100%, and should reflect genuine medical probability of each condition.
        """
        return prompt

    def _construct_treatment_prompt(self, patient_data, diagnosis_choice, diagnosis_result):
        """Construct a prompt for treatment plan based on selected diagnosis"""
        prompt = f"""
Patient Information:
- Name: {patient_data['name']}
- Age: {patient_data['age']}
- Sex: {patient_data['sex']}
- Symptoms: {patient_data['symptoms']}
- Current Medications: {patient_data['current_medications']}
- Medical History: {patient_data['medical_history']}
- Allergies: {patient_data['allergies']}
- Health Habits: {self.patient_id.health_habits or 'Not reported'}

Differential Diagnosis Information:
{diagnosis_result}

The selected diagnosis is: {diagnosis_choice}

Please provide a comprehensive treatment plan for this diagnosis that includes:
1. Immediate next steps (tests, referrals, or treatments)
2. Medication recommendations with specific dosages and frequencies
3. Non-medication interventions (lifestyle modifications, physical therapy, etc.)
4. Follow-up recommendations (timing, tests, specialist consultations)
5. Warning signs that would require immediate medical attention
6. Long-term management strategy if applicable

Present the treatment plan in a clear, structured format with numbered steps.
        """
        return prompt


class PatientHealthHabits(models.Model):
    _name = 'medical.patient.habit'
    _description = 'Patient Health Habits'

    patient_id = fields.Many2one('medical.patient', string='Patient', required=True, ondelete='cascade')

    # Smoking habits
    smoking_status = fields.Selection([
        ('non_smoker', 'Non-Smoker'),
        ('ex_smoker', 'Ex-Smoker'),
        ('occasional', 'Occasional Smoker'),
        ('daily_light', 'Daily Light Smoker (< 10/day)'),
        ('daily_heavy', 'Daily Heavy Smoker (≥ 10/day)')
    ], string='Smoking Status')
    smoking_years = fields.Integer(string='Years of Smoking')
    smoking_quit_date = fields.Date(string='Quit Date')
    smoking_notes = fields.Text(string='Smoking Notes')

    # Alcohol consumption
    alcohol_status = fields.Selection([
        ('non_drinker', 'Non-Drinker'),
        ('occasional', 'Occasional Drinker'),
        ('regular_light', 'Regular Light Drinker'),
        ('regular_moderate', 'Regular Moderate Drinker'),
        ('regular_heavy', 'Regular Heavy Drinker')
    ], string='Alcohol Consumption')
    alcohol_frequency = fields.Selection([
        ('never', 'Never'),
        ('monthly', 'Monthly or less'),
        ('weekly', '2-4 times a month'),
        ('weekly_multiple', '2-3 times a week'),
        ('daily', '4+ times a week')
    ], string='Alcohol Frequency')
    alcohol_drinks_per_day = fields.Float(string='Average Drinks Per Day')
    alcohol_notes = fields.Text(string='Alcohol Notes')

    # Other substance use
    substance_use = fields.Boolean(string='Substance Use')
    substances = fields.Many2many('medical.substance', string='Substances Used')
    substance_notes = fields.Text(string='Substance Use Notes')

    # Physical activity
    physical_activity = fields.Selection([
        ('sedentary', 'Sedentary'),
        ('light', 'Light Activity'),
        ('moderate', 'Moderate Activity'),
        ('active', 'Very Active'),
        ('athlete', 'Athlete')
    ], string='Physical Activity Level')
    exercise_frequency = fields.Selection([
        ('never', 'Never'),
        ('rarely', 'Rarely'),
        ('weekly', '1-2 times per week'),
        ('regular', '3-5 times per week'),
        ('daily', 'Daily')
    ], string='Exercise Frequency')
    exercise_notes = fields.Text(string='Exercise Notes')

    # Diet
    diet_type = fields.Selection([
        ('regular', 'Regular/No Restrictions'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('paleo', 'Paleo'),
        ('keto', 'Ketogenic'),
        ('low_carb', 'Low Carbohydrate'),
        ('low_fat', 'Low Fat'),
        ('gluten_free', 'Gluten Free'),
        ('diabetic', 'Diabetic'),
        ('other', 'Other')
    ], string='Diet Type')
    diet_notes = fields.Text(string='Diet Notes')

    # Sleep
    avg_sleep_hours = fields.Float(string='Average Sleep Hours')
    sleep_quality = fields.Selection([
        ('poor', 'Poor'),
        ('fair', 'Fair'),
        ('good', 'Good'),
        ('excellent', 'Excellent')
    ], string='Sleep Quality')
    sleep_notes = fields.Text(string='Sleep Notes')


class MedicalSubstance(models.Model):
    _name = 'medical.substance'
    _description = 'Substances for tracking substance use'

    name = fields.Char(string='Substance Name', required=True)
    category = fields.Selection([
        ('cannabis', 'Cannabis'),
        ('opioids', 'Opioids'),
        ('stimulants', 'Stimulants'),
        ('hallucinogens', 'Hallucinogens'),
        ('sedatives', 'Sedatives'),
        ('inhalants', 'Inhalants'),
        ('other', 'Other')
    ], string='Category', required=True)
    description = fields.Text(string='Description')
    common_effects = fields.Text(string='Common Effects')
    medical_interactions = fields.Text(string='Known Medical Interactions')
    active = fields.Boolean(string='Active', default=True)

    def action_generate_treatment(self):
        """Generate treatment plan for selected diagnosis"""
        self.ensure_one()

        if not self.selected_diagnosis:
            raise models.UserError("Please select a diagnosis first.")

        if not self.api_key:
            # Try to get API key from system parameters
            api_key = self.env['ir.config_parameter'].sudo().get_param('medical_diagnosis.openai_api_key')
            if not api_key:
                raise models.UserError("OpenAI API key is not configured.")
            self.api_key = api_key

        # Get patient data
        patient = self.patient_id

        # Construct patient data for API call
        patient_data = {
            "name": patient.name,
            "age": str(patient.age),
            "sex": dict(patient._fields['sex'].selection).get(patient.sex),
            "symptoms": self.symptoms,
            "current_medications": patient.current_medications or "None reported",
            "medical_history": patient.medical_history or "None reported",
            "allergies": patient.allergies or "None reported"
        }

        try:
            # Call OpenAI API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            # Construct the prompt for treatment plan
            treatment_prompt = self._construct_treatment_prompt(patient_data, self.selected_diagnosis,
                                                                self.diagnosis_result)

            payload = {
                "model": self.openai_model,
                "messages": [
                    {"role": "system",
                     "content": "You are a medical treatment planner. Provide a detailed, step-by-step treatment plan for the selected diagnosis. Consider the patient's age, sex, medical history, current medications, and allergies. Include medications (with dosages), procedures, lifestyle modifications, and follow-up recommendations."},
                    {"role": "user", "content": treatment_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                treatment_result = result['choices'][0]['message']['content']

                # Update treatment plan
                self.treatment_plan = treatment_result
                self.state = 'treated'

                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'medical.diagnosis',
                    'res_id': self.id,
                    'view_mode': 'form',
                    'target': 'current',
                }
            else:
                _logger.error(f"OpenAI API Error: {response.text}")
                raise models.UserError(f"Error calling OpenAI API: {response.text}")
        finally:
            print("Successfully Completed")