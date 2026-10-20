import smtplib
from email.message import EmailMessage


def send_outlook_email(receiver, subject, message):

    sender_email = "TP083606@mail.apu.edu.my"
    sender_password = "Thivyah@1503"


    email = EmailMessage()

    email["From"] = sender_email
    email["To"] = receiver
    email["Subject"] = subject

    email.set_content(message)


    server = smtplib.SMTP(
        "smtp.office365.com",
        587
    )

    server.starttls()

    server.login(
        sender_email,
        sender_password
    )

    server.send_message(email)

    server.quit()


    print("Email sent successfully")