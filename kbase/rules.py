# Define the rules inside a rule-based expert system
class Rule:
    def __init__(self, user_cf, expert_cf, apply_rule):
        self.user_cf = user_cf
        self.expert_cf = expert_cf
        self.apply_rule = apply_rule

def obesity_rules():
    return [
        Rule(1.0, 1.0, lambda patient: 25 <= patient.data['bmi'] >= 30),
    ]

def gestational_diabetes_rules():
    return [
        Rule(1.0, 0.9, lambda patient: patient.data['1_hour_plasma_glucose_level'] >= 180),
        Rule(1.0, 0.75, lambda patient: patient.data['gestational_diabetes_history']),
        Rule(1.0, 1.0, lambda patient: patient.data['bmi'] >= 30),
    ]

def hypertension_rules():
    return [
        Rule(1.0, 0.95, lambda patient: patient.data['systolic_blood_pressure'] >= 140 or patient.data['diastolic_blood_pressure'] >= 90),
        # Preemclampia symptoms
        Rule(1.0, 0.7, lambda patient: patient.data['urine_protein_level'] > 300),
        Rule(0.8, 0.55, lambda patient: patient.data['blurred_vision']),
    ]

def anaemia_rules():
    # translate the following rules into python code
    return [
        Rule(1.0, 0.95, lambda patient: patient.data['haemoglobin_level'] < 11),
    ]

def rickets_rules():
    return [
        Rule(1.0, 0.8, lambda patient: patient.data['calcium_level'] < 8.5),
        Rule(1.0, 0.8, lambda patient: patient.data['phosphate_level'] < 2.5),
    ]

def kidney_diseases_rules():
    return [
        Rule(1.0, 0.8, lambda patient: patient.data['urine_protein_level'] > 300),
        Rule(1.0, 0.8, lambda patient: patient.data['blood_creatinine_level'] > 0.85),
        Rule(1.0, 0.8, lambda patient: patient.data['weeks_pregnant'] < 12 and patient.data['blood_urea_nitrogen_level'] > 12),
        Rule(1.0, 0.8, lambda patient: patient.data['weeks_pregnant'] > 12 and patient.data['weeks_pregnant'] < 24 and patient.data['blood_urea_nitrogen_level'] > 13),
        Rule(1.0, 0.8, lambda patient: patient.data['weeks_pregnant'] > 24 and patient.data['blood_urea_nitrogen_level'] > 11),
        Rule(1.0, 0.8, lambda patient: patient.data['hypertension']),
        Rule(1.0, 0.8, lambda patient: patient.data['fatigue']),
    ]

def scurvy_rules():
    return [
        Rule(1.0, 0.8, lambda patient: patient.data['fatigue']),
        Rule(1.0, 0.8, lambda patient: patient.data['gingivitis']),
        Rule(1.0, 0.8, lambda patient: patient.data['vitamin_c_level'] < 0.02),
    ]

def heart_disease_rules():
    return [
        Rule(0.95, 0.75, lambda patient: patient.data['hypertension']),
        Rule(1.0, 0.75, lambda patient: patient.data['weeks_pregnant'] < 12 and (patient.data['ldlc_level'] > 3.27 or patient.data['hdlc_level'] < 1.23)),
        Rule(1.0, 0.75, lambda patient: patient.data['weeks_pregnant'] > 12 and (patient.data['ldlc_level'] > 4.83 or patient.data['hdlc_level'] < 1.41)),
        Rule(1.0, 0.7, lambda patient: 25 <= patient.data['bmi'] >= 30),
        Rule(0.95, 0.75, lambda patient: patient.data['family_history_heart_disease']),
        Rule(0.95, 0.55, lambda patient: patient.data['gestational_diabetes']),
        Rule(0.8, 0.7, lambda patient: patient.data['chest_pain'] or patient.data['fatigue']),
    ]

def eye_disease_rules():
    return [
        Rule(0.8, 0.55, lambda patient: patient.data['blurred_vision']),
        Rule(0.8, 0.55, lambda patient: patient.data['floating_spots']),
    ]
    
def compute_CF(rule, patient):
    if rule.apply_rule(patient):
        return rule.user_CF * rule.expert_cf
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

    threshold = 0.9

    for disease in check_sequence:
        rules = diseases[disease]
        cfs = [compute_CF(rule, patient) for rule in rules]
        cf_combined = combine_CFs(cfs)
        confidence_percentage = cf_combined * 100

        if confidence_percentage / 100 >= threshold:
            patient.set(disease, True)
            diagnosis_results[disease] = True
        else:
            patient.set(disease, False)
            diagnosis_results[disease] = False

    return diagnosis_results


def disease_to_keywords(diagnosis_results):
    disease_to_keyword = {
        'obesity': ['carbohydrates', 'fiber', 'low_carb_diet', 'low_fat_diet', 'obesity', 'high_fiber_diet', 'ketogenic_diet', 'gluten_free_diet', 
                    'vegan_diet', 'omni_diet'],
        'gestational_diabetes': ['carbohydrates', 'protien', 'fiber', 'low_carb_diet', 'diabeties', 'pregnancy', 'magnesium', 'hormone_diet', 
                                 'type_a_diet', 'omni_diet'],
        'hypertension': ['sodium', 'low_sodium_diet', 'dash_diet', 'hypertension', 'chloride', 'Mediterranean_diet', 'hormone_diet', 'omni_diet'],
        'anemia': ['iron', 'vitamin_c', 'vitamin_e', 'anemia'],
        'rickets': ['calcium', 'vitamin_d', 'rickets', 'phosphorus'],
        'kidney_diseases': ['protein', 'sodium', 'potassium', 'kidney_disease', 'alkaline_diet', 'chloride'],
        'scurvy': ['vitamin_c', 'scurvy'],
        'heart_disease': ['sodium', 'protien', 'fiber', 'low_sodium_diet', 'low_fat_diet', 'dash_diet', 'heart_disease', 'chloride',
                           'magnesium', 'selenium', 'Mediterranean_diet', 'hormone_diet', 'type_o_diet', 'type_a_diet', 'paleo_diet', 'omni_diet'],
        'eye_disease': ['vitamin_a', 'eye_disease']
    }
  
    keywords = []

    for disease, present in diagnosis_results.items():
        if present:
            keywords += disease_to_keyword[disease]

    return keywords

def get_features(patient):
    diagnosis_results = evaluate_all_rules(patient)
    features = disease_to_keywords(diagnosis_results)
    return features
    # recommended_diet = diet_recommendation_rules(diagnosis_results)
    # return recommended_diet


'''
Without using model

# using the diagnosis results and the food_dataset panda dataframe, return all the Meal_Id of the meals where the Disease column (space separated) contains any of the disease in diagnosis_results
def diet_recommendation_rules(diagnosis_results):
    recommended_diet = []
    for disease, present in diagnosis_results.items():
        if present:
            recommended_diet += food_dataset[food_dataset['Disease'].str.contains(disease)]['Meal_Id'].tolist()

    # remove duplicates
    recommended_diet = list(set(recommended_diet))
    return recommended_diet

def get_diet(patient):
    diagnosis_results = evaluate_all_rules(patient)
    recommended_diet = diet_recommendation_rules(diagnosis_results)
    return recommended_diet

'''

# patient_data = {
#     'bmi': 31, # BMI of 31 which indicates obesity
#     '1_hour_plasma_glucose_level': 190, # 1 hour plasma glucose level of 190, indicating gestational diabetes
#     'gestational_diabetes_history': True, # Patient has a history of gestational diabetes
#     'systolic_blood_pressure': 145, # High systolic blood pressure, indicating hypertension
#     'diastolic_blood_pressure': 95, # High diastolic blood pressure, also indicating hypertension
#     'urine_protein_level': 350, # High level of protein in urine, indicating pre-eclampsia or kidney disease
#     'blurred_vision': True, # Symptom can be related to hypertension or eye disease
#     'haemoglobin_level': 10.5, # Low haemoglobin level, indicating anaemia
#     'calcium_level': 8.2, # Low calcium level, indicating rickets
#     'phosphate_level': 2.4, # Low phosphate level, also indicating rickets
#     'blood_creatinine_level': 0.9, # High blood creatinine level, indicating kidney disease
#     'weeks_pregnant': 14, # Patient is in the second trimester of pregnancy
#     'blood_urea_nitrogen_level': 14, # High blood urea nitrogen level, indicating kidney disease
#     'fatigue': True, # Patient has fatigue, which can be a symptom of multiple diseases
#     'gingivitis': True, # Patient has gingivitis, which can be a symptom of scurvy
#     'vitamin_c_level': 0.01, # Low vitamin C level, indicating scurvy
#     'ldlc_level': 3.5, # LDL cholesterol level is within normal range
#     'hdlc_level': 1.2, # HDL cholesterol level is within normal range
#     'family_history_heart_disease': True, # Family history of heart disease
#     'chest_pain': True, # Chest pain can be a symptom of heart disease
#     'floating_spots': True, # Floating spots can be a symptom of eye disease
#     'obesity': False,
#     'gestational_diabetes': False,
#     'hypertension': False,   
#     'anaemia': False,
#     'rickets': False,
#     'kidney_diseases': False,
#     'scurvy': False,
#     'heart_disease': False,
#     'eye_disease': False
# }

# keywords = ['calcium', 'carbohydrates', 'chloride', 'fiber', 'iodine', 'iron', 'magnesium', 'manganese', 'phosphorus', 'potassium', 
    #             'protien', 'selenium', 'sodium', 'vitamin_a', 'vitamin_c', 'vitamin_d', 'vitamin_e', 'anemia', 'cancer', 'diabeties', 'eye_disease', 
    #             'goitre', 'heart_disease', 'hypertension', 'kidney_disease', 'obesity', 'pregnancy', 'rickets', 'scurvy', 'Mediterranean_diet', 
    #             'alkaline_diet', 'dash_diet', 'gluten_free_diet', 'high_fiber_diet', 'high_protien_diet', 'hormone_diet', 'ketogenic_diet', 
    #             'low_carb_diet', 'low_fat_diet', 'low_sodium_diet', 'omni_diet', 'paleo_diet', 'type_a_diet', 'type_o_diet', 'vegan_diet']
