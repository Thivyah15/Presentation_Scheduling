import pandas as pd
from datetime import datetime, timedelta
import os



# ================= GENERATE TIME SLOTS ================= #

def generate_slots(start_date, end_date):

    slots = []

    current = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )


    while current <= end:

        time = datetime.strptime(
            "09:00 AM",
            "%I:%M %p"
        )


        finish = datetime.strptime(
            "05:00 PM",
            "%I:%M %p"
        )


        while time + timedelta(hours=1) <= finish:


            start = time.strftime(
                "%I:%M %p"
            )


            stop = (
                time + timedelta(hours=1)
            ).strftime(
                "%I:%M %p"
            )


            slots.append({

                "Date":
                    current.strftime("%Y-%m-%d"),

                "Presentation Slot":
                    f"{start} - {stop}"

            })


            time += timedelta(hours=1)


        current += timedelta(days=1)


    return pd.DataFrame(slots)





# ================= TIME CONVERSION ================= #

def convert_time(value):

    value = str(value).strip()


    if "AM" in value or "PM" in value:

        return datetime.strptime(
            value,
            "%I:%M %p"
        )


    return datetime.strptime(
        value,
        "%H:%M"
    )





# ================= CHECK BUSY ================= #

def check_busy(df, date, slot):


    start, end = slot.split(" - ")


    start = convert_time(start)

    end = convert_time(end)



    daily = df[
        df["Date"] == date
    ]



    for _, row in daily.iterrows():


        busy_start, busy_end = (
            row["Time"].split(" - ")
        )


        busy_start = convert_time(
            busy_start
        )


        busy_end = convert_time(
            busy_end
        )



        if (
            start < busy_end
            and
            end > busy_start
        ):

            return True



    return False





# ================= MAIN FUNCTION ================= #

def generate_common_availability():


    supervisor_file = (
        "data/supervisor.xlsx"
    )

    marker_file = (
        "data/second_marker.xlsx"
    )


    availability_file = (
        "data/common_availability.xlsx"
    )



    if not os.path.exists(supervisor_file):

        return pd.DataFrame()



    if not os.path.exists(marker_file):

        return pd.DataFrame()




    supervisor = pd.read_excel(
        supervisor_file
    )


    marker = pd.read_excel(
        marker_file
    )



    supervisor.columns = (
        supervisor.columns.str.strip()
    )


    marker.columns = (
        marker.columns.str.strip()
    )




    # ================= CLEAN DATE ================= #

    for df in [supervisor, marker]:


        df["Date"] = (

            df["Date"]
            .astype(str)
            .str.replace(
                r"^[A-Za-z]+",
                "",
                regex=True
            )
            .str.strip()

        )


        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d-%b-%y"
        ).dt.strftime(
            "%Y-%m-%d"
        )




    supervisor_name = (
        supervisor["Staff Name"].iloc[0]
    )


    marker_name = (
        marker["Staff Name"].iloc[0]
    )



    dates = pd.concat(
        [
            supervisor["Date"],
            marker["Date"]
        ]
    )



    slots = generate_slots(
        dates.min(),
        dates.max()
    )



    new_rows = []



    for _, row in slots.iterrows():


        date = row["Date"]

        slot = row["Presentation Slot"]



        if (
            not check_busy(
                supervisor,
                date,
                slot
            )

            and

            not check_busy(
                marker,
                date,
                slot
            )
        ):


            new_rows.append({

                "Supervisor Name":
                    supervisor_name,


                "2nd Marker Name":
                    marker_name,


                "Day":
                    datetime.strptime(
                        date,
                        "%Y-%m-%d"
                    ).strftime("%A"),


                "Date":
                    date,


                "Presentation Slot":
                    slot,


                "Status":
                    "Available"

            })



    new_data = pd.DataFrame(
        new_rows
    )




    # ================= KEEP OLD DATA ================= #

    if os.path.exists(availability_file):


        old = pd.read_excel(
            availability_file
        )


        old.columns = (
            old.columns.str.strip()
        )



        # keep old accepted/pending requests

        for i, row in new_data.iterrows():


            match = old[

                (old["Supervisor Name"] ==
                 supervisor_name)

                &

                (old["2nd Marker Name"] ==
                 marker_name)

                &

                (old["Date"] ==
                 row["Date"])

                &

                (old["Presentation Slot"] ==
                 row["Presentation Slot"])

            ]



            if not match.empty:


                status = (
                    match.iloc[0]["Status"]
                )


                if status != "Available":

                    new_data.loc[
                        i,
                        "Status"
                    ] = status





        # remove only old available
        # for current lecturer pair

        old = old[

            ~(
                (old["Supervisor Name"] ==
                 supervisor_name)

                &

                (old["2nd Marker Name"] ==
                 marker_name)

                &

                (old["Status"] ==
                 "Available")
            )

        ]



        final = pd.concat(
            [
                old,
                new_data
            ],
            ignore_index=True
        )



    else:

        final = new_data




    # ================= REMOVE DUPLICATES ================= #

    final = final.drop_duplicates(

        subset=[

            "Supervisor Name",

            "2nd Marker Name",

            "Date",

            "Presentation Slot"

        ]

    )




    # ================= SORT ================= #

    final["SortDate"] = pd.to_datetime(
        final["Date"]
    )


    final["SortTime"] = pd.to_datetime(

        final["Presentation Slot"]
        .str.split(" - ")
        .str[0],

        format="%I:%M %p"

    )



    # GROUP BY LECTURER PAIR FIRST

    final = final.sort_values(

        by=[

            "Supervisor Name",

            "2nd Marker Name",

            "SortDate",

            "SortTime"

        ]

    )



    final = final.drop(
        columns=[
            "SortDate",
            "SortTime"
        ]
    )



    # ================= SAVE ================= #

    os.makedirs(
        "data",
        exist_ok=True
    )


    final.to_excel(
        availability_file,
        index=False
    )


    return final