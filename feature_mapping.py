
import pandas as pd

DATA_PATH = "data.csv"

FEATURE_GROUPS = {
    "Personal Information": [
        "Marital status",
        "Gender",
        "Age at enrollment",
        "Nacionality",
        "International",
        "Displaced",
        "Educational special needs"
    ],

    "Admission & Education": [
        "Application mode",
        "Application order",
        "Course",
        "Daytime/evening attendance",
        "Previous qualification",
        "Previous qualification (grade)",
        "Admission grade",
        "Mother's qualification",
        "Father's qualification"
    ],

    "Financial & Family Background": [
        "Mother's occupation",
        "Father's occupation",
        "Debtor",
        "Tuition fees up to date",
        "Scholarship holder"
    ],

    "Academic Performance": [
        "Curricular units 1st sem (credited)",
        "Curricular units 1st sem (enrolled)",
        "Curricular units 1st sem (evaluations)",
        "Curricular units 1st sem (approved)",
        "Curricular units 1st sem (grade)",
        "Curricular units 1st sem (without evaluations)",
        "Unemployment rate",
        "Inflation rate",
        "GDP"
    ]
}

ALL_FEATURES = [
    feature
    for group in FEATURE_GROUPS.values()
    for feature in group
]

SYSTEM_FEATURES = [
    "Unemployment rate",
    "Inflation rate",
    "GDP"
]

USER_INPUT_FEATURES = [
    feature
    for feature in ALL_FEATURES
    if feature not in SYSTEM_FEATURES
]

CATEGORICAL_FEATURES = [
    "Marital status",
    "Application mode",
    "Course",
    "Previous qualification",
    "Nacionality",
    "Mother's qualification",
    "Father's qualification",
    "Mother's occupation",
    "Father's occupation"
]

BINARY_FEATURES = [
    "Displaced",
    "Educational special needs",
    "Debtor",
    "Tuition fees up to date",
    "Gender",
    "Scholarship holder",
    "International",
    "Daytime/evening attendance"
]

ORDINAL_FEATURES = [
    "Application order"
]


NUMERICAL_FEATURES = [
    feature
    for feature in ALL_FEATURES
    if feature not in (
        CATEGORICAL_FEATURES
        + BINARY_FEATURES
        + SYSTEM_FEATURES
    )
]


FEATURE_LABELS = {
    "Marital status": "Marital Status",
    "Application mode": "Application Mode",
    "Application order": "Application Order",
    "Course": "Course",
    "Daytime/evening attendance": "Attendance",
    "Previous qualification": "Previous Qualification",
    "Previous qualification (grade)": "Previous Qualification Grade",
    "Nacionality": "Nationality",
    "Mother's qualification": "Mother's Education",
    "Father's qualification": "Father's Education",
    "Mother's occupation": "Mother's Occupation",
    "Father's occupation": "Father's Occupation",
    "Admission grade": "Admission Grade",
    "Displaced": "Displaced Student",
    "Educational special needs": "Educational Special Needs",
    "Debtor": "Outstanding Debt",
    "Tuition fees up to date": "Tuition Fees Up to Date",
    "Gender": "Gender",
    "Scholarship holder": "Scholarship Holder",
    "Age at enrollment": "Age at Enrollment",
    "International": "International Student",
    "Curricular units 1st sem (credited)": "Credited Units",
    "Curricular units 1st sem (enrolled)": "Enrolled Units",
    "Curricular units 1st sem (evaluations)": "Evaluations",
    "Curricular units 1st sem (approved)": "Approved Units",
    "Curricular units 1st sem (grade)": "Semester Grade",
    "Curricular units 1st sem (without evaluations)": "Units Without Evaluations",
    "Unemployment rate": "Unemployment Rate",
    "Inflation rate": "Inflation Rate",
    "GDP": "GDP"
}


def load_source_data():
    data = pd.read_csv(DATA_PATH, sep=";")
    data.columns = data.columns.str.strip()
    return data


def get_value_mapping():
    data = load_source_data()

    mapping = {}

    for feature in CATEGORICAL_FEATURES + BINARY_FEATURES:
        mapping[feature] = sorted(
            data[feature].dropna().unique().tolist()
        )

    return mapping


def validate_feature_mapping():
    data = load_source_data()

    assert len(ALL_FEATURES) == 30
    assert len(set(ALL_FEATURES)) == 30

    excluded_features = {
        "Curricular units 2nd sem (credited)",
        "Curricular units 2nd sem (enrolled)",
        "Curricular units 2nd sem (evaluations)",
        "Curricular units 2nd sem (approved)",
        "Curricular units 2nd sem (grade)",
        "Curricular units 2nd sem (without evaluations)"
    }

    assert set(ALL_FEATURES) == (
        set(data.columns) - {"Target"} - excluded_features
    )

    assert len(FEATURE_LABELS) == 30

    assert len(CATEGORICAL_FEATURES) == 9
    assert len(BINARY_FEATURES) == 8
    assert len(NUMERICAL_FEATURES) == 10
    assert len(ORDINAL_FEATURES) == 1
    assert len(SYSTEM_FEATURES) == 3

    assert set(ORDINAL_FEATURES).issubset(
        set(NUMERICAL_FEATURES)
    )

    model_features = (
        set(CATEGORICAL_FEATURES)
        | set(BINARY_FEATURES)
        | set(NUMERICAL_FEATURES)
        | set(SYSTEM_FEATURES)
    )

    assert model_features == set(ALL_FEATURES)

    return True

VALUE_LABELS = {
    "Marital status": {
        1: "Single",
        2: "Married",
        3: "Widower",
        4: "Divorced",
        5: "Facto Union",
        6: "Legally Separated"
    },

    "Gender": {
        0: "Female",
        1: "Male"
    },

    "Daytime/evening attendance": {
        0: "Evening",
        1: "Daytime"
    },

    "Displaced": {
        0: "No",
        1: "Yes"
    },

    "Educational special needs": {
        0: "No",
        1: "Yes"
    },

    "Debtor": {
        0: "No",
        1: "Yes"
    },

    "Tuition fees up to date": {
        0: "No",
        1: "Yes"
    },

    "Scholarship holder": {
        0: "No",
        1: "Yes"
    },

    "International": {
        0: "No",
        1: "Yes"
    },

    "Course": {
        33: "Biofuel Production Technologies",
        171: "Animation and Multimedia Design",
        8014: "Social Service (Evening)",
        9003: "Agronomy",
        9070: "Communication Design",
        9085: "Veterinary Nursing",
        9119: "Informatics Engineering",
        9130: "Equinculture",
        9147: "Management",
        9238: "Social Service",
        9254: "Tourism",
        9500: "Nursing",
        9556: "Oral Hygiene",
        9670: "Advertising and Marketing Management",
        9773: "Journalism and Communication",
        9853: "Basic Education",
        9991: "Management (Evening)"
    },

    "Nacionality": {
        1: "Portuguese",
        2: "German",
        6: "Spanish",
        11: "Italian",
        13: "Dutch",
        14: "English",
        17: "Lithuanian",
        21: "Angolan",
        22: "Cape Verdean",
        24: "Guinean",
        25: "Mozambican",
        26: "Santomean",
        32: "Turkish",
        41: "Brazilian",
        62: "Romanian",
        100: "Moldovan",
        101: "Mexican",
        103: "Ukrainian",
        105: "Russian",
        108: "Cuban",
        109: "Colombian"
    },   
    "Application mode": {
        1: "1st Phase - General Contingent",
        2: "Ordinance No. 612/93",
        5: "1st Phase - Azores Special Contingent",
        7: "Holders of Other Higher Courses",
        10: "Ordinance No. 854-B/99",
        15: "International Student (Bachelor)",
        16: "1st Phase - Madeira Special Contingent",
        17: "2nd Phase - General Contingent",
        18: "3rd Phase - General Contingent",
        26: "Different Study Plan",
        27: "Other Institution",
        39: "Over 23 Years Old",
        42: "Transfer",
        43: "Change of Course",
        44: "Technological Specialization Diploma",
        51: "Change of Institution/Course",
        53: "Short Cycle Diploma",
        57: "International Institution/Course Change"
    },

    "Previous qualification": {
        1: "Secondary Education",
        2: "Higher Education - Bachelor's Degree",
        3: "Higher Education - Degree",
        4: "Higher Education - Master's",
        5: "Higher Education - Doctorate",
        6: "Frequency of Higher Education",
        9: "12th Year - Not Completed",
        10: "11th Year - Not Completed",
        12: "Other - 11th Year",
        14: "10th Year of Schooling",
        15: "10th Year - Not Completed",
        19: "Basic Education - 3rd Cycle",
        38: "Basic Education - 2nd Cycle",
        39: "Technological Specialization Course",
        40: "Higher Education - 1st Cycle",
        42: "Professional Higher Technical Course",
        43: "Higher Education - Master's (2nd Cycle)"
    },

    "Mother's qualification": {
        1: "Secondary Education - 12th Year",
        2: "Higher Education - Bachelor's Degree",
        3: "Higher Education - Degree",
        4: "Higher Education - Master's",
        5: "Higher Education - Doctorate",
        6: "Frequency of Higher Education",
        9: "12th Year - Not Completed",
        10: "11th Year - Not Completed",
        11: "7th Year (Old System)",
        12: "Other - 11th Year",
        14: "10th Year of Schooling",
        18: "General Commerce Course",
        19: "Basic Education - 3rd Cycle",
        22: "Technical-Professional Course",
        26: "7th Year of Schooling",
        27: "2nd Cycle of General High School",
        29: "9th Year - Not Completed",
        30: "8th Year of Schooling",
        34: "Unknown",
        35: "Cannot Read or Write",
        36: "Can Read - No 4th Year Completed",
        37: "Basic Education - 1st Cycle",
        38: "Basic Education - 2nd Cycle",
        39: "Technological Specialization Course",
        40: "Higher Education - 1st Cycle",
        41: "Specialized Higher Studies Course",
        42: "Professional Higher Technical Course",
        43: "Higher Education - Master's",
        44: "Higher Education - Doctorate"
    },

    "Father's qualification": {
        1: "Secondary Education - 12th Year",
        2: "Higher Education - Bachelor's Degree",
        3: "Higher Education - Degree",
        4: "Higher Education - Master's",
        5: "Higher Education - Doctorate",
        6: "Frequency of Higher Education",
        9: "12th Year - Not Completed",
        10: "11th Year - Not Completed",
        11: "7th Year (Old System)",
        12: "Other - 11th Year",
        13: "2nd Year Complementary High School",
        14: "10th Year of Schooling",
        18: "General Commerce Course",
        19: "Basic Education - 3rd Cycle",
        20: "Complementary High School Course",
        22: "Technical-Professional Course",
        25: "Complementary High School - Not Completed",
        26: "7th Year of Schooling",
        27: "2nd Cycle of General High School",
        29: "9th Year - Not Completed",
        30: "8th Year of Schooling",
        31: "General Administration and Commerce",
        33: "Supplementary Accounting and Administration",
        34: "Unknown",
        35: "Cannot Read or Write",
        36: "Can Read - No 4th Year Completed",
        37: "Basic Education - 1st Cycle",
        38: "Basic Education - 2nd Cycle",
        39: "Technological Specialization Course",
        40: "Higher Education - 1st Cycle",
        41: "Specialized Higher Studies Course",
        42: "Professional Higher Technical Course",
        43: "Higher Education - Master's",
        44: "Higher Education - Doctorate"
    },

    "Mother's occupation": {
        0: "Student",
        1: "Legislative and Executive Directors",
        2: "Intellectual and Scientific Specialists",
        3: "Intermediate-Level Technicians",
        4: "Administrative Staff",
        5: "Personal Services and Sales Workers",
        6: "Agriculture and Fisheries Workers",
        7: "Industry and Construction Workers",
        8: "Machine Operators and Assemblers",
        9: "Unskilled Workers",
        10: "Armed Forces",
        90: "Other Situation",
        99: "Not Specified",
        122: "Health Professionals",
        123: "Teachers",
        125: "ICT Specialists",
        131: "Science and Engineering Technicians",
        132: "Health Technicians",
        134: "Legal and Social Service Technicians",
        141: "Office Workers and Secretaries",
        143: "Accounting and Financial Operators",
        144: "Administrative Support Staff",
        151: "Personal Service Workers",
        152: "Sellers",
        153: "Personal Care Workers",
        171: "Skilled Construction Workers",
        173: "Printing and Craft Workers",
        175: "Food and Textile Industry Workers",
        191: "Cleaning Workers",
        192: "Unskilled Agricultural Workers",
        193: "Unskilled Industrial and Construction Workers",
        194: "Meal Preparation Assistants"
    },

    "Father's occupation": {
        0: "Student",
        1: "Legislative and Executive Directors",
        2: "Intellectual and Scientific Specialists",
        3: "Intermediate-Level Technicians",
        4: "Administrative Staff",
        5: "Personal Services and Sales Workers",
        6: "Agriculture and Fisheries Workers",
        7: "Industry and Construction Workers",
        8: "Machine Operators and Assemblers",
        9: "Unskilled Workers",
        10: "Armed Forces",
        90: "Other Situation",
        99: "Not Specified",
        101: "Armed Forces Officers",
        102: "Armed Forces Sergeants",
        103: "Other Armed Forces Personnel",
        112: "Administrative and Commercial Directors",
        114: "Hotel and Service Directors",
        121: "Physical Science and Engineering Specialists",
        122: "Health Professionals",
        123: "Teachers",
        124: "Finance and Accounting Specialists",
        131: "Science and Engineering Technicians",
        132: "Health Technicians",
        134: "Legal and Social Service Technicians",
        135: "ICT Technicians",
        141: "Office Workers and Secretaries",
        143: "Accounting and Financial Operators",
        144: "Administrative Support Staff",
        151: "Personal Service Workers",
        152: "Sellers",
        153: "Personal Care Workers",
        154: "Security Personnel",
        161: "Market-Oriented Agricultural Workers",
        163: "Subsistence Farmers and Fishers",
        171: "Skilled Construction Workers",
        172: "Metal Workers",
        174: "Electrical and Electronics Workers",
        175: "Food and Textile Industry Workers",
        181: "Fixed Plant and Machine Operators",
        182: "Assembly Workers",
        183: "Vehicle Drivers",
        192: "Unskilled Agricultural Workers",
        193: "Unskilled Industrial and Construction Workers",
        194: "Meal Preparation Assistants",
        195: "Street Vendors and Service Providers"
    }

}


def get_display_options(feature):
    data = load_source_data()

    values = sorted(data[feature].dropna().unique().tolist())

    labels = VALUE_LABELS.get(feature, {})

    return {
        labels.get(value, str(value)): value
        for value in values
    }


def encode_value(feature, display_value):
    options = get_display_options(feature)

    if display_value not in options:
        raise ValueError(
            f"Unknown value '{display_value}' for {feature}"
        )

    return options[display_value]


def decode_value(feature, code):
    labels = VALUE_LABELS.get(feature, {})

    return labels.get(code, str(code))
if __name__ == "__main__":
    data = load_source_data()

    columns = [
        "Application mode",
        "Previous qualification",
        "Mother's qualification",
        "Father's qualification",
        "Mother's occupation",
        "Father's occupation"
    ]

    for column in columns:
        print(f"\n{column}:")
        print(sorted(data[column].unique().tolist()))