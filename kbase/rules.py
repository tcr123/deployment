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
    '''
    IF a patient is pregnant AND has a fasting plasma glucose level >= 92 mg/dL and < 126 mg/dL, THEN the patient might have gestational diabetes.
    IF a patient is pregnant AND has a 1-hour plasma glucose level >= 180 mg/dL after a 75-gram glucose load, THEN the patient might have gestational diabetes.
    IF a patient is pregnant AND has a 2-hour plasma glucose level >= 153 mg/dL after a 75-gram glucose load, THEN the patient might have gestational diabetes.
    IF a patient is pregnant AND has previously been diagnosed with gestational diabetes, THEN the patient has a higher risk of gestational diabetes.
    IF a patient is pregnant AND has a pre-pregnancy body mass index (BMI) >= 30, THEN the patient has a higher risk of gestational diabetes.
    IF a patient is pregnant AND has polycystic ovary syndrome, THEN the patient has a higher risk of gestational diabetes.
    IF a patient is pregnant AND has a first-degree relative with diabetes, THEN the patient has a higher risk of gestational diabetes.
    IF a patient is pregnant AND has previously given birth to a baby weighing over 9 pounds, THEN the patient has a higher risk of gestational diabetes.
    '''
    return [
        Rule(0.8, lambda patient: patient.data['fasting_plasma_glucose_level'] >= 126),
        Rule(0.8, lambda patient: patient.data['1_hour_plasma_glucose_level'] >= 180),
        Rule(0.8, lambda patient: patient.data['2_hour_plasma_glucose_level'] >= 153),
        Rule(0.8, lambda patient: patient.data['gestational_diabetes_history']),
        Rule(0.8, lambda patient: patient.data['bmi'] >= 30),
        Rule(0.8, lambda patient: patient.data['polycystic_ovary_syndrome']),
        Rule(0.8, lambda patient: patient.data['first_degree_relative_with_diabetes']),
        Rule(0.8, lambda patient: patient.data['previous_baby_weighed_over_9_pounds']),
    ]

def hypertension_rules():
    # translate the following rules into python code
    '''
    IF systolic blood pressure is < 140 mm Hg AND diastolic blood pressure is < 90 mm Hg BEFORE 20 weeks gestation, THEN person has Normal blood pressure.
    IF systolic blood pressure is >= 140 mm Hg OR diastolic blood pressure is >= 90 mm Hg BEFORE 20 weeks gestation, THEN the person has Chronic Hypertension.
    IF systolic blood pressure is >= 140 mm Hg OR diastolic blood pressure is >= 90 mm Hg AFTER 20 weeks gestation AND no sign of preeclampsia, THEN the person has Gestational Hypertension.
    IF systolic blood pressure is >= 140 mm Hg OR diastolic blood pressure is >= 90 mm Hg AFTER 20 weeks gestation AND has signs of preeclampsia (proteinuria, thrombocytopenia, renal insufficiency, impaired liver function, pulmonary edema, severe headaches, or visual disturbances), THEN the person has Preeclampsia.
    IF systolic blood pressure is > 160 mm Hg OR diastolic blood pressure is > 110 mm Hg WITH signs of preeclampsia, THEN the person has Severe Preeclampsia and requires immediate medical attention.
    '''
    return [
        Rule(0.8, lambda patient: patient.data['systolic_blood_pressure'] < 140 and patient.data['diastolic_blood_pressure'] < 90 and patient.data['weeks_pregnant'] < 20),
        Rule(0.8, lambda patient: patient.data['systolic_blood_pressure'] >= 140 or patient.data['diastolic_blood_pressure'] >= 90 and patient.data['weeks_pregnant'] < 20),
        Rule(0.8, lambda patient: patient.data['systolic_blood_pressure'] >= 140 or patient.data['diastolic_blood_pressure'] >= 90 and patient.data['weeks_pregnant'] >= 20 and not patient.data['preeclampsia']),
        Rule(0.8, lambda patient: patient.data['systolic_blood_pressure'] >= 140 or patient.data['diastolic_blood_pressure'] >= 90 and patient.data['weeks_pregnant'] >= 20 and patient.data['preeclampsia']),
        Rule(0.8, lambda patient: patient.data['systolic_blood_pressure'] > 160 or patient.data['diastolic_blood_pressure'] > 110 and patient.data['preeclampsia_signs']),
    ]

def anaemia_rules():
    # translate the following rules into python code
    '''
    IF a pregnant woman's haemoglobin level is < 11 g/dL THEN she may have anaemia.
    '''
    return [
        Rule(0.8, lambda patient: patient.data['haemoglobin_level'] < 11),
    ]

def rickets_rules():
    # translate the following rules into python code
    '''
    IF a person's blood tests show calcium level < 8.5 mg/dL THEN they may have rickets.
    IF a person's blood tests show phosphate level < 2.5 mg/dL THEN they may have rickets.
    IF a person's blood tests show alkaline phosphatase level > 147 IU/L THEN they may have rickets.
    IF X-rays of the person's bones show changes or deformities associated with rickets THEN they may have rickets.
    '''
    return [
        Rule(0.8, lambda patient: patient.data['calcium_level'] < 8.5),
        Rule(0.8, lambda patient: patient.data['phosphate_level'] < 2.5),
        Rule(0.8, lambda patient: patient.data['alkaline_phosphatase_level'] > 147),
        Rule(0.8, lambda patient: patient.data['rickets_associated_deformities']),
    ]

def kidney_diseases_rules():
    '''
    IF a person's urine test shows protein level of > 300mg / 24hours  THEN they may have kidney disease.
    IF a person's blood test shows creatinine level of > 0.85 mg/dL THEN they may have kidney disease.
    IF a person's pregnancy week is less than 12 weeks AND her blood test shows blood urea nitrogen (BUN) level > 12 THEN she may have kidney disease.
    IF a person's pregnancy week is mroe than 12 weeks AND less than 24 weeks AND her blood test shows blood urea nitrogen (BUN) level > 13 THEN she may have kidney disease.
    IF a person's pregnancy week is mroe than 24 weeks AND her blood test shows blood urea nitrogen (BUN) level > 11 THEN she may have kidney disease.
    IF a person's Glomerular Filtration Rate (GFR) is < 60 for 3 months or more THEN they may have chronic kidney disease.
    IF a person has hypertension THEN they may have kidney disease.
    IF a person has symptoms like swelling in the ankles, poor appetite, fatigue, sleep problems, muscle cramps at night, puffy eyes in the morning, or frequent urination THEN they may have kidney disease.
    IF a person has a family history of kidney disease or has diabetes or high blood pressure THEN they are at higher risk for kidney disease.
    '''
    return [
        Rule(0.8, lambda patient: patient.data['urine_protein_level'] > 300),
        Rule(0.8, lambda patient: patient.data['blood_creatinine_level'] > 0.85),
        Rule(0.8, lambda patient: patient.data['weeks_pregnant'] < 12 and patient.data['blood_urea_nitrogen_level'] > 12),
        Rule(0.8, lambda patient: patient.data['weeks_pregnant'] > 12 and patient.data['weeks_pregnant'] < 24 and patient.data['blood_urea_nitrogen_level'] > 13),
        Rule(0.8, lambda patient: patient.data['weeks_pregnant'] > 24 and patient.data['blood_urea_nitrogen_level'] > 11),
        Rule(0.8, lambda patient: patient.data['glomerular_filtration_rate'] < 60),
        Rule(0.8, lambda patient: patient.data['hypertension']),
        Rule(0.8, lambda patient: patient.data['swelling_in_ankles'] or patient.data['poor_appetite'] or patient.data['fatigue'] or patient.data['sleep_problems'] or patient.data['muscle_cramps_at_night'] or patient.data['puffy_eyes_in_morning'] or patient.data['frequent_urination']),
        Rule(0.8, lambda patient: patient.data['family_history_kidney_disease']),
    ]

def scurvy_rules():
    '''
    IF a person's dietary history shows prolonged inadequate intake of vitamin C (<10 mg/day for about a month) THEN they are at risk of scurvy.
    IF a person presents with symptoms such as fatigue, malaise, and inflammation of the gums (gingivitis) THEN they may have scurvy.
    IF a person presents with more severe symptoms such as anaemia, edema (swelling), petechiae (small red or purple spots), bleeding and bruising easily, or joint pain THEN they may have scurvy.
    IF a person presents with cork-screw hair and/or swollen, bleeding gums, which are classic signs of scurvy, THEN they may have scurvy.
    IF a person's blood test shows vitamin C level < 0.02 mg/dL THEN they may have scurvy.
    '''
    return [
        Rule(0.8, lambda patient: patient.data['daily_vitamin_c_intake'] < 10),
        Rule(0.8, lambda patient: patient.data['fatigue']),
        Rule(0.8, lambda patient: patient.data['cork_screw_hair'] or patient.data['gingivitis']),
        Rule(0.8, lambda patient: patient.data['vitamin_c_level'] < 0.02),
    ]

def heart_disease_rules():
    '''
    IF a person's blood pressure is consistently over 130/80 mm Hg THEN they are at risk for heart disease.
    IF a person's pregnancy week is less than 12 weeks AND (total cholesterol level > 5.64 mmol/L OR LDL cholesterol level > 3.27 mmol/L OR HDL cholesterol level < 1.23 mmol/L) THEN they are at risk for heart disease.
    IF a person's pregnancy week more less than 12 weeks AND (total cholesterol level > 7.50 mmol/L OR LDL cholesterol level > 4.83 mmol/L OR HDL cholesterol level < 1.41 mmol/L) THEN they are at risk for heart disease.
    IF a person has a high body mass index (BMI), particularly over 30, THEN they are at risk for heart disease.
    IF a person has a family history of heart disease at an early age THEN they are at risk for heart disease.
    IF a person has been diagnosed with diabetes THEN they are at risk for heart disease.
    IF a person is a smoker THEN they are at risk for heart disease.
    IF a person leads a sedentary lifestyle and does not engage in regular physical activity THEN they are at risk for heart disease.
    IF a person experiences symptoms such as chest pain, chest tightness, shortness of breath, or fatigue THEN they may have heart disease.
    IF a person's electrocardiogram (ECG/EKG), echocardiogram, or other heart imaging tests show abnormal results THEN they may have heart disease.
    '''
    return [
        Rule(0.8, lambda patient: patient.data['hyptertension']),
        Rule(0.8, lambda patient: patient.data['weeks_pregnant'] < 12 and (patient.data['tc_level'] > 5.64 or patient.data['ldlc_level'] > 3.27 or patient.data['hdlc_level'] < 1.23)),
        Rule(0.8, lambda patient: patient.data['weeks_pregnant'] > 12 and (patient.data['tc_level'] > 7.50 or patient.data['ldlc_level'] > 4.83 or patient.data['hdlc_level'] < 1.41)),
        Rule(0.8, lambda patient: patient.data['bmi'] > 30),
        Rule(0.8, lambda patient: patient.data['family_history_heart_disease']),
        Rule(0.8, lambda patient: patient.data['diabetes']),
        Rule(0.8, lambda patient: patient.data['smoker']),
        Rule(0.8, lambda patient: patient.data['chest_pain'] or patient.data['shortness_of_breath'] or patient.data['fatigue']),
    ]

def eye_disease_rules():
    '''
    IF a person experiences blurred or hazy vision, THEN they might have a refractive error (like myopia, hyperopia, or astigmatism) or cataract.
    IF a person experiences a gradual loss of central vision, perhaps along with distortions such as straight lines appearing wavy, THEN they might have age-related macular degeneration.
    IF a person sees floating spots or flashes of light, THEN they might have a retinal detachment or vitreous detachment.
    IF a person experiences loss of peripheral vision or 'tunnel vision', THEN they might have glaucoma.
    IF a person experiences double vision, THEN they might have a corneal problem, a nerve problem, or uncorrected refractive error.
    IF a person has increased sensitivity to light, THEN they might have an inflammation or infection, such as conjunctivitis.
    IF a person experiences red, itchy, or dry eyes, THEN they might have an allergy or dry eye syndrome.
    IF a person has difficulty seeing at night or in low light, THEN they might have night blindness, which can be a symptom of Vitamin A deficiency or retinitis pigmentosa.
    IF a person's eyes look bulgy or they have difficulty moving their eyes, THEN they might have thyroid eye disease.
    IF a person's comprehensive eye exam shows abnormalities such as increased eye pressure, optic nerve damage, or retinal damage, THEN they might have glaucoma, macular degeneration, or other serious eye conditions.
    '''
    return [
        Rule(0.8, lambda patient: patient.data['blurred_vision']),
        Rule(0.8, lambda patient: patient.data['floating_spots'] or patient.data['flashes_of_light']),
        Rule(0.8, lambda patient: patient.data['increased_sensitivity_to_light']),
        Rule(0.8, lambda patient: patient.data['red_eyes']),
        Rule(0.8, lambda patient: patient.data['difficulty_seeing_in_low_light']),
        Rule(0.8, lambda patient: patient.data['bulgy_eyes']),
    ]

def diet_recommendation_rules():
    '''
    IF a person has obesity (CF=0.9) THEN they might benefit from the low_carb_diet (CF=0.7) or Mediterranean_diet (CF=0.7).
    IF a person has diabetes (CF=0.9) THEN they might benefit from the low_carb_diet (CF=0.8) or high_fiber_diet (CF=0.8).
    IF a person has hypertension (CF=0.9) THEN they might benefit from the DASH_diet (CF=0.8) or low_sodium_diet (CF=0.8).
    IF a person has anemia (CF=0.9) THEN they might benefit from a high_protein_diet (CF=0.7), assuming the anemia is due to iron deficiency.
    IF a person has rickets (CF=0.9) THEN they might benefit from an omni_diet with adequate vitamin D and calcium (CF=0.7).
    IF a person has kidney diseases (CF=0.9) THEN they might benefit from the low_sodium_diet (CF=0.7) or low_protein_diet (CF=0.7).
    IF a person has scurvy (CF=0.9) THEN they might benefit from an omni_diet (CF=0.7) that includes plenty of vitamin C-rich foods.
    IF a person has heart disease (CF=0.9) THEN they might benefit from the DASH_diet (CF=0.8) or a low_fat_diet (CF=0.7).
    IF a person has eye-disease (CF=0.9) THEN they might benefit from an omni_diet (CF=0.7) rich in omega-3 fatty acids and vitamins for macular health.
    '''
    return [
        Rule(0.9, lambda patient: patient.data['obesity']),
        Rule(0.9, lambda patient: patient.data['diabetes']),
        Rule(0.9, lambda patient: patient.data['hypertension']),
        Rule(0.9, lambda patient: patient.data['anemia']),
        Rule(0.9, lambda patient: patient.data['rickets']),
        Rule(0.9, lambda patient: patient.data['kidney_diseases']),
        Rule(0.9, lambda patient: patient.data['scurvy']),
        Rule(0.9, lambda patient: patient.data['heart_disease']),
        Rule(0.9, lambda patient: patient.data['eye_disease']),
    ]
    
# def compute_CF(user_CF, rule, patient):
#     if rule.apply_rule(patient):
#         return user_CF * rule.expert_cf
#     else:
#         return 0
        
# def combine_CFs(cfs):
#     cf_combined = cfs[0]
#     for cf in cfs[1:]:
#         cf_combined = cf_combined + cf * (1 - cf_combined)
#     return cf_combined

# patient_data = {
#     'bmi': 31,
# }

# patient = Patient(patient_data)
# ob_rules = obesity_rules()

# user_CF = 0.7

# cfs = [compute_CF(user_CF, rule, patient) for rule in ob_rules]
# cf_combined = combine_CFs(cfs)
# confidence_percentage = cf_combined * 100

# print(f'Confidence percentage: {confidence_percentage:.2f}%')