import os
from typing import List
from requests import post, Response


class MailgunException(Exception):
    def __init__(self, message):
        self.message = message


class Mailgun():

    FROM_TITLE = "Pricing service"
    FROM_EMAIL = "do-not-reply@sandbox6ecc4b8cc3e54a739ed5bcac3c989ae7.mailgun.org"

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)
        if api_key is None:
            raise MailgunException('Failed to load Mailgun API KEY')
        if domain is None:
            raise MailgunException('Failed to load Mailgun Domain')
        response = post(
            f"{domain}/messages",
            auth=("api", api_key),
            data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html})
        if response.status_code != 200:
            print(response.json())
            raise MailgunException('An error ocurred while sending email')
        return response
