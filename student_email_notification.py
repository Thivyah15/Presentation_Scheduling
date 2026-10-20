import pandas as pd
from outlook_email import send_outlook_email


def send_student_status_email(student_id, status):

    students = pd.read_excel(
        "data/student.xlsx"
    )


    student = students[
        students["Student ID"] == student_id
    ]


    if student.empty:
        print("Student not found")
        return


    student = student.iloc[0]


    student_name = student["Student Name"]
    student_email = student["Student Email"]


    if status == "Approved":

        subject = "Presentation Request Approved"

        message = f"""
Hello {student_name},

Your presentation request has been approved.

Please login to APSS to view your presentation schedule.

Thank you.
"""


    elif status == "Rejected":

        subject = "Presentation Request Rejected"

        message = f"""
Hello {student_name},

Your presentation request has been rejected.

Please login to APSS and select another available presentation slot.

Thank you.
"""


    else:
        return


    send_outlook_email(
        student_email,
        subject,
        message
    )