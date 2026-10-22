import os
import pandas as pd

from outlook_email import send_outlook_email
from config import APSS_URL


# ==========================================
# Get Lecturer Email from staff.xlsx
# ==========================================
def get_lecturer_email(lecturer_name):

    file = "data/staff.xlsx"

    if not os.path.exists(file):

        print("staff.xlsx not found.")

        return None


    staff = pd.read_excel(file)


    staff.columns = (
        staff.columns
        .str.strip()
    )


    staff = staff.rename(
        columns={
            "Lect ID": "lect_id",
            "Staff Name": "staff_name",
            "Email": "email"
        }
    )


    staff["staff_name"] = (
        staff["staff_name"]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    staff["email"] = (
        staff["email"]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    result = staff[
        staff["staff_name"] == lecturer_name.strip()
    ]


    if not result.empty:

        return result.iloc[0]["email"]


    else:

        print(
            "Lecturer email not found:",
            lecturer_name
        )

        return None


# ==========================================
# Send Lecturer Request Email
# ==========================================
def send_lecturer_request_email(
    lecturer_name,
    student_id,
    student_name,
    selected_slots
):


    lecturer_email = get_lecturer_email(
        lecturer_name
    )


    if not lecturer_email:

        return


    subject = "New Presentation Slot Request"


    system_link = (
        f"{APSS_URL}/staff_login"
    )


    message = f"""
Dear Lecturer,

A new presentation slot request has been submitted and requires your review.


Presentation Request Details

Student ID: {student_id}

Student Name: {student_name}


Preferred Presentation Slots:

{selected_slots}


Please login to the Automated Presentation Scheduling System (APSS) to review and approve or reject this request.


System Link:
{system_link}


Thank you.

Automated Presentation Scheduling System (APSS)

This is an automated email. Please do not reply.
"""


    send_outlook_email(
        lecturer_email,
        subject,
        message
    )