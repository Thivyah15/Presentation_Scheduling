from flask import Flask, render_template, request, redirect, url_for, session, send_file

import mysql.connector

from save_apu_data import retrieve_timetable
from find_common_availability import generate_common_availability
from save_apu_data import save_timetable

from students import (
    add_student,
    get_students
)

import pandas as pd
import os

from conflict_report import generate_conflict_report

from staff_utilization_report import generate_utilization_report

from flask import session

from icalendar import Calendar, Event
from datetime import datetime

app = Flask(__name__)

app.secret_key = "apss_secret_key"



# ================= DATABASE CONNECTION ================= #

def get_db_connection():

    conn = mysql.connector.connect(

        host="localhost",

        user="root",

        password="",

        database="schedule"

    )

    return conn


@app.route("/")
def welcome():
    return render_template("home.html")

@app.route("/staff_login", methods=["GET", "POST"])
def staff_login():

    if request.method == "POST":

        email = request.form["email"]


        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="schedule"
        )


        cursor = conn.cursor(dictionary=True)


        cursor.execute(
            """
            SELECT *
            FROM staff
            WHERE email = %s
            """,
            (email,)
        )


        staff = cursor.fetchone()


        cursor.close()
        conn.close()


        if staff:

            session["lect_id"] = staff["lect_id"]
            session["staff_name"] = staff["staff_name"]
            session["staff_email"] = staff["email"]

            return redirect("/index")


        else:

            return render_template(
                "staff_login.html",
                error="Email not found"
            )


    return render_template("staff_login.html")


@app.route("/index")
def index():

    return render_template(
        "index.html",
        staff_name=session.get("staff_name")
    )

@app.route("/timetable", methods=["GET", "POST"])
def timetable():


    conn = get_db_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT lect_id, staff_name
        FROM staff
        ORDER BY staff_name
    """)


    staff = cursor.fetchall()


    cursor.close()
    conn.close()



    success = None
    error = None




    if request.method == "POST":


        method = request.form.get("method")



        # =====================================
        # RETRIEVE SUPERVISOR FROM APU
        # =====================================

        if method == "supervisor_api":


            supervisor = request.form.get(
                "supervisor"
            )


            week = request.form.get(
                "supervisor_week"
            )



            if supervisor and week:


                result = save_timetable(

                    supervisor,

                    week,

                    "data/supervisor.xlsx"

                )



                success = (
                    "Supervisor timetable retrieved successfully."
                )


            else:

                error = (
                    "Please enter supervisor and week."
                )





        # =====================================
        # RETRIEVE 2ND MARKER FROM APU
        # =====================================

        elif method == "marker_api":


            marker = request.form.get(
                "marker"
            )


            week = request.form.get(
                "marker_week"
            )



            if marker and week:


                result = save_timetable(

                    marker,

                    week,

                    "data/second_marker.xlsx"

                )



                success = (
                    "2nd Marker timetable retrieved successfully."
                )


            else:

                error = (
                    "Please enter 2nd marker and week."
                )






        # =====================================
        # EXCEL UPLOAD
        # =====================================

        elif method == "excel":


            excel_type = request.form.get(
                "excel_type"
            )


            file = request.files.get(
                "file"
            )



            if file and excel_type:



                if excel_type == "supervisor":


                    path = (
                        "data/supervisor.xlsx"
                    )


                else:


                    path = (
                        "data/second_marker.xlsx"
                    )



                file.save(path)



                success = (
                    "Excel timetable uploaded successfully."
                )



            else:


                error = (
                    "Please select type and upload file."
                )





    return render_template(
        "timetable.html",
        staff=staff,
        success=success,
        error=error
    )




@app.route("/common_availability", methods=["GET", "POST"])
def common_availability():

    availability = None


    if request.method == "POST":

        try:

            from find_common_availability import generate_common_availability

            generate_common_availability()

            print("Availability generated successfully")


        except Exception as e:

            print("Availability generation failed")
            print(e)



    availability_file = "data/common_availability.xlsx"


    if os.path.exists(availability_file):


        availability = pd.read_excel(
            availability_file
        )


        availability.columns = (
            availability.columns.str.strip()
        )



        # ================================
        # CHECK SCHEDULED PRESENTATIONS
        # ================================


        schedule_file = "data/presentation_schedule.xlsx"


        if os.path.exists(schedule_file):


            schedule = pd.read_excel(
                schedule_file
            )


            schedule.columns = (
                schedule.columns.str.strip()
            )



            for index, row in availability.iterrows():


                matched = schedule[

                    (schedule["Supervisor"] == row["Supervisor Name"])

                    &

                    (schedule["2nd Marker"] == row["2nd Marker Name"])

                    &

                    (schedule["Date"] == row["Date"])

                    &

                    (schedule["Presentation Slot"] == row["Presentation Slot"])

                ]



                if not matched.empty:

                    availability.at[
                        index,
                        "Status"
                    ] = "Not Available"



        # ================================
        # FILTER STAFF VIEW
        # ================================


        current_staff = session.get(
            "staff_name"
        )


        if current_staff:


            availability = availability[

                (availability["Supervisor Name"] == current_staff)

                |

                (availability["2nd Marker Name"] == current_staff)

            ]




        # ================================
        # FORMAT DATE
        # ================================


        if "Date" in availability.columns:


            availability["Display Date"] = (

                pd.to_datetime(
                    availability["Date"]
                )
                .dt.strftime("%d-%m-%Y")

            )



    return render_template(
        "common_availability.html",
        availability=availability
    )


@app.route("/students", methods=["GET", "POST"])
def student_page():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT lect_id, staff_name
        FROM staff
        ORDER BY staff_name
    """)

    staff = cursor.fetchall()

    cursor.close()
    conn.close()

    message = None

    if request.method == "POST":

        student_id = request.form["student_id"]
        student_name = request.form["student_name"]
        student_email = request.form["student_email"]
        supervisor = request.form["supervisor"]
        marker = request.form["marker"]

        success, message = add_student(
            student_id,
            student_name,
            student_email,
            supervisor,
            marker
        )

    students = get_students()

    # Filter students for the logged-in lecturer
    staff_name = session.get("staff_name")

    if staff_name and not students.empty:
        students = students[
            (students["Supervisor"] == staff_name) |
            (students["2nd Marker"] == staff_name)
        ]

    return render_template(
        "students.html",
        staff=staff,
        students=students,
        message=message
    )





@app.route("/import_students", methods=["POST"])
def import_students():

    file = request.files["student_file"]


    if file.filename == "":

        return redirect("/students")



    # Read uploaded Excel

    new_students = pd.read_excel(file)



    new_students.columns = (
        new_students.columns
        .str.strip()
    )



    required_columns = [
        "Student ID",
        "Student Name",
        "Student Email",
        "Supervisor",
        "2nd Marker"
    ]



    # Check Excel format

    for column in required_columns:

        if column not in new_students.columns:

            return "Invalid Excel format"



    student_file = "data/student.xlsx"



    # If existing student file exists

    if os.path.exists(student_file):


        old_students = pd.read_excel(
            student_file
        )


        old_students.columns = (
            old_students.columns
            .str.strip()
        )



        students = pd.concat(
            [
                old_students,
                new_students
            ],
            ignore_index=True
        )



    else:


        students = new_students




    # Remove duplicate Student ID

    students = students.drop_duplicates(
        subset=["Student ID"],
        keep="first"
    )




    students.to_excel(
        student_file,
        index=False
    )



    return redirect("/students")



@app.route("/presentation_schedule")
def presentation_schedule():

    schedule_file = "data/presentation_schedule.xlsx"

    staff_name = session.get("staff_name")

    if os.path.exists(schedule_file):

        schedule = pd.read_excel(schedule_file)

        schedule.columns = schedule.columns.str.strip()

        # Only show this lecturer's schedules
        if staff_name:

            schedule = schedule[
                (schedule["Supervisor"].astype(str).str.strip() == staff_name.strip()) |
                (schedule["2nd Marker"].astype(str).str.strip() == staff_name.strip())
            ]

        if "Date" in schedule.columns:

            schedule["Display Date"] = pd.to_datetime(
                schedule["Date"],
                format="mixed",
                dayfirst=True,
                errors="coerce"
            ).dt.strftime("%d-%m-%Y")

        schedule = schedule.sort_values(
            by=[
                "Date",
                "Day",
                "Presentation Slot"
            ]
        )

    else:

        schedule = pd.DataFrame()

    return render_template(
        "presentation_schedule.html",
        schedule=schedule
    )


@app.route("/export_student_calendar/<int:index>")
def export_student_calendar(index):

    schedule_file = "data/presentation_schedule.xlsx"

    if not os.path.exists(schedule_file):
        return "Schedule not found."

    schedule = pd.read_excel(schedule_file)
    schedule.columns = schedule.columns.str.strip()

    if index >= len(schedule):
        return "Invalid record."

    row = schedule.iloc[index]

    cal = Calendar()
    cal.add("prodid", "-//APSS//")
    cal.add("version", "2.0")

    event = Event()

    date = pd.to_datetime(
        row["Date"],
        dayfirst=True,
        errors="coerce"
    )

    slot = str(row["Presentation Slot"])

    start_time = slot.split("-")[0].strip()
    end_time = slot.split("-")[1].strip()

    start = datetime.strptime(
        date.strftime("%Y-%m-%d") + " " + start_time,
        "%Y-%m-%d %I:%M %p"
    )

    end = datetime.strptime(
        date.strftime("%Y-%m-%d") + " " + end_time,
        "%Y-%m-%d %I:%M %p"
    )

    event.add(
        "summary",
        f"Presentation - {row['Student Name']}"
    )

    event.add("dtstart", start)
    event.add("dtend", end)

    event.add(
        "description",
        f"""
Student ID: {row['Student ID']}
Student Name: {row['Student Name']}
Supervisor: {row['Supervisor']}
2nd Marker: {row['2nd Marker']}
"""
    )

    cal.add_component(event)

    filename = f"{row['Student ID']}.ics"

    with open(filename, "wb") as f:
        f.write(cal.to_ical())

    return send_file(
        filename,
        as_attachment=True
    )


@app.route("/conflict_report")
def conflict_report():

    staff_name = session.get("staff_name")




    conflict_df = generate_conflict_report()



    # Clean names
    conflict_df["Supervisor"] = (
        conflict_df["Supervisor"]
        .astype(str)
        .str.strip()
    )


    conflict_df["2nd Marker"] = (
        conflict_df["2nd Marker"]
        .astype(str)
        .str.strip()
    )


    staff_name = str(staff_name).strip()



    # Only show this staff's students
    conflict_df = conflict_df[
        (conflict_df["Supervisor"] == staff_name) |
        (conflict_df["2nd Marker"] == staff_name)
    ]



    conflicts = conflict_df.to_dict(
        orient="records"
    )


    return render_template(
        "conflict_report.html",
        conflicts=conflicts
    )




@app.route("/generate_conflict_report")
def generate_conflict_report_page():

    staff_name = session.get("staff_name")



    conflict_df = generate_conflict_report()



    conflict_df["Supervisor"] = (
        conflict_df["Supervisor"]
        .astype(str)
        .str.strip()
    )


    conflict_df["2nd Marker"] = (
        conflict_df["2nd Marker"]
        .astype(str)
        .str.strip()
    )



    conflict_df = conflict_df[
        (conflict_df["Supervisor"] == staff_name) |
        (conflict_df["2nd Marker"] == staff_name)
    ]



    conflicts = conflict_df.to_dict(
        orient="records"
    )


    return render_template(
        "conflict_report.html",
        conflicts=conflicts
    )



# ============================
# STUDENT REQUEST LIST
# ============================

@app.route("/student_requests")
def student_requests():

    file = "data/presentation_requests.xlsx"

    staff_name = session.get("staff_name")


    if not staff_name:
        return redirect("/staff_login")



    if not os.path.exists(file):

        return render_template(
            "student_requests.html",
            requests=pd.DataFrame()
        )



    df = pd.read_excel(file)



    # Clean column names

    df.columns = df.columns.str.strip()



    # Create approval columns

    required_columns = [
        "Supervisor Status",
        "2nd Marker Status",
        "Status"
    ]


    for col in required_columns:

        if col not in df.columns:

            df[col] = "Pending"


        df[col] = (
            df[col]
            .fillna("Pending")
            .astype(str)
            .str.strip()
        )



    # Save original Excel row

    df["Excel Index"] = df.index



    # Clean staff names

    df["Supervisor"] = (
        df["Supervisor"]
        .astype(str)
        .str.strip()
    )


    df["2nd Marker"] = (
        df["2nd Marker"]
        .astype(str)
        .str.strip()
    )



    staff_name = staff_name.strip()



    # Show only related students

    df = df[
        (df["Supervisor"] == staff_name)
        |
        (df["2nd Marker"] == staff_name)
    ]



    # Date format

    if "Date" in df.columns:

        df["Display Date"] = pd.to_datetime(
            df["Date"],
            dayfirst=True,
            errors="coerce"
        ).dt.strftime("%d-%m-%Y")



    return render_template(
        "student_requests.html",
        requests=df,
        staff_name=staff_name
    )



# ============================
# APPROVE REQUEST
# ============================

@app.route("/staff_approve_request/<int:index>", methods=["POST"])
def staff_approve_request(index):

    file = "data/presentation_requests.xlsx"


    df = pd.read_excel(file)

    df.columns = df.columns.str.strip()



    for col in [
        "Supervisor Status",
        "2nd Marker Status",
        "Status"
    ]:

        if col not in df.columns:
            df[col] = "Pending"



    staff_name = session.get("staff_name")



    if not staff_name:
        return redirect("/staff_login")



    # Supervisor decision

    if df.loc[index, "Supervisor"] == staff_name:

        df.loc[index, "Supervisor Status"] = "Accepted"



    # 2nd Marker decision

    elif df.loc[index, "2nd Marker"] == staff_name:

        df.loc[index, "2nd Marker Status"] = "Accepted"



    update_request_status(df, index)



    df.to_excel(
        file,
        index=False
    )


    return redirect("/student_requests")







# ============================
# REJECT REQUEST
# ============================

@app.route("/staff_reject_request/<int:index>", methods=["POST"])
def staff_reject_request(index):

    file = "data/presentation_requests.xlsx"


    df = pd.read_excel(file)

    df.columns = df.columns.str.strip()



    for col in [
        "Supervisor Status",
        "2nd Marker Status",
        "Status"
    ]:

        if col not in df.columns:
            df[col] = "Pending"



    staff_name = session.get("staff_name")



    if not staff_name:
        return redirect("/staff_login")



    # Supervisor decision

    if df.loc[index, "Supervisor"] == staff_name:

        df.loc[index, "Supervisor Status"] = "Rejected"



    # 2nd Marker decision

    elif df.loc[index, "2nd Marker"] == staff_name:

        df.loc[index, "2nd Marker Status"] = "Rejected"



    update_request_status(df, index)



    df.to_excel(
        file,
        index=False
    )


    return redirect("/student_requests")





# ============================
# UPDATE FINAL STATUS
# ============================

def update_request_status(df, index):


    supervisor = df.loc[
        index,
        "Supervisor Status"
    ]


    marker = df.loc[
        index,
        "2nd Marker Status"
    ]



    # Both accepted

    if supervisor == "Accepted" and marker == "Accepted":

        df.loc[index, "Status"] = "Scheduled"



    # Any rejection

    elif supervisor == "Rejected" or marker == "Rejected":

        df.loc[index, "Status"] = "Rejected"



    else:

        df.loc[index, "Status"] = "Pending"


def update_request_status(df, index):

    supervisor = df.loc[index, "Supervisor Status"]
    marker = df.loc[index, "2nd Marker Status"]

    if supervisor == "Accepted" and marker == "Accepted":

        df.loc[index, "Status"] = "Scheduled"

        # Save into presentation_schedule.xlsx
        schedule_file = "data/presentation_schedule.xlsx"

        schedule_row = df.loc[[index]].copy()

        if os.path.exists(schedule_file):

            schedule = pd.read_excel(schedule_file)

            schedule.columns = schedule.columns.str.strip()

            # Prevent duplicate schedule
            duplicate = (
                (schedule["Student ID"].astype(str) == str(schedule_row.iloc[0]["Student ID"]))
                &
                (schedule["Date"].astype(str) == str(schedule_row.iloc[0]["Date"]))
                &
                (schedule["Presentation Slot"].astype(str) == str(schedule_row.iloc[0]["Presentation Slot"]))
            )

            if not duplicate.any():
                schedule = pd.concat([schedule, schedule_row], ignore_index=True)

        else:

            schedule = schedule_row

        schedule.to_excel(schedule_file, index=False)

    elif supervisor == "Rejected" or marker == "Rejected":

        df.loc[index, "Status"] = "Rejected"

    else:

        df.loc[index, "Status"] = "Pending"


# ================= STUDENT PORTAL =================
@app.route("/student")
def student_dashboard():

    import pandas as pd

    student_id = session.get("student_id")

    presentation = None


    if student_id:

        file = "data/presentation_schedule.xlsx"


        try:

            df = pd.read_excel(file)


            student_data = df[
                df["Student ID"] == student_id
            ]


            if not student_data.empty:


                presentation = student_data.iloc[0].to_dict()



                # Format Date to dd-mm-yyyy
                if "Date" in presentation:


                    date_value = pd.to_datetime(
                        presentation["Date"]
                    )


                    presentation["Display Date"] = date_value.strftime(
                        "%d-%m-%Y"
                    )



        except Exception as e:

            print("Dashboard Error:", e)



    return render_template(
        "student_dashboard.html",
        presentation=presentation
    )


@app.route("/my_presentation")
def my_presentation():

    file = "data/presentation_requests.xlsx"

    student_id = session.get("student_id")


    if not student_id:
        return redirect("/student_login")


    if not os.path.exists(file):

        return render_template(
            "my_presentation.html",
            presentations=[]
        )


    df = pd.read_excel(file)

    df.columns = df.columns.str.strip()


    # Get student's requests

    df = df[
        df["Student ID"] == student_id
    ]


    if "Date" in df.columns:

        df["Display Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        ).dt.strftime("%d-%m-%Y")


    presentations = df.to_dict(
        orient="records"
    )


    return render_template(
        "my_presentation.html",
        presentations=presentations
    )

@app.route("/available_slots")
def available_slots():

    slots = pd.DataFrame()

    student_id = session.get("student_id")


    if student_id:

        student_file = "data/student.xlsx"
        availability_file = "data/common_availability.xlsx"
        request_file = "data/presentation_requests.xlsx"
        schedule_file = "data/presentation_schedule.xlsx"



        if os.path.exists(student_file) and os.path.exists(availability_file):


            students = pd.read_excel(student_file)

            students.columns = (
                students.columns
                .str.strip()
            )


            student = students[
                students["Student ID"]
                .astype(str)
                .str.strip()
                ==
                str(student_id).strip()
            ]



            if not student.empty:


                supervisor = student.iloc[0]["Supervisor"]
                marker = student.iloc[0]["2nd Marker"]



                # Read availability

                availability = pd.read_excel(
                    availability_file
                )


                availability.columns = (
                    availability.columns
                    .str.strip()
                )



                slots = availability[
                    (availability["Supervisor Name"] == supervisor)
                    &
                    (availability["2nd Marker Name"] == marker)
                ]



                # Remove requested slots

                if os.path.exists(request_file):

                    requests = pd.read_excel(
                        request_file
                    )


                    requests.columns = (
                        requests.columns
                        .str.strip()
                    )


                    used_requests = requests[
                        requests["Status"].isin(
                            [
                                "Pending",
                                "Accepted"
                            ]
                        )
                    ]



                    for _, row in used_requests.iterrows():

                        slots = slots[
                            ~(
                                (slots["Day"] == row["Day"])
                                &
                                (slots["Date"].astype(str) == str(row["Date"]))
                                &
                                (slots["Presentation Slot"] == row["Presentation Slot"])
                            )
                        ]



                # Remove assigned schedules

                if os.path.exists(schedule_file):


                    schedule = pd.read_excel(
                        schedule_file
                    )


                    schedule.columns = (
                        schedule.columns
                        .str.strip()
                    )



                    for _, row in schedule.iterrows():

                        slots = slots[
                            ~(
                                (slots["Day"] == row["Day"])
                                &
                                (slots["Date"].astype(str) == str(row["Date"]))
                                &
                                (slots["Presentation Slot"] == row["Presentation Slot"])
                            )
                        ]



    return render_template(
        "available_slots.html",
        slots=slots
    )

@app.route("/request_slot", methods=["POST"])
def request_slot():


    student_id = session.get("student_id")


    if not student_id:

        return redirect("/student")



    request_file = "data/presentation_requests.xlsx"

    student_file = "data/student.xlsx"




    # Read student information

    students = pd.read_excel(student_file)


    students.columns = (
        students.columns
        .str.strip()
    )



    student = students[
        students["Student ID"] == student_id
    ]



    if student.empty:

        return "Student record not found"



    student_info = student.iloc[0]




    # Check existing request

    if os.path.exists(request_file):


        requests = pd.read_excel(
            request_file
        )


        requests.columns = (
            requests.columns
            .str.strip()
        )



        existing = requests[
            (requests["Student ID"] == student_id)
            &
            (requests["Status"].isin(
                ["Pending", "Accepted"]
            ))
        ]



        if not existing.empty:


            return redirect("/request_status")



    else:


        requests = pd.DataFrame()




    # Create new request

    new_request = {


        "Student ID":
        student_info["Student ID"],


        "Student Name":
        student_info["Student Name"],


        "Supervisor":
        request.form["supervisor"],


        "2nd Marker":
        request.form["marker"],


        "Day":
        request.form["day"],


        "Date":
        request.form["date"],


        "Presentation Slot":
        request.form["slot"],


        "Status":
        "Pending"

    }





    requests = pd.concat(
        [
            requests,
            pd.DataFrame([new_request])
        ],
        ignore_index=True
    )




    requests.to_excel(
        request_file,
        index=False
    )




    return redirect("/request_status")


@app.route("/request_status")
def request_status():

    request_file = "data/presentation_requests.xlsx"

    student_id = session.get("student_id")

    if not student_id:
        return redirect("/student_login")

    if not os.path.exists(request_file):
        return render_template(
            "request_status.html",
            requests=pd.DataFrame()
        )

    requests = pd.read_excel(request_file)

    requests.columns = requests.columns.str.strip()

    if "Status" not in requests.columns:
        requests["Status"] = "Pending"

    requests["Status"] = (
        requests["Status"]
        .fillna("Pending")
        .astype(str)
        .str.strip()
    )

    requests = requests[
        requests["Student ID"].astype(str) == str(student_id)
    ]

    if "Date" in requests.columns:

        requests["Display Date"] = pd.to_datetime(
            requests["Date"],
            errors="coerce"
        ).dt.strftime("%d-%m-%Y")

    return render_template(
        "request_status.html",
        requests=requests
    )




@app.route("/student_login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        email = request.form["email"].strip()


        student_file = "data/student.xlsx"


        if os.path.exists(student_file):

            students = pd.read_excel(
                student_file
            )


            students.columns = (
                students.columns.str.strip()
            )


            student = students[
                students["Student Email"]
                .astype(str)
                .str.strip()
                ==
                email
            ]


            if not student.empty:


                session["student_id"] = (
                    student.iloc[0]["Student ID"]
                )


                session["student_name"] = (
                    student.iloc[0]["Student Name"]
                )


                return redirect(
                    url_for("student_dashboard")
                )


        return render_template(
            "student_login.html",
            error="Student email not found."
        )


    return render_template(
        "student_login.html"
    )


if __name__ == "__main__":
    app.run(debug=True)