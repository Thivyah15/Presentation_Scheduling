import os
import pandas as pd
from datetime import datetime


# ==========================================
# STAFF NOTIFICATION
# ==========================================

def create_staff_notification(
    staff_name,
    student_id,
    student_name
):

    file = "data/notifications.xlsx"


    notification = {

        "Staff Name": staff_name,

        "Student ID": student_id,

        "Student Name": student_name,

        "Title": "New Presentation Request",

        "Message": "A new presentation request has been submitted.",

        "Status": "Unread",

        "Date": datetime.now().strftime("%d-%m-%Y %H:%M")

    }


    if os.path.exists(file):

        df = pd.read_excel(file)

    else:

        df = pd.DataFrame(columns=[
            "Staff Name",
            "Student ID",
            "Student Name",
            "Title",
            "Message",
            "Status",
            "Date"
        ])


    df = pd.concat(
        [df, pd.DataFrame([notification])],
        ignore_index=True
    )


    df.to_excel(
        file,
        index=False
    )



# ==========================================
# STUDENT NOTIFICATION
# ==========================================

def create_student_notification(
    student_id,
    title,
    message
):

    file = "data/student_notifications.xlsx"


    notification = {

        "Student ID": student_id,

        "Title": title,

        "Message": message,

        "Status": "Unread",

        "Date": datetime.now().strftime("%d-%m-%Y %H:%M")

    }


    if os.path.exists(file):

        df = pd.read_excel(file)

    else:

        df = pd.DataFrame(columns=[
            "Student ID",
            "Title",
            "Message",
            "Status",
            "Date"
        ])


    df = pd.concat(
        [df, pd.DataFrame([notification])],
        ignore_index=True
    )


    df.to_excel(
        file,
        index=False
    )