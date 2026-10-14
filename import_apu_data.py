import requests
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="schedule"
)

cursor = conn.cursor()

url = "https://api.apiit.edu.my/staff/listing"

headers = {
    "Authorization": 
"Bearer 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"
}
response = requests.get(url, headers=headers)
staff_list = response.json()
print("Total staff from API:", len(staff_list))

sql_check = """
SELECT lect_id 
FROM staff
WHERE lect_id = %s
"""


sql_insert = """
INSERT INTO staff (lect_id, staff_name, email)
VALUES (%s, %s, %s)
"""


new_staff = 0
existing_staff = 0


for staff in staff_list:
    lect_id = staff["CODE"]
    staff_name = staff["FULLNAME"].strip()

    staff_email = staff.get("EMAIL")

    if staff_email:
        staff_email = staff_email.strip()
    else:
        staff_email = None


    # Check existing staff
    cursor.execute(
        sql_check,
        (lect_id,)
    )

    result = cursor.fetchone()


    if result:

        # Already exist
        existing_staff += 1

    else:

        # Insert new staff
        cursor.execute(
            sql_insert,
            (
                lect_id,
                staff_name, 
                staff_email
            )
        )

        new_staff += 1



conn.commit()


cursor.close()
conn.close()


print("==============================")
print("STAFF IMPORT COMPLETED")
print("==============================")

print(f"Existing staff skipped : {existing_staff}")
print(f"New staff added        : {new_staff}")