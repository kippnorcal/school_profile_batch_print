import smtplib
import os


GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PWD = os.getenv("GMAIL_PWD")
SLACK_EMAIL = os.getenv("SLACK_EMAIL")

def notify(school, count):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(GMAIL_USER, GMAIL_PWD)
    subject = "Subject: Tableau Batch Print - Success"
    text = f"The Student Profile Batch Printer created {count} profiles for {school}"
    message = f"{subject}\n\n{text}"
    server.sendmail(GMAIL_USER, SLACK_EMAIL, message)
    server.quit()
