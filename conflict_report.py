import pandas as pd
import os


def generate_conflict_report():

    # =====================================================
    # INPUT FILES
    # =====================================================

    student_file = "data/student.xlsx"
    schedule_file = "data/presentation_schedule.xlsx"
    availability_file = "data/common_availability.xlsx"


    # =====================================================
    # OUTPUT FILE
    # =====================================================

    conflict_report_file = "data/conflict_report.xlsx"


    # =====================================================
    # Check Files
    # =====================================================

    required_files = [
        student_file,
        schedule_file,
        availability_file
    ]


    for file in required_files:

        if not os.path.exists(file):

            return pd.DataFrame(
                columns=[
                    "Student ID",
                    "Student Name",
                    "Supervisor",
                    "2nd Marker",
                    "Conflict Type",
                    "Details"
                ]
            )


    # =====================================================
    # Read Excel Files
    # =====================================================

    student_df = pd.read_excel(student_file)

    schedule_df = pd.read_excel(schedule_file)

    availability_df = pd.read_excel(availability_file)



    # =====================================================
    # Clean Column Names
    # =====================================================

    student_df.columns = (
        student_df.columns
        .str.strip()
    )


    schedule_df.columns = (
        schedule_df.columns
        .str.strip()
    )


    availability_df.columns = (
        availability_df.columns
        .str.strip()
    )



    # =====================================================
    # Clean Data
    # =====================================================

    student_df["Student ID"] = (
        student_df["Student ID"]
        .astype(str)
        .str.strip()
    )


    schedule_df["Student ID"] = (
        schedule_df["Student ID"]
        .astype(str)
        .str.strip()
    )


    student_df["Supervisor"] = (
        student_df["Supervisor"]
        .astype(str)
        .str.strip()
    )


    student_df["2nd Marker"] = (
        student_df["2nd Marker"]
        .astype(str)
        .str.strip()
    )


    availability_df["Supervisor Name"] = (
        availability_df["Supervisor Name"]
        .astype(str)
        .str.strip()
    )


    if "2nd Marker Name" in availability_df.columns:

        availability_df["2nd Marker"] = (
            availability_df["2nd Marker Name"]
            .astype(str)
            .str.strip()
        )

    else:

        availability_df["2nd Marker"] = (
            availability_df["2nd Marker"]
            .astype(str)
            .str.strip()
        )


    availability_df["Status"] = (
        availability_df["Status"]
        .astype(str)
        .str.strip()
    )



    # =====================================================
    # Generate Conflict List
    # =====================================================

    conflict_list = []



    # Find students without assigned slots

    unscheduled_students = student_df[
        ~student_df["Student ID"].isin(
            schedule_df["Student ID"]
        )
    ]



    for _, student in unscheduled_students.iterrows():


        student_id = student["Student ID"]

        student_name = student["Student Name"]

        supervisor = student["Supervisor"]

        marker = student["2nd Marker"]



        # Check common availability

        available_slots = availability_df[

            (availability_df["Supervisor Name"] == supervisor)

            &

            (availability_df["2nd Marker"] == marker)

            &

            (availability_df["Status"] == "Available")

        ]



        if available_slots.empty:


            conflict_list.append({

                "Student ID": student_id,

                "Student Name": student_name,

                "Supervisor": supervisor,

                "2nd Marker": marker,

                "Conflict Type":
                "No Common Availability",

                "Details":
                "Supervisor and 2nd Marker do not have matching available slots."

            })


        else:


            conflict_list.append({

                "Student ID": student_id,

                "Student Name": student_name,

                "Supervisor": supervisor,

                "2nd Marker": marker,

                "Conflict Type":
                "Slot Not Assigned",

                "Details":
                "Available slot exists but no presentation slot assigned."

            })



    # =====================================================
    # Create DataFrame
    # =====================================================

    if len(conflict_list) > 0:

        conflict_df = pd.DataFrame(
            conflict_list
        )


    else:

        conflict_df = pd.DataFrame(

            columns=[

                "Student ID",
                "Student Name",
                "Supervisor",
                "2nd Marker",
                "Conflict Type",
                "Details"

            ]

        )



    # =====================================================
    # Save Excel Report
    # =====================================================

    conflict_df.to_excel(

        conflict_report_file,

        index=False

    )



    # Return data to Flask

    return conflict_df