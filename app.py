
import streamlit as st
from pathlib import Path
import joblib
import pandas as pd
from recommendation_engine import generate_recommendations

from feature_mapping import (
    FEATURE_GROUPS,
    ALL_FEATURES,
    FEATURE_LABELS,
    get_display_options,
    encode_value,
    decode_value,
    validate_feature_mapping
)


st.set_page_config(
    page_title="EduPulse | Student Success System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_css():
    css_file = Path("app.css")

    if css_file.exists():
        st.markdown(
            f"<style>{css_file.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True
        )


load_css()


@st.cache_resource
def load_model():
    return joblib.load("edupulse_model.pkl")


@st.cache_data
def load_data():
    return pd.read_csv("data.csv", sep=";")


model = load_model()
data = load_data()
def mapped_selectbox(label, feature):
    options = get_display_options(feature)

    selected_label = st.selectbox(
        label,
        list(options.keys())
    )

    return encode_value(feature, selected_label)


if not validate_feature_mapping():
    st.error("Feature mapping validation failed.")
    st.stop()


with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0 25px 0;">
            <h1 style="color:#20B9A5 !important; font-size:28px;">
                🎓 EduPulse
            </h1>
            <p style="color:#B8C5D6 !important; font-size:13px;">
                Every Student Matters.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Students",
            "Add New Student",
            "Recommendations"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("Student Success & Early Warning System")


if page == "Overview":
    st.title("Welcome to EduPulse 👋")
    st.write(
        "Turning student data into meaningful support."
    )

    st.divider()

    st.subheader("System Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Students",
            f"{len(data):,}"
        )

    with col2:
        dropout_count = (data["Target"] == "Dropout").sum()
        st.metric(
            "Dropout Students",
            f"{dropout_count:,}"
        )

    with col3:
        dropout_rate = (
            dropout_count / len(data) * 100
        )
        st.metric(
            "Dropout Rate",
            f"{dropout_rate:.1f}%"
        )

    st.divider()

    st.subheader("Student Distribution")

    distribution = (
        data["Target"]
        .value_counts()
        .rename_axis("Student Status")
        .reset_index(name="Number of Students")
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.bar_chart(
            distribution,
            x="Student Status",
            y="Number of Students"
        )

    with col2:
        st.dataframe(
            distribution,
            use_container_width=True,
            hide_index=True
        )


elif page == "Students":
    st.title("Students")
    st.write("Explore and manage student records.")

    st.divider()

    students = data.copy()
    students.insert(
        0,
        "Student ID",
        [f"STU-{i:04d}" for i in range(1, len(students) + 1)]
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        search = st.text_input(
            "Search Student",
            placeholder="Enter Student ID..."
        )

    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Dropout", "Enrolled", "Graduate"]
        )

    filtered_students = students.copy()

    if search:
        filtered_students = filtered_students[
            filtered_students["Student ID"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if status_filter != "All":
        filtered_students = filtered_students[
            filtered_students["Target"] == status_filter
        ]

    st.divider()

    st.subheader("Student Records")

    st.caption(f"Showing {len(filtered_students):,} students")

    st.dataframe(
        filtered_students,
        use_container_width=True,
        hide_index=True
    )

    if not filtered_students.empty:
        selected_id = st.selectbox(
            "Select a Student",
            filtered_students["Student ID"].tolist()
        )

        selected_student = filtered_students[
            filtered_students["Student ID"] == selected_id
        ].iloc[0]

        st.divider()

        st.subheader(f"Student Profile: {selected_id}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Student Status", selected_student["Target"])

        with col2:
            st.metric(
                "Age at Enrollment",
                int(selected_student["Age at enrollment"])
            )

        with col3:
            st.metric(
                "Admission Grade",
                selected_student["Admission grade"]
            )

        st.subheader("Academic Performance")

        academic_columns = [
            "Curricular units 1st sem (credited)",
            "Curricular units 1st sem (enrolled)",
            "Curricular units 1st sem (evaluations)",
            "Curricular units 1st sem (approved)",
            "Curricular units 1st sem (grade)",
            "Curricular units 1st sem (without evaluations)"
        ]

        st.dataframe(
            selected_student[academic_columns].to_frame(
                name="Value"
            ),
            use_container_width=True
        )

    else:
        st.warning("No students found matching your search.")




elif page == "Add New Student":

    st.title("Add New Student")
    st.write("Enter student information to evaluate academic performance.")
    st.divider()

    with st.form("new_student_form"):

        st.subheader("1. Personal Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.number_input(
                "Age at Enrollment",
                min_value=15,
                max_value=80,
                value=18
            )

        with col2:
            gender = mapped_selectbox("Gender", "Gender")

        with col3:
            marital_status = mapped_selectbox(
                "Marital Status",
                "Marital status"
            )

        st.divider()

        st.subheader("2. Admission & Education")

        col1, col2 = st.columns(2)

        with col1:
            application_mode = mapped_selectbox(
                "Application Mode",
                "Application mode"
            )

            application_order = st.number_input(
                "Application Order",
                min_value=0,
                max_value=10,
                value=1
            )

            course = mapped_selectbox("Course", "Course")

            previous_qualification = mapped_selectbox(
                "Previous Qualification",
                "Previous qualification"
            )

        with col2:
            previous_grade = st.number_input(
                "Previous Qualification Grade",
                min_value=0.0,
                max_value=200.0,
                value=120.0
            )

            admission_grade = st.number_input(
                "Admission Grade",
                min_value=0.0,
                max_value=200.0,
                value=120.0
            )

            attendance = mapped_selectbox(
                "Attendance",
                "Daytime/evening attendance"
            )

            nationality = mapped_selectbox(
                "Nationality",
                "Nacionality"
            )

        st.divider()

        st.subheader("3. Financial & Family Background")

        col1, col2 = st.columns(2)

        with col1:
            mothers_qualification = mapped_selectbox(
                "Mother's Qualification",
                "Mother's qualification"
            )

            fathers_qualification = mapped_selectbox(
                "Father's Qualification",
                "Father's qualification"
            )

            mothers_occupation = mapped_selectbox(
                "Mother's Occupation",
                "Mother's occupation"
            )

        with col2:
            fathers_occupation = mapped_selectbox(
                "Father's Occupation",
                "Father's occupation"
            )

            displaced = mapped_selectbox(
                "Displaced",
                "Displaced"
            )

            educational_special_needs = mapped_selectbox(
                "Educational Special Needs",
                "Educational special needs"
            )

            debtor = mapped_selectbox(
                "Debtor",
                "Debtor"
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            tuition_fees = mapped_selectbox(
                "Tuition Fees Up to Date",
                "Tuition fees up to date"
            )

        with col2:
            scholarship = mapped_selectbox(
                "Scholarship Holder",
                "Scholarship holder"
            )

        with col3:
            international = mapped_selectbox(
                "International Student",
                "International"
            )

        st.divider()

        st.subheader("4. Academic Performance")

        col1, col2, col3 = st.columns(3)

        with col1:
            credited = st.number_input(
                "1st Semester Credited Units",
                min_value=0,
                value=0
            )

            enrolled = st.number_input(
                "1st Semester Enrolled Units",
                min_value=0,
                value=5
            )

        with col2:
            evaluations = st.number_input(
                "1st Semester Evaluations",
                min_value=0,
                value=5
            )

            approved = st.number_input(
                "1st Semester Approved Units",
                min_value=0,
                value=3
            )

        with col3:
            grade = st.number_input(
                "1st Semester Grade",
                min_value=0.0,
                max_value=20.0,
                value=10.0
            )

            without_evaluations = st.number_input(
                "Units Without Evaluations",
                min_value=0,
                value=0
            )

        st.divider()

        st.subheader("5. Economic Indicators")

        st.caption(
            "Enter the economic indicators associated "
            "with the student's academic period."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            unemployment_rate = st.number_input(
                "Unemployment Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=11.1,
                step=0.1
            )

        with col2:
            inflation_rate = st.number_input(
                "Inflation Rate (%)",
                min_value=-100.0,
                max_value=100.0,
                value=1.4,
                step=0.1
            )

        with col3:
            gdp = st.number_input(
                "GDP",
                min_value=-100.0,
                max_value=100.0,
                value=0.32,
                step=0.01
            )

        st.divider()

        submitted = st.form_submit_button(
            "Save Student Information",
            use_container_width=True
        )


    if submitted:

        input_data = {
            "Marital status": marital_status,
            "Application mode": application_mode,
            "Application order": application_order,
            "Course": course,
            "Daytime/evening attendance": attendance,
            "Previous qualification": previous_qualification,
            "Previous qualification (grade)": previous_grade,
            "Nacionality": nationality,
            "Mother's qualification": mothers_qualification,
            "Father's qualification": fathers_qualification,
            "Mother's occupation": mothers_occupation,
            "Father's occupation": fathers_occupation,
            "Admission grade": admission_grade,
            "Displaced": displaced,
            "Educational special needs": educational_special_needs,
            "Debtor": debtor,
            "Tuition fees up to date": tuition_fees,
            "Gender": gender,
            "Scholarship holder": scholarship,
            "Age at enrollment": age,
            "International": international,
            "Curricular units 1st sem (credited)": credited,
            "Curricular units 1st sem (enrolled)": enrolled,
            "Curricular units 1st sem (evaluations)": evaluations,
            "Curricular units 1st sem (approved)": approved,
            "Curricular units 1st sem (grade)": grade,
            "Curricular units 1st sem (without evaluations)": without_evaluations,
            "Unemployment rate": unemployment_rate,
            "Inflation rate": inflation_rate,
            "GDP": gdp
        }

        input_df = pd.DataFrame([input_data])
        input_df = input_df.loc[:, model.feature_names_in_]

        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]

        st.session_state["last_student_data"] = input_data.copy()
        st.session_state["last_prediction"] = prediction

        st.success("Prediction completed successfully!")

        st.subheader("Student Prediction")
        st.markdown(f"### Predicted Status: {prediction}")

        st.divider()
        st.subheader("Prediction Probabilities")

        classes = model.classes_

        for i in range(len(classes)):
            percentage = probabilities[i] * 100
            st.write(f"{classes[i]}: {percentage:.2f}%")
            st.progress(float(probabilities[i]))

        st.divider()

        probability_data = pd.DataFrame({
            "Student Status": classes,
            "Probability": probabilities * 100
        })

        st.bar_chart(
            probability_data.set_index("Student Status")
        )




elif page == "Recommendations":

    st.title("Student Recommendations")
    st.write("Personalized early intervention and student support plan.")

    if "last_student_data" not in st.session_state:

        st.info("Please submit a student prediction first.")

    else:

        student_data = st.session_state["last_student_data"]
        predicted_status = st.session_state["last_prediction"]

        recommendations = generate_recommendations(
            student_data,
            predicted_status
        )

        high_count = sum(
            1 for item in recommendations
            if item["priority"] == "High"
        )

        medium_count = sum(
            1 for item in recommendations
            if item["priority"] == "Medium"
        )

        low_count = sum(
            1 for item in recommendations
            if item["priority"] == "Low"
        )

        st.subheader("Student Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Predicted Student Status",
                predicted_status
            )

        with col2:
            st.metric(
                "Total Support Categories",
                len(recommendations)
            )

        st.divider()

        st.subheader("Intervention Priority Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("High Priority", high_count)

        with col2:
            st.metric("Medium Priority", medium_count)

        with col3:
            st.metric("Low Priority", low_count)

        st.divider()

        st.subheader("Personalized Support Plan")

        st.caption(
            "Recommended interventions based on the student's "
            "predicted status and available academic and financial indicators."
        )

        priority_order = {
            "High": 1,
            "Medium": 2,
            "Low": 3
        }

        sorted_recommendations = sorted(
            recommendations,
            key=lambda item: priority_order[item["priority"]]
        )

        for index, item in enumerate(sorted_recommendations, start=1):

            with st.container(border=True):

                st.markdown(
                    f"### {index}. {item['category']}"
                )

                if item["priority"] == "High":
                    st.error("HIGH PRIORITY")

                elif item["priority"] == "Medium":
                    st.warning("MEDIUM PRIORITY")

                else:
                    st.info("LOW PRIORITY")

                st.markdown("**Why is this support needed?**")

                for reason in item["reasons"]:
                    st.markdown(f"- {reason}")

                st.markdown("**Recommended Actions**")

                for action_number, action in enumerate(
                    item["actions"], start=1
                ):
                    st.markdown(
                        f"{action_number}. {action}"
                    )

        st.divider()

        st.caption(
            "EduPulse | Every Student Matters."
        )
