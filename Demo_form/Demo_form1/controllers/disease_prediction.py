import os
import json
import time
from openai import OpenAI


class MedicalDiagnosisConsole:
    def __init__(self):
        # Check for API key
        self.api_key = """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"""  # os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            self.api_key = self.get_api_key_input()

        # Sample synthetic patients for demonstration
        self.synthetic_patients = [
            {
                "name": "John Smith",
                "age": "45",
                "sex": "Male",
                "symptoms": "Chest pain, shortness of breath, pain radiating to left arm, sweating. Symptoms started 2 hours ago while exercising.",
                "current_medications": "Lisinopril 10mg daily for hypertension, Atorvastatin 20mg daily for high cholesterol.",
                "medical_history": "Hypertension diagnosed 5 years ago, Type 2 Diabetes diagnosed 3 years ago, Family history of heart disease.",
                "allergies": "Penicillin"
            },
            {
                "name": "Sarah Johnson",
                "age": "32",
                "sex": "Female",
                "symptoms": "Severe headache for past 3 days, sensitivity to light, nausea, blurred vision occasionally. Pain is throbbing and primarily on right side of head.",
                "current_medications": "Oral contraceptives, occasional ibuprofen for menstrual cramps.",
                "medical_history": "History of tension headaches, anxiety disorder diagnosed 2 years ago.",
                "allergies": "None"
            },
            {
                "name": "Miguel Rodriguez",
                "age": "67",
                "sex": "Male",
                "symptoms": "Increasing confusion over past 2 weeks, memory loss, difficulty finding words, agitation in evenings. Family reports personality changes.",
                "current_medications": "Metformin 1000mg twice daily, Losartan 50mg daily, Aspirin 81mg daily.",
                "medical_history": "Type 2 Diabetes (10 years), Hypertension, History of TIA 3 years ago.",
                "allergies": "Sulfa drugs"
            },
            {
                "name": "Emma Chen",
                "age": "8",
                "sex": "Female",
                "symptoms": "Fever (101.5°F), sore throat, enlarged tonsils with white patches, difficulty swallowing, fatigue. Symptoms started yesterday.",
                "current_medications": "Children's Tylenol as needed for fever",
                "medical_history": "Recurrent ear infections as toddler, otherwise healthy.",
                "allergies": "None known"
            },
            {
                "name": "Robert Wilson",
                "age": "52",
                "sex": "Male",
                "symptoms": "Lower back pain for 3 weeks, pain radiates down right leg to foot, numbness and tingling in right foot, pain worse with sitting.",
                "current_medications": "Ibuprofen 800mg as needed, not providing much relief.",
                "medical_history": "Hypertension, previous back strain 2 years ago that resolved with physical therapy.",
                "allergies": "Codeine"
            }
        ]

    def get_api_key_input(self):
        """Get the OpenAI API key from user input"""
        print("\n" + "=" * 80)
        print("OpenAI API Key Required")
        print("=" * 80)
        return input("Please enter your OpenAI API key: ")

    def display_menu(self):
        """Display the main menu of the application"""
        print("\n" + "=" * 80)
        print(f"{'MEDICAL DIAGNOSIS ASSISTANT':^80}")
        print("=" * 80)
        print("\nMAIN MENU:")
        print("1. Use synthetic patient data")
        print("2. Enter new patient data")
        print("3. Exit")
        return input("\nSelect an option (1-3): ")

    def display_synthetic_patients(self):
        """Display the list of available synthetic patients"""
        print("\n" + "=" * 80)
        print(f"{'SYNTHETIC PATIENTS':^80}")
        print("=" * 80)

        for i, patient in enumerate(self.synthetic_patients, 1):
            print(
                f"{i}. {patient['name']} - {patient['age']}y/o {patient['sex']} - Main symptom: {patient['symptoms'].split(',')[0]}")

        return input("\nSelect a patient (1-5) or 0 to return to main menu: ")

    def collect_patient_data(self):
        """Collect patient data from user input"""
        print("\n" + "=" * 80)
        print(f"{'ENTER PATIENT DATA':^80}")
        print("=" * 80)

        patient_data = {
            "name": input("Patient Name: "),
            "age": input("Age: "),
            "sex": input("Sex (Male/Female/Other): "),
            "symptoms": input("Symptoms (provide details): "),
            "current_medications": input("Current Medications (enter 'none' if not taking any): "),
            "medical_history": input("Medical History (enter 'none' if not applicable): "),
            "allergies": input("Allergies (enter 'none' if not applicable): ")
        }

        return patient_data

    def generate_differential_diagnosis(self, patient_data):
        """Generate differential diagnosis with detailed symptom matching using OpenAI API"""
        try:
            print("\nAnalyzing symptoms and generating potential diagnoses...\n")

            # Create OpenAI client
            client = OpenAI(api_key=self.api_key)

            # Construct the prompt for differential diagnosis
            diagnosis_prompt = self.construct_diagnosis_prompt(patient_data)

            # Call the OpenAI API for diagnosis
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system",
                     "content": "You are a medical diagnostic assistant. Analyze the patient information and provide 3-5 most likely diagnoses. For each diagnosis, assign a likelihood percentage based on how well it matches the patient's presentation. Then clearly indicate which symptoms/factors match perfectly, which information is missing that would strengthen the diagnosis, and which symptoms/factors contradict this diagnosis. Number each diagnosis clearly and include the likelihood percentage prominently."},
                    {"role": "user", "content": diagnosis_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            # Display the differential diagnosis
            diagnosis_result = response.choices[0].message.content

            print("\n" + "=" * 80)
            print(f"{'DIFFERENTIAL DIAGNOSIS':^80}")
            print("=" * 80 + "\n")
            print(f"Patient: {patient_data['name']} ({patient_data['age']}y/o {patient_data['sex']})")
            print("-" * 80 + "\n")
            print(diagnosis_result)

            # Ask user to select a diagnosis
            print("\n" + "-" * 80)
            diagnosis_choice = input("Select a diagnosis number for treatment plan: ")

            # Generate treatment plan for selected diagnosis
            self.generate_treatment_plan(patient_data, diagnosis_choice, diagnosis_result)

        except Exception as e:
            print(f"\nError: {str(e)}")

    def generate_treatment_plan(self, patient_data, diagnosis_choice, diagnosis_result):
        """Generate treatment plan for the selected diagnosis"""
        try:
            print("\nGenerating treatment plan for selected diagnosis...\n")

            # Create OpenAI client
            client = OpenAI(api_key=self.api_key)

            # Construct the prompt for treatment plan
            treatment_prompt = self.construct_treatment_prompt(patient_data, diagnosis_choice, diagnosis_result)

            # Call the OpenAI API for treatment plan
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system",
                     "content": "You are a medical treatment planner. Provide a detailed, step-by-step treatment plan for the selected diagnosis. Consider the patient's age, sex, medical history, current medications, and allergies. Include medications (with dosages), procedures, lifestyle modifications, and follow-up recommendations."},
                    {"role": "user", "content": treatment_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            # Display the treatment plan
            treatment_result = response.choices[0].message.content

            print("\n" + "=" * 80)
            print(f"{'TREATMENT PLAN':^80}")
            print("=" * 80 + "\n")
            print(f"Patient: {patient_data['name']} ({patient_data['age']}y/o {patient_data['sex']})")
            print(f"Selected Diagnosis: {diagnosis_choice}")
            print("-" * 80 + "\n")
            print(treatment_result)
            print("\n" + "=" * 80)
            print("DISCLAIMER: This is for educational purposes only. This is not medical advice.")
            print("Always consult with a qualified healthcare professional before starting any treatment.")
            print("=" * 80)

        except Exception as e:
            print(f"\nError: {str(e)}")

    def construct_diagnosis_prompt(self, patient_data):
        """Construct a prompt for differential diagnosis based on patient data"""
        prompt = f"""
Patient Information:
- Name: {patient_data['name']}
- Age: {patient_data['age']}
- Sex: {patient_data['sex']}
- Symptoms: {patient_data['symptoms']}
- Current Medications: {patient_data['current_medications'] or 'None reported'}
- Medical History: {patient_data['medical_history'] or 'None reported'}
- Allergies: {patient_data['allergies'] or 'None reported'}

Based on this information, please provide 3-5 possible diagnoses. For each diagnosis:
1. Number the diagnosis clearly (1, 2, 3, etc.)
2. State the diagnosis name
3. Provide a likelihood percentage (e.g., "Likelihood: 85%") indicating how well the patient's presentation matches this diagnosis
4. List all symptoms/factors that perfectly match this diagnosis
5. List any information that is missing that would strengthen this diagnosis (like "would be stronger if patient reported smoking" or "would be more likely if patient had fever")
6. List any symptoms/factors that contradict or don't align with this diagnosis

Provide each diagnosis in a clear, numbered format that a user could select from. The likelihood percentages should reflect your clinical assessment of probability - they do not need to add up to 100%, and should reflect genuine medical probability of each condition.
        """
        return prompt

    def construct_treatment_prompt(self, patient_data, diagnosis_choice, diagnosis_result):
        """Construct a prompt for treatment plan based on selected diagnosis"""
        prompt = f"""
Patient Information:
- Name: {patient_data['name']}
- Age: {patient_data['age']}
- Sex: {patient_data['sex']}
- Symptoms: {patient_data['symptoms']}
- Current Medications: {patient_data['current_medications'] or 'None reported'}
- Medical History: {patient_data['medical_history'] or 'None reported'}
- Allergies: {patient_data['allergies'] or 'None reported'}

Differential Diagnosis Information:
{diagnosis_result}

The user has selected diagnosis #{diagnosis_choice} for treatment planning.

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

    def run(self):
        """Run the main application loop"""
        print("\n" + "*" * 80)
        print(f"{'MEDICAL DIAGNOSIS ASSISTANT - CONSOLE VERSION':^80}")
        print("*" * 80)
        print("\nDISCLAIMER: This tool is for educational purposes only.")
        print("It does not provide medical advice. Always consult with a qualified")
        print("healthcare provider for diagnosis and treatment.")
        print("*" * 80)

        while True:
            choice = self.display_menu()

            if choice == '1':
                patient_choice = self.display_synthetic_patients()
                if patient_choice == '0':
                    continue

                try:
                    patient_index = int(patient_choice) - 1
                    if 0 <= patient_index < len(self.synthetic_patients):
                        self.generate_differential_diagnosis(self.synthetic_patients[patient_index])
                    else:
                        print("\nInvalid selection. Please try again.")
                except ValueError:
                    print("\nInvalid input. Please enter a number.")

                input("\nPress Enter to continue...")

            elif choice == '2':
                patient_data = self.collect_patient_data()
                self.generate_differential_diagnosis(patient_data)
                input("\nPress Enter to continue...")

            elif choice == '3':
                print("\nThank you for using the Medical Diagnosis Assistant. Goodbye!")
                break

            else:
                print("\nInvalid choice. Please try again.")


def main():
    app = MedicalDiagnosisConsole()
    app.run()


if __name__ == "__main__":
    main()
