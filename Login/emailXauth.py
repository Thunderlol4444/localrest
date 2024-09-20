from __future__ import print_function

import base64
import os.path
import random
import smtplib

from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

# user token storage
USER_TOKENS = 'token.json'

# application credentials
CREDENTIALS = r'C:\Users\Thunder\PycharmProjects\localHostTesting\credentials.json'


def get_token() -> str:
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(USER_TOKENS):
        creds = Credentials.from_authorized_user_file(USER_TOKENS, SCOPES)
        creds.refresh(Request())
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(USER_TOKENS, 'w') as token:
            token.write(creds.to_json())

    return creds.token


def generate_oauth2_string(username, access_token) -> str:
    auth_string = 'user=' + username + '\1auth=Bearer ' + access_token + '\1\1'
    return base64.b64encode(auth_string.encode('ascii')).decode('ascii')


def send_email(host, port, subject, msg, sender, recipients):
    access_token = get_token()
    auth_string = generate_oauth2_string(sender, access_token)

    msg = MIMEText(msg)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    server = smtplib.SMTP(host, port)
    server.starttls()
    server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()


def main():
    OTP = random.randint(1000, 9999)
    host = "smtp.gmail.com"
    port = 587

    user = "jasonsimsamsung@gmail.com"
    recipient = "211153@student.upm.edu.my"
    subject = "Test email Oauth2"
    msg = f"Hello world {OTP}"
    sender = user
    recipients = [recipient]
    send_email(host, port, subject, msg, sender, recipients)


if __name__ == '__main__':
    main()
