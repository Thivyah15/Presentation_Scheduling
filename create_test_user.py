
from getpass import getpass
from werkzeug.security import generate_password_hash
from app import get_db_connection

email = input("Enter email address: ").strip().lower()
password = getpass("Enter password: ")
role = input("Enter role (student/lecturer): ").strip().lower()

if not email or not password:
    print("Email and password are required.")

elif role not in ("student", "lecturer"):
    print("Role must be student or lecturer.")

else:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        password_hash = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users (email, password_hash, role)
            VALUES (%s, %s, %s)
            """,
            (email, password_hash, role)
        )

        conn.commit()
        print("Test account created successfully.")

    except Exception as error:
        conn.rollback()
        print("Could not create account:", error)

    finally:
        cursor.close()
        conn.close()