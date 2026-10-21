import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook


# ==========================================
# Get Lecturer ID from staff.xlsx
# ==========================================
def get_lect_id(staff_name):

    file = "data/staff.xlsx"

    if not os.path.exists(file):

        print("staff.xlsx not found.")

        return None


    staff = pd.read_excel(file)


    staff.columns = (
        staff.columns
        .str.strip()
    )


    staff["Staff Name"] = (
        staff["Staff Name"]
        .astype(str)
        .str.strip()
    )


    staff_name = staff_name.strip()


    result = staff.loc[
        staff["Staff Name"] == staff_name,
        "Lect ID"
    ]


    if not result.empty:

        return str(
            result.iloc[0]
        ).strip()


    else:

        return None


# ==========================================
# Retrieve timetable from APU
# Save as Excel
# ==========================================
def save_timetable(
        staff_name,
        week,
        file_path
):


    lect_id = get_lect_id(
        staff_name
    )


    if lect_id is None:

        print(
            f"Staff '{staff_name}' not found."
        )

        return False


    url = (
        "https://api.apiit.edu.my/timetable-print/index.php"
    )


    params = {

        "LectID": lect_id,

        "Submit": "Submit",

        "Week": week,

        "print_request": "print"

    }


    response = requests.get(
        url,
        params=params
    )


    response.raise_for_status()


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    rows = soup.find_all("tr")


    wb = Workbook()

    ws = wb.active

    ws.title = "Timetable"


    ws.append(
        [
            "Staff Name",
            "Date",
            "Time"
        ]
    )


    for tr in rows:


        cells = tr.find_all("td")


        if len(cells) >= 2:


            date = cells[0].get_text(
                strip=True
            )


            time = cells[1].get_text(
                strip=True
            )


            ws.append(
                [
                    staff_name,
                    date,
                    time
                ]
            )


    os.makedirs(
        "data",
        exist_ok=True
    )


    wb.save(
        file_path
    )


    print(
        f"{staff_name} timetable saved to {file_path}"
    )


    return True


# ==========================================
# Main function called by Flask
# ==========================================
def retrieve_timetable(
        staff_name,
        week,
        role
):


    if role == "supervisor":


        file_path = (
            "data/supervisor.xlsx"
        )


    elif role == "second_marker":


        file_path = (
            "data/second_marker.xlsx"
        )


    else:


        print(
            "Invalid timetable role."
        )

        return False


    result = save_timetable(
        staff_name,
        week,
        file_path
    )


    return result


# ==========================================
# Test without Flask
# ==========================================
if __name__ == "__main__":


    staff_name = input(
        "Enter Lecturer Name: "
    )


    week = input(
        "Enter Week (DD-MM-YYYY): "
    )


    role = input(
        "Enter Role (supervisor/second_marker): "
    )


    retrieve_timetable(
        staff_name,
        week,
        role
    )


    print(
        "Timetable retrieval completed."
    )