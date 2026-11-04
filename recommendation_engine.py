
def generate_recommendations(student_data, predicted_status):

    recommendations = []

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    academic_reasons = []
    academic_actions = []
    academic_priority = "Low"

    financial_reasons = []
    financial_actions = []
    financial_priority = "Low"

    approved = student_data["Curricular units 1st sem (approved)"]
    enrolled = student_data["Curricular units 1st sem (enrolled)"]
    evaluations = student_data["Curricular units 1st sem (evaluations)"]
    grade = student_data["Curricular units 1st sem (grade)"]

    debtor = student_data["Debtor"]
    tuition = student_data["Tuition fees up to date"]
    scholarship = student_data["Scholarship holder"]

    if predicted_status == "Dropout":
        academic_reasons.append(
            "The model identified an elevated dropout risk."
        )

        academic_actions.append(
            "Arrange regular academic follow-up sessions and monitor the student's progress."
        )

        academic_priority = "High"

    elif predicted_status == "Enrolled":
        academic_reasons.append(
            "The model predicted that the student may remain enrolled."
        )

        academic_actions.append(
            "Monitor academic progress and provide support when needed."
        )

        academic_priority = "Medium"

    elif predicted_status == "Graduate":
        academic_reasons.append(
            "The model predicted a Graduate outcome."
        )

        academic_actions.append(
            "Encourage internships, career planning, and professional development."
        )

    if enrolled > 0:

        approval_rate = approved / enrolled

        if approval_rate < 0.5:

            academic_reasons.append(
                f"The student approved only {approved} out of {enrolled} enrolled units."
            )

            academic_actions.append(
                "Provide additional tutoring and academic support in challenging courses."
            )

            academic_priority = "High"

    if evaluations > 0 and grade < 10:

        academic_reasons.append(
            f"The first-semester grade is {grade}, which is below 10."
        )

        academic_actions.append(
            "Arrange individual tutoring and review the student's study plan."
        )

        academic_priority = "High"

    if academic_actions:

        recommendations.append({
            "category": "Academic Support",
            "priority": academic_priority,
            "reasons": academic_reasons,
            "actions": academic_actions
        })

    if debtor == 1:

        financial_reasons.append(
            "The student is recorded as having an outstanding debt."
        )

        financial_actions.append(
            "Contact the student to discuss payment difficulties and available financial support."
        )

        financial_priority = "High"

    if tuition == 0:

        financial_reasons.append(
            "The student's tuition fees are not up to date."
        )

        financial_actions.append(
            "Review the student's tuition status and discuss possible payment arrangements."
        )

        financial_priority = "High"

    if scholarship == 0:

        financial_reasons.append(
            "The student is not currently recorded as a scholarship holder."
        )

        financial_actions.append(
            "Check whether the student is eligible for available scholarship programs."
        )

        if financial_priority != "High":
            financial_priority = "Low"

    if financial_actions:

        recommendations.append({
            "category": "Financial Support",
            "priority": financial_priority,
            "reasons": financial_reasons,
            "actions": financial_actions
        })

    if not recommendations:

        recommendations.append({
            "category": "General Support",
            "priority": "Low",
            "reasons": [
                "No specific academic or financial support indicators were identified by the current rules."
            ],
            "actions": [
                "Continue monitoring the student's academic progress."
            ]
        })

    recommendations.sort(
        key=lambda item: priority_order[item["priority"]]
    )

    return recommendations
