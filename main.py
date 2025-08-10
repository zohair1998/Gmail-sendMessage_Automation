import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, body_text):
    message = MIMEText(body_text, 'plain')  
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(service, sender, to, subject, body):
    message = create_message(sender, to, subject, body)
    service.users().messages().send(userId='me', body=message).execute()

def main():
    recipients = [
        "email1@nomail.com",
        "email2@nomail.com",
        "email3@nomail.com",
        "email4@nomail.com"
    ]

    service = get_gmail_service()
    sender = "zohair@gmail.com"
    subject = "My first automated email "
    body = """Hello,

This is a test message from API program.
Best,
Zohair

"""

    for recipient in recipients:
        send_email(service, sender, recipient, subject, body)
        print(f"Email sent to {recipient} successfully")

if __name__ == '__main__':
    main()
