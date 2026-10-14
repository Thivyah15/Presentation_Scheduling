import pandas as pd
import os


# ================= FILE LOCATION ================= #

availability_file = "data/common_availability.xlsx"
schedule_file = "data/presentation_schedule.xlsx"
utilization_file = "data/staff_utilization_report.xlsx"



# ================= GENERATE UTILIZATION REPORT ================= #

def generate_utilization_report():


    # ================= CHECK FILES ================= #

    if not os.path.exists(availability_file):

        empty_df = pd.DataFrame()

        return empty_df, empty_df



    if not os.path.exists(schedule_file):

        empty_df = pd.DataFrame()

        return empty_df, empty_df



    # ================= READ EXCEL FILES ================= #

    availability_df = pd.read_excel(
        availability_file
    )


    schedule_df = pd.read_excel(
        schedule_file
    )



    # Remove spaces from columns

    availability_df.columns = (
        availability_df.columns
        .str.strip()
    )


    schedule_df.columns = (
        schedule_df.columns
        .str.strip()
    )



    # ================= CHECK DATA ================= #

    if availability_df.empty or schedule_df.empty:

        empty_df = pd.DataFrame()

        return empty_df, empty_df



    # =====================================================
    # SUPERVISOR UTILIZATION
    # =====================================================


    # Total available slots

    supervisor_total = (

        availability_df
        .groupby("Supervisor Name")
        .size()
        .reset_index(
            name="Total Slots"
        )

    )



    # Assigned presentation slots

    supervisor_assigned = (

        schedule_df
        .groupby("Supervisor")
        .size()
        .reset_index(
            name="Assigned Slots"
        )

    )



    # Merge data

    supervisor_utilization = pd.merge(

        supervisor_total,

        supervisor_assigned,

        left_on="Supervisor Name",

        right_on="Supervisor",

        how="left"

    )



    supervisor_utilization["Assigned Slots"] = (

        supervisor_utilization["Assigned Slots"]
        .fillna(0)
        .astype(int)

    )



    # Remaining slots

    supervisor_utilization["Remaining Slots"] = (

        supervisor_utilization["Total Slots"]

        -

        supervisor_utilization["Assigned Slots"]

    )



    # Utilization %

    supervisor_utilization["Utilization (%)"] = (

        supervisor_utilization["Assigned Slots"]

        /

        supervisor_utilization["Total Slots"]

        *

        100

    ).round(2)



    supervisor_utilization = supervisor_utilization[

        [

            "Supervisor Name",

            "Total Slots",

            "Assigned Slots",

            "Remaining Slots",

            "Utilization (%)"

        ]

    ]



    supervisor_utilization.rename(

        columns={

            "Supervisor Name":
            "Supervisor"

        },

        inplace=True

    )



    # =====================================================
    # 2ND MARKER UTILIZATION
    # =====================================================


    # Total available slots

    marker_total = (

        availability_df
        .groupby("2nd Marker Name")
        .size()
        .reset_index(
            name="Total Slots"
        )

    )



    # Assigned slots

    marker_assigned = (

        schedule_df
        .groupby("2nd Marker")
        .size()
        .reset_index(
            name="Assigned Slots"
        )

    )



    # Merge data

    marker_utilization = pd.merge(

        marker_total,

        marker_assigned,

        left_on="2nd Marker Name",

        right_on="2nd Marker",

        how="left"

    )



    marker_utilization["Assigned Slots"] = (

        marker_utilization["Assigned Slots"]
        .fillna(0)
        .astype(int)

    )



    # Remaining slots

    marker_utilization["Remaining Slots"] = (

        marker_utilization["Total Slots"]

        -

        marker_utilization["Assigned Slots"]

    )



    # Utilization %

    marker_utilization["Utilization (%)"] = (

        marker_utilization["Assigned Slots"]

        /

        marker_utilization["Total Slots"]

        *

        100

    ).round(2)



    marker_utilization = marker_utilization[

        [

            "2nd Marker Name",

            "Total Slots",

            "Assigned Slots",

            "Remaining Slots",

            "Utilization (%)"

        ]

    ]



    marker_utilization.rename(

        columns={

            "2nd Marker Name":
            "2nd Marker"

        },

        inplace=True

    )



    # =====================================================
    # SAVE EXCEL REPORT
    # =====================================================


    with pd.ExcelWriter(

        utilization_file,

        engine="openpyxl"

    ) as writer:


        supervisor_utilization.to_excel(

            writer,

            sheet_name="Supervisor Utilization",

            index=False

        )


        marker_utilization.to_excel(

            writer,

            sheet_name="2nd Marker Utilization",

            index=False

        )



    # Return data to Flask

    return supervisor_utilization, marker_utilization