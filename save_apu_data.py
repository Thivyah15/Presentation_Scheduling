import mysql.connector
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import os



# ==========================================
# Get Lecturer ID from MySQL
# ==========================================

def get_lect_id(staff_name):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="schedule"
    )


    cursor = conn.cursor(dictionary=True)


    cursor.execute(
        """
        SELECT lect_id 
        FROM staff 
        WHERE staff_name = %s
        """,
        (staff_name,)
    )


    row = cursor.fetchone()


    cursor.close()
    conn.close()



    if row:
        return row["lect_id"]

    else:
        return None





# ==========================================
# Retrieve timetable from APU
# Save as Excel
# ==========================================

def save_timetable(staff_name, week, file_path):


    lect_id = get_lect_id(staff_name)



    if lect_id is None:

        print(
            f"Staff '{staff_name}' not found."
        )

        return False




    url = "https://api.apiit.edu.my/timetable-print/index.php"



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