import os.path

import base64
from collections import defaultdict

from time import sleep
from summerizer import nlp_parse
from parser import parse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def parse_email(email):
    pass


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['Label_1481308289868124811'],
                                                  q='is:unread').execute()
        messages = results.get('messages', [])
        # results = service.users().labels().list(userId='me').execute()
        # labels = results.get('labels', [])

        if not messages:
            print('No messages found.')
            return
        # response = defaultdict(list)
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            email_data = msg["payload"]["headers"]
            print(msg['snippet'])
            for values in email_data:
                name = values["name"]
                if name == "From":
                    from_name = values["value"]
                    subject = [j["value"] for j in email_data if j["name"] == "Subject"]
                    print(from_name, subject)
            for p in msg["payload"]["parts"]:
                sleep(2)
                if p["mimeType"] == "text/html":
                    body = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8").strip()
                    nlp_parse(parse(body))
                    # response[msg['snippet']].append(nlp_parse(parse(body)))

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
