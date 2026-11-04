
# EduPulse 🎓

### Every Student Matters.

**EduPulse** is a Machine Learning-powered Student Early Warning and Support System designed to predict students' academic outcomes and recommend personalized interventions.

The system aims to help educational institutions identify students who may be at risk of dropping out and support better, data-informed decisions.

---

## Project Overview

EduPulse analyzes student demographic, academic, financial, and socio-economic information to predict one of three academic outcomes:

- Dropout
- Enrolled
- Graduate

Based on the prediction and selected student indicators, the system generates personalized academic and financial support recommendations.

## Key Features

- **Student Dashboard:** Explore student records and academic statistics.
- **Student Management:** Search and view existing student profiles.
- **Dropout Prediction:** Predict student academic outcomes using a trained Machine Learning model.
- **Prediction Probabilities:** Display the probability associated with each predicted outcome.
- **Personalized Recommendations:** Generate support actions based on prediction results and student indicators.
- **Early Warning Support:** Help identify students who may need additional academic or financial attention.

## Machine Learning

The project uses a supervised Machine Learning approach to classify students into three outcome categories.

The model development process includes:

- Data loading and understanding.
- Exploratory Data Analysis (EDA).
- Data preprocessing.
- Feature engineering and feature selection.
- Model training and comparison.
- Hyperparameter tuning.
- Model evaluation.
- Model serialization for application deployment.

**Selected Model:** Logistic Regression

The model is saved as a reusable Scikit-learn Pipeline.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Model Persistence | Joblib |
| Web Application | Streamlit |
| Version Control | Git, GitHub |

## Project Structure

```text
EduPulse/
│
├── app.py
├── app.css
├── feature_mapping.py
├── recommendation_engine.py
├── edupulse_model.pkl
├── data.csv
├── Dr_Amr.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_NAME
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

## Dataset

The project uses the **Predict Students' Dropout and Academic Success** dataset from the UCI Machine Learning Repository.

The dataset contains demographic, academic, and socio-economic features used to analyze student academic outcomes.

Dataset source:

https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success

## Important Notes

- Predictions are based on the available dataset features and the trained model.
- The system is intended as a decision-support tool, not a replacement for human judgment.
- Recommendations are rule-based and should be reviewed by educational professionals.
- The original dataset represents a specific educational context, so model performance and applicability should be validated before deployment in other educational environments.

## Future Improvements

- Model optimization and performance enhancement.
- Advanced feature selection.
- Improved prediction reliability.
- More personalized intervention strategies.
- Integration with additional educational data sources.

---

**EduPulse | Every Student Matters.**
