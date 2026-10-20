import mysql.connector
from outlook_email import send_outlook_email



def get_lecturer_email(lecturer_name):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="schedule"
    )


    cursor = conn.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT email
        FROM staff
        WHERE staff_name = %s
        """,
        (lecturer_name,)
    )


    lecturer = cursor.fetchone()


    cursor.close()
    conn.close()


    if lecturer:

        return lecturer["email"]


    else:

        print(
            "Lecturer email not found:",
            lecturer_name
        )

        return None




def send_lecturer_request_email(
    lecturer_name,
    student_id,
    student_name,
    presentation_date,
    presentation_slot,
):


    lecturer_email = get_lecturer_email(
        lecturer_name
    )


    if not lecturer_email:

        return



    subject = "New Presentation Slot Request"



    message = f"""
Dear Lecturer,

A new presentation slot request has been submitted and requires your review.

Presentation Request Details

Student ID: {student_id}
Student Name: {student_name}
Presentation Date: {presentation_date}
Presentation Time: {presentation_slot}

Please login to the Automated Presentation Scheduling System (APSS) to review and approve or reject this request.

Thank you.

Automated Presentation Scheduling System (APSS)

This is an automated email. Please do not reply.
"""



    send_outlook_email(
        lecturer_email,
        subject,
        message
    )