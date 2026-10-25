
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# ==============================
# LOAD TOKEN FROM .ENV
# ==============================
BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

token = os.getenv("API_TOKEN")

if not token:
    raise ValueError(
        "API_TOKEN not found. Check your .env file."
    )

# ==============================
# API SETTINGS
# ==============================
url = "https://api.apiit.edu.my/staff/listing"

headers = {
    "Authorization": f"Bearer {token}"
}

excel_file = BASE_DIR / "data" / "staff.xlsx"

# ==============================
# GET STAFF FROM API
# ==============================
try:
    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()
    staff_list = response.json()

except requests.RequestException as error:
    print("Failed to retrieve staff:", error)
    raise SystemExit(1)

if not isinstance(staff_list, list):
    raise ValueError("Unexpected API response format.")

print("Total staff from API:", len(staff_list))

# ==============================
# LOAD EXISTING STAFF
# ==============================
excel_file.parent.mkdir(parents=True, exist_ok=True)

if excel_file.exists():
    existing_df = pd.read_excel(excel_file)
    existing_df.columns = existing_df.columns.str.strip()
else:
    existing_df = pd.DataFrame(
        columns=["Lect ID", "Staff Name", "Email"]
    )

for column in ["Lect ID", "Staff Name", "Email"]:
    if column not in existing_df.columns:
        existing_df[column] = ""

existing_ids = set(
    existing_df["Lect ID"]
    .dropna()
    .astype(str)
    .str.strip()
)

new_staff = []
existing_staff = 0

# ==============================
# CHECK & ADD NEW STAFF
# ==============================
for staff in staff_list:
    lect_id = str(staff.get("CODE") or "").strip()
    staff_name = str(staff.get("FULLNAME") or "").strip()
    staff_email = str(staff.get("EMAIL") or "").strip()

    if not lect_id:
        continue

    if lect_id in existing_ids:
        existing_staff += 1
        continue

    new_staff.append({
        "Lect ID": lect_id,
        "Staff Name": staff_name,
        "Email": staff_email
    })

    existing_ids.add(lect_id)

# ==============================
# SAVE NEW STAFF
# ==============================
if new_staff:
    new_df = pd.DataFrame(new_staff)

    final_df = pd.concat(
        [existing_df, new_df],
        ignore_index=True
    )

    final_df.to_excel(excel_file, index=False)
    total_staff = len(final_df)
else:
    total_staff = len(existing_df)

# ==============================
# SUMMARY
# ==============================
print("==============================")
print("STAFF IMPORT COMPLETED")
print("==============================")
print(f"Existing staff skipped : {existing_staff}")
print(f"New staff added        : {len(new_staff)}")
print(f"Total staff in Excel   : {total_staff}")
