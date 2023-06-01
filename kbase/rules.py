# Define the rules inside a rule-based expert system
# The system will determine the confidence factor of each rule for each disease from the list [obesity, diabetes, hypertension, anaemia, rickets, kidney dieases, scurvy, heart disease, eye cancer]

from patient import Patient

class Rule:
    def __init__(self, expert_cf, apply_rule):
        self.expert_cf = expert_cf
        self.apply_rule = apply_rule

def obesity_rules():
    return [
        Rule(1.0, lambda patient: 25 <= patient.data['bmi'] >= 30),
    ]

def gestational_diabetes_rules():
    return [
        Rule(0.8, lambda patient: patient.data['1_hour_plasma_glucose_level'] >= 180),
        Rule(0.8, lambda patient: patient.data['gestational_diabetes_history']),
        Rule(0.8, lambda patient: patient.data['bmi'] >= 30),
    ]

def hypertension_rules():
    return [
        Rule(0.8, lambda patient: patient.data['systolic_blood_pressure'] >= 140 or patient.data['diastolic_blood_pressure'] >= 90),
        # Preemclampia symptoms
        Rule(0.8, lambda patient: patient.data['urine_protein_level'] > 300),
        Rule(0.8, lambda patient: patient.data['blurred_vision']),
    ]

def anaemia_rules():
    # translate the following rules into python code
    return [
        Rule(0.8, lambda patient: patient.data['haemoglobin_level'] < 11),
    ]

def rickets_rules():
    return [
        Rule(0.8, lambda patient: patient.data['calcium_level'] < 8.5),
        Rule(0.8, lambda patient: patient.data['phosphate_level'] < 2.5),
    ]

def kidney_diseases_rules():
    return [
        Rule(0.8, lambda patient: patient.data['urine_protein_level'] > 300),
        Rule(0.8, lambda patient: patient.data['blood_creatinine_level'] > 0.85),
        Rule(0.8, lambda patient: patient.data['weeks_pregnant'] < 12 and patient.data['blood_urea_nitrogen_level'] > 12),
        Rule(0.8, lambda patient: patient.data['weeks_pregnant'] > 12 and patient.data['weeks_pregnant'] < 24 and patient.data['blood_urea_nitrogen_level'] > 13),
        Rule(0.8, lambda patient: patient.data['weeks_pregnant'] > 24 and patient.data['blood_urea_nitrogen_level'] > 11),
        Rule(0.8, lambda patient: patient.data['hypertension']),
        Rule(0.8, lambda patient: patient.data['fatigue']),
    ]

def scurvy_rules():
    return [
        Rule(0.8, lambda patient: patient.data['fatigue']),
        Rule(0.8, lambda patient: patient.data['gingivitis']),
        Rule(0.8, lambda patient: patient.data['vitamin_c_level'] < 0.02),
    ]

def heart_disease_rules():
    return [
        Rule(0.8, lambda patient: patient.data['hyptertension']),
        Rule(0.8, lambda patient: patient.data['weeks_pregnant'] < 12 and (patient.data['ldlc_level'] > 3.27 or patient.data['hdlc_level'] < 1.23)),
        Rule(0.8, lambda patient: patient.data['weeks_pregnant'] > 12 and (patient.data['ldlc_level'] > 4.83 or patient.data['hdlc_level'] < 1.41)),
        Rule(0.8, lambda patient: patient.data['bmi'] > 30),
        Rule(0.8, lambda patient: patient.data['family_history_heart_disease']),
        Rule(0.8, lambda patient: patient.data['gestational_diabetes']),
        Rule(0.8, lambda patient: patient.data['chest_pain'] or patient.data['fatigue']),
    ]

def eye_disease_rules():
    return [
        Rule(0.8, lambda patient: patient.data['blurred_vision']),
        Rule(0.8, lambda patient: patient.data['floating_spots']),
    ]
    
def compute_CF(user_CF, rule, patient):
    if rule.apply_rule(patient):
        return user_CF * rule.expert_cf
    else:
        return 0
        
def combine_CFs(cfs):
    cf_combined = cfs[0]
    for cf in cfs[1:]:
        cf_combined = cf_combined + cf * (1 - cf_combined)
    return cf_combined


def evaluate_all_rules(patient):
    check_sequence = ['gestational_diabetes', 'hypertension', 'obesity', 'anaemia', 'rickets', 'kidney_diseases', 'scurvy', 'heart_disease', 'eye_disease']
    diseases = {
        'obesity': obesity_rules(),
        'gestational_diabetes': gestational_diabetes_rules(),
        'hypertension': hypertension_rules(),
        'anaemia': anaemia_rules(),
        'rickets': rickets_rules(),
        'kidney_diseases': kidney_diseases_rules(),
        'scurvy': scurvy_rules(),
        'heart_disease': heart_disease_rules(),
        'eye_disease': eye_disease_rules()
    }

    diagnosis_results = {}

    user_CF = 0.7
    threshold = 0.95

    for disease in check_sequence:
        rules = diseases[disease]
        cfs = [compute_CF(user_CF, rule, patient) for rule in rules]
        cf_combined = combine_CFs(cfs)
        confidence_percentage = cf_combined * 100

        if confidence_percentage / 100 >= threshold:
            patient.set(disease, True)
            diagnosis_results[disease] = True
        else:
            patient.set(disease, False)
            diagnosis_results[disease] = False

    return diagnosis_results

# disease list = ['obesity', 'gestational_diabetes', 'hypertension', 'anaemia', 'rickets', 'kidney_diseases', 'scurvy', 'heart_disease', 'eye_disease']

def diet_recommendation_rules(diagnosis_results):
    diets = {
        'alkaline_diet': ['kidney_diseases'],
        'low_fat_diet': ['obesity', 'heart_disease'],
        'ketogenic_diet': ['obesity'],
        'low_sodium_diet': ['hypertension'],
        'high_fiber_diet': ['gestational_diabetes', 'obesity'],
        'high_protein_diet': ['anaemia'],
        'dash_diet': ['hypertension', 'heart_disease'],
        'low_carb_diet': ['gestational_diabetes', 'obesity'],
        'vegan_diet': ['obesity', 'hypertension'],
        'hormone_diet': ['rickets'],
        'type_a_diet': ['gestational_diabetes', 'heart_diasease'],
        'paleo_diet': ['gestational_diabetes'],
        'Mediterranean_diet': ['heart_disease', 'hypertension'],
        'gluten_free_diet': ['diabetes'],
        'omni_diet': ['gestational_diabetes', 'obesity', 'hypertension', 'heart_disease'],
        'type_o_diet': ['heart_disease']
    }

    diet_counts = {}

    for diet, conditions in diets.items():
        for condition in conditions:
            if diagnosis_results.get(condition):
                diet_counts[diet] = diet_counts.get(diet, 0) + 1

    if diet_counts:
        # Return the diet with the highest count
        recommended_diet = max(diet_counts, key=diet_counts.get)
    else:
        recommended_diet = None  # No suitable diet found

    return recommended_diet

def recommend_diet(patient):
    diagnosis_results = evaluate_all_rules(patient)
    recommended_diet = diet_recommendation_rules(diagnosis_results)
    return recommended_diet

patient_data = {
    'bmi': 31, # BMI of 31 which indicates obesity
    '1_hour_plasma_glucose_level': 190, # 1 hour plasma glucose level of 190, indicating gestational diabetes
    'gestational_diabetes_history': True, # Patient has a history of gestational diabetes
    'systolic_blood_pressure': 145, # High systolic blood pressure, indicating hypertension
    'diastolic_blood_pressure': 95, # High diastolic blood pressure, also indicating hypertension
    'urine_protein_level': 350, # High level of protein in urine, indicating pre-eclampsia or kidney disease
    'blurred_vision': True, # Symptom can be related to hypertension or eye disease
    'haemoglobin_level': 10.5, # Low haemoglobin level, indicating anaemia
    'calcium_level': 8.2, # Low calcium level, indicating rickets
    'phosphate_level': 2.4, # Low phosphate level, also indicating rickets
    'blood_creatinine_level': 0.9, # High blood creatinine level, indicating kidney disease
    'weeks_pregnant': 14, # Patient is in the second trimester of pregnancy
    'blood_urea_nitrogen_level': 14, # High blood urea nitrogen level, indicating kidney disease
    'hypertension': True, # Patient has hypertension
    'fatigue': True, # Patient has fatigue, which can be a symptom of multiple diseases
    'gingivitis': True, # Patient has gingivitis, which can be a symptom of scurvy
    'vitamin_c_level': 0.01, # Low vitamin C level, indicating scurvy
    'hyptertension': True, # Typo here, should be 'hypertension'
    'ldlc_level': 3.5, # LDL cholesterol level is within normal range
    'hdlc_level': 1.2, # HDL cholesterol level is within normal range
    'family_history_heart_disease': True, # Family history of heart disease
    'chest_pain': True, # Chest pain can be a symptom of heart disease
    'floating_spots': True, # Floating spots can be a symptom of eye disease

    # add fields for the diseases we want to check for
    'obesity': False,
    'gestational_diabetes': False,
    'hypertension': False,   
    'anaemia': False,
    'rickets': False,
    'kidney_diseases': False,
    'scurvy': False,
    'heart_disease': False,
    'eye_disease': False
}

patient = Patient(patient_data)
recommended_diet = recommend_diet(patient)
print(recommended_diet)