from odoo import models, fields, api


class Patient(models.Model):
    _name = 'medical.patient'
    _description = 'Patient Record'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', required=True)
    sex = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Sex', required=True)

    # Additional patient information
    date_of_birth = fields.Date(string='Date of Birth')
    blood_group = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'),
        ('o+', 'O+'), ('o-', 'O-'),
    ], string='Blood Group')
    height = fields.Float(string='Height (cm)')
    weight = fields.Float(string='Weight (kg)')

    # Contact information
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')

    # Medical information
    allergies = fields.Text(string='Allergies')
    current_medications = fields.Text(string='Current Medications')
    medical_history = fields.Text(string='Medical History')

    # Health habits
    health_habits = fields.Text(string='Health Habits Summary', compute='_compute_health_habits_summary', store=True)
    habit_ids = fields.One2many('medical.patient.habit', 'patient_id', string='Health Habits')

    # Relations
    diagnosis_ids = fields.One2many('medical.diagnosis', 'patient_id', string='Diagnoses')

    # BMI calculation
    bmi = fields.Float(string='BMI', compute='_compute_bmi', store=True)

    @api.depends('weight', 'height')
    def _compute_bmi(self):
        for record in self:
            if record.weight and record.height and record.height > 0:
                record.bmi = record.weight / ((record.height / 100) ** 2)
            else:
                record.bmi = 0

    # Age calculation from date of birth
    @api.onchange('date_of_birth')
    def _onchange_date_of_birth(self):
        if self.date_of_birth:
            today = fields.Date.today()
            delta = today - self.date_of_birth
            self.age = delta.days // 365

    @api.depends('habit_ids', 'habit_ids.smoking_status', 'habit_ids.alcohol_status', 'habit_ids.substance_use')
    def _compute_health_habits_summary(self):
        for record in self:
            if not record.habit_ids:
                record.health_habits = "No health habits information recorded."
                continue

            habit = record.habit_ids[0]  # Get the first habit record

            summary_parts = []

            # Smoking
            if habit.smoking_status:
                smoking_status = dict(self.env['medical.patient.habit']._fields['smoking_status'].selection).get(
                    habit.smoking_status)
                summary_parts.append(f"Smoking: {smoking_status}")

                if habit.smoking_status == 'ex_smoker' and habit.smoking_quit_date:
                    summary_parts[-1] += f" (Quit on {habit.smoking_quit_date})"
                elif habit.smoking_status not in ('non_smoker', 'ex_smoker') and habit.smoking_years:
                    summary_parts[-1] += f" for {habit.smoking_years} years"

            # Alcohol
            if habit.alcohol_status:
                alcohol_status = dict(self.env['medical.patient.habit']._fields['alcohol_status'].selection).get(
                    habit.alcohol_status)
                alcohol_info = f"Alcohol: {alcohol_status}"

                if habit.alcohol_status != 'non_drinker' and habit.alcohol_frequency:
                    frequency = dict(self.env['medical.patient.habit']._fields['alcohol_frequency'].selection).get(
                        habit.alcohol_frequency)
                    alcohol_info += f" ({frequency})"

                summary_parts.append(alcohol_info)

            # Substance Use
            if habit.substance_use:
                substances = ", ".join(habit.substances.mapped('name'))
                summary_parts.append(f"Substance Use: {substances or 'Yes'}")

            # Physical Activity
            if habit.physical_activity:
                activity_level = dict(self.env['medical.patient.habit']._fields['physical_activity'].selection).get(
                    habit.physical_activity)
                summary_parts.append(f"Physical Activity: {activity_level}")

            # Diet
            if habit.diet_type:
                diet_type = dict(self.env['medical.patient.habit']._fields['diet_type'].selection).get(habit.diet_type)
                summary_parts.append(f"Diet: {diet_type}")

            # Combine all parts
            record.health_habits = ". ".join(summary_parts) if summary_parts else "No significant health habits noted."
