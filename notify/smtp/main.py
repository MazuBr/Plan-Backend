import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

sender = "matvsudev@gmail.com"
password = os.getenv("EMAIL_PASS")


def send_email(reciever, subject, body):
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = reciever
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            text = message.as_string()
            server.sendmail(sender, reciever, text)
            print("Ok")
    except Exception as e:
        print(f"Ошибка при отправке сообщения {e}")
