import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


# ======================================
# PROJECT SETTINGS
# ======================================
BASE_DIR = Path(__file__).resolve().parent
EXCEL_FILE = BASE_DIR / "data" / "staff.xlsx"
API_URL = "https://api.apiit.edu.my/staff/listing"


# ======================================
# LOAD API TOKEN
# ======================================
load_dotenv(BASE_DIR / ".env")

token = os.getenv("API_TOKEN")

if not token:
    raise ValueError(
        "API_TOKEN was not found in the .env file."
    )

token = token.strip()


headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}


# ======================================
# RETRIEVE STAFF FROM API
# ======================================
try:

    response = requests.get(
        API_URL,
        headers=headers,
        timeout=30
    )

    if response.status_code != 200:

        print("API Error:")
        print(response.text)

        response.raise_for_status()


    staff_list = response.json()


except requests.Timeout:

    print("API request timed out.")
    raise SystemExit(1)


except requests.RequestException as error:

    print("Failed to retrieve staff:", error)
    raise SystemExit(1)


except ValueError:

    print("Invalid API response format.")
    raise SystemExit(1)



# ======================================
# VALIDATE API RESPONSE
# ======================================
if not isinstance(staff_list, list):

    print("Unexpected API response.")
    raise SystemExit(1)


print(f"Retrieved {len(staff_list)} staff records.")



# ======================================
# LOAD EXISTING STAFF EXCEL
# ======================================
EXCEL_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


if EXCEL_FILE.exists():

    existing_df = pd.read_excel(EXCEL_FILE)

else:

    existing_df = pd.DataFrame(
        columns=[
            "Lect ID",
            "Staff Name",
            "Email"
        ]
    )


existing_df.columns = (
    existing_df.columns
    .str.strip()
)


for column in [
    "Lect ID",
    "Staff Name",
    "Email"
]:

    if column not in existing_df.columns:

        existing_df[column] = ""


existing_df = existing_df[
    [
        "Lect ID",
        "Staff Name",
        "Email"
    ]
]


existing_ids = set(
    existing_df["Lect ID"]
    .astype(str)
    .str.strip()
)



# ======================================
# PROCESS STAFF DATA
# ======================================
new_staff = []
existing_staff = 0


for staff in staff_list:


    if not isinstance(staff, dict):
        continue


    lect_id = str(
        staff.get("CODE", "")
    ).strip()


    staff_name = str(
        staff.get("FULLNAME", "")
    ).strip()


    email = str(
        staff.get("EMAIL", "")
    ).strip()



    if not lect_id:
        continue



    if lect_id in existing_ids:

        existing_staff += 1
        continue



    new_staff.append(
        {
            "Lect ID": lect_id,
            "Staff Name": staff_name,
            "Email": email
        }
    )


    existing_ids.add(lect_id)



# ======================================
# SAVE STAFF TO EXCEL
# ======================================
if new_staff:


    new_df = pd.DataFrame(new_staff)


    final_df = pd.concat(
        [
            existing_df,
            new_df
        ],
        ignore_index=True
    )


else:

    final_df = existing_df



final_df.to_excel(
    EXCEL_FILE,
    index=False
)



# ======================================
# IMPORT SUMMARY
# ======================================
print()

print("=" * 40)
print("STAFF IMPORT COMPLETED")
print("=" * 40)

print(f"Existing staff skipped : {existing_staff}")
print(f"New staff added        : {len(new_staff)}")
print(f"Total staff            : {len(final_df)}")
print(f"Excel file             : {EXCEL_FILE}")

print("=" * 40)