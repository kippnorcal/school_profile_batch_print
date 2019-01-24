import smtplib
import os


GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PWD = os.getenv("GMAIL_PWD")
SLACK_EMAIL = os.getenv("SLACK_EMAIL")

def notify(school, count, error=False, error_message=None):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(GMAIL_USER, GMAIL_PWD)
    if error:
        subject = "Tableau Batch Print - Error"
        text = f"The Student Profile Batch Printer encountered an error:\n{error_message}"
        message = f"Subject: {subject}\n\n{text}"
    else:
        subject = "Tableau Batch Print - Success"
        text = f"The Student Profile Batch Printer created {count} profiles for {school}"
        message = f"Subject: {subject}\n\n{text}"
    server.sendmail(GMAIL_USER, SLACK_EMAIL, message)
    server.quit()
