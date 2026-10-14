import pandas as pd
import os


# ================= FILE LOCATION ================= #

student_file = "data/student.xlsx"
availability_file = "data/common_availability.xlsx"
schedule_file = "data/presentation_schedule.xlsx"



# ================= CREATE STUDENT FILE ================= #

def create_student_file():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(student_file):

        df = pd.DataFrame(
            columns=[
                "Student ID",
                "Student Name",
                "Student Email",
                "Supervisor",
                "2nd Marker"
            ]
        )

        df.to_excel(
            student_file,
            index=False
        )



# ================= ADD STUDENT ================= #
# ================= ADD STUDENT ================= #

def add_student(
    student_id,
    student_name,
    student_email,
    supervisor,
    marker
):

    create_student_file()


    student_df = pd.read_excel(
        student_file
    )


    student_df.columns = (
        student_df.columns.str.strip()
    )


    # Check duplicate Student ID

    if student_id in student_df["Student ID"].astype(str).values:

        return False, "Student ID already exists."



    # Create new student record

    new_student = pd.DataFrame([{

        "Student ID": student_id,

        "Student Name": student_name,

        "Student Email": student_email,

        "Supervisor": supervisor,

        "2nd Marker": marker

    }])



    # Add to existing list

    student_df = pd.concat(
        [
            student_df,
            new_student
        ],
        ignore_index=True
    )



    # Save Excel

    student_df.to_excel(
        student_file,
        index=False
    )



    return True, "Student added successfully."





# ================= GET STUDENT LIST ================= #

def get_students():

    create_student_file()


    df = pd.read_excel(
        student_file
    )


    return df





# ================= GET AVAILABLE SLOT ================= #

def get_available_slots(
    supervisor,
    marker
):


    if not os.path.exists(availability_file):

        return pd.DataFrame()



    availability_df = pd.read_excel(
        availability_file
    )


    availability_df.columns = (
        availability_df.columns.str.strip()
    )



    available = availability_df[

        (availability_df["Supervisor Name"] == supervisor)

        &

        (availability_df["2nd Marker Name"] == marker)

        &

        (availability_df["Status"] == "Available")

    ]


    return available





# ================= SAVE PRESENTATION SCHEDULE ================= #

def save_schedule(
    student_id,
    student_name,
    supervisor,
    marker,
    selected_slot
):


    # Read schedule file

    if os.path.exists(schedule_file):

        schedule_df = pd.read_excel(
            schedule_file
        )

    else:

        schedule_df = pd.DataFrame(

            columns=[

                "Student ID",
                "Student Name",
                "Supervisor",
                "2nd Marker",
                "Day",
                "Date",
                "Presentation Slot"

            ]

        )



    schedule_df.columns = (
        schedule_df.columns.str.strip()
    )



    # Check duplicate student


    if student_id in schedule_df["Student ID"].astype(str).values:


        return False, "Student already scheduled."





    new_schedule = pd.DataFrame([{


        "Student ID":
            student_id,


        "Student Name":
            student_name,


        "Supervisor":
            supervisor,


        "2nd Marker":
            marker,


        "Day":
            selected_slot["Day"],


        "Date":
            selected_slot["Date"],


        "Presentation Slot":
            selected_slot["Presentation Slot"]

    }])



    schedule_df = pd.concat(

        [

            schedule_df,

            new_schedule

        ],

        ignore_index=True

    )



    schedule_df.to_excel(

        schedule_file,

        index=False

    )





    # Update availability


    availability_df = pd.read_excel(

        availability_file

    )


    condition = (

        (availability_df["Supervisor Name"] == supervisor)

        &

        (availability_df["2nd Marker Name"] == marker)

        &

        (availability_df["Day"] == selected_slot["Day"])

        &

        (availability_df["Date"] == selected_slot["Date"])

        &

        (availability_df["Presentation Slot"] == selected_slot["Presentation Slot"])

    )



    availability_df.loc[
        condition,
        "Status"
    ] = "Not Available"



    availability_df.to_excel(

        availability_file,

        index=False

    )



    return True, "Presentation schedule created successfully."