import os
import subprocess
import sys

def display_menu():
    os.system("cls" if os.name == "nt" else "clear")

    print("\n")
    print("=" * 58)
    print("     AUTOMATED PRESENTATION SCHEDULING SYSTEM")
    print("=" * 58)

    print("1. Retrieve APU Staff Timetable")
    print("2. Generate Common Availability")
    print("3. Manage Students & Assign Presentation")
    print("4. Generate Conflict Report")
    print("5. Generate Workload Report")
    print("6. Generate Staff Utilization Report")
    print("7. Exit")

    print("=" * 58)

while True:
    display_menu()

    choice = input(
        "\nEnter your choice: "
    ).strip()

    print()

    if choice == "1":
        subprocess.run(
            [sys.executable, "save_apu_data.py"]
        )

    elif choice == "2":
        subprocess.run(
            [sys.executable, "find_common_availability.py"]
        )

    elif choice == "3":
        subprocess.run(
            [sys.executable, "update_availability.py"]
        )

    elif choice == "4":
        subprocess.run(
            [sys.executable, "conflict_report.py"]
        )

    elif choice == "5":
        subprocess.run(
            [sys.executable, "workload_report.py"]
        )

    elif choice == "6":
        subprocess.run(
            [sys.executable, "staff_utilization_report.py"]
        )

    elif choice == "7":
        print("\nThank you for using the")
        print("Automated Presentation Scheduling System.")
        break

    else:
        print("\nInvalid option. Please try again.")
    
    input("\nPress Enter to return to the main menu...")