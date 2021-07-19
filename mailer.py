import json
import os

import requests


class Mailer:
    """
    A mail server connection object for sending email notifications.

    Params:
        jobname:    The name of the job to be referenced in the emails.
    """

    def __init__(self, jobname):
        self.jobname = jobname
        self.mg_api_key = os.getenv("MG_API_KEY")
        self.mg_domain = os.getenv("MG_DOMAIN")
        self.mg_api_url = os.getenv("MG_API_URL")
        self.from_address = os.getenv("SENDER_EMAIL")
        self.to_address = os.getenv("RECIPIENT_EMAIL")

    def _subject_line(self):
        """Return formatted subject line based on error message content"""
        subject_type = "Error" if self.error_message else "Success"
        return f"{self.jobname} - {subject_type}"

    def _body_text(self):
        """Return formatted body text based on error message content."""
        if self.error_message:
            return f"{self.jobname} encountered an error.\n{self.error_message}"
        else:
            return f"{self.jobname} completed successfully."

    def _attachments(self):
        """Return list of attachments (in this case, logs)"""
        filename = "app.log"
        if os.path.exists(filename):
            return [("attachment", (filename, open(filename, "rb").read()))]

    def notify(self, error_message=None):
        """Send email success/error notifications using Mailgun API."""
        self.error_message = error_message
        requests.post(
            f"{self.mg_api_url}{self.mg_domain}/messages",
            auth=("api", self.mg_api_key),
            files=self._attachments(),
            data={
                "from": self.from_address,
                "to": self.to_address,
                "subject": self._subject_line(),
                "text": self._body_text(),
            },
        )