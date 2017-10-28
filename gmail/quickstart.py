import argparse
import os
from typing import List

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()  # If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def print_unread():
    service = get_service()
    messages_service = service.users().messages()
    results = messages_service.list(userId='me', q='is:unread').execute()
    unread_messages = results.get('messages', [])  # type: : List[dict]
    unread_ids = [msg['id'] for msg in unread_messages]
    for id_ in unread_ids:
        msg = messages_service.get(userId='me', id=id_).execute()
        print(msg)



def get_service():
    """Creates a Gmail API service """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('gmail', 'v1', http=http)


def main1():
    print_unread()

def main2():
    """
    outputs a list of label names
    of the user's Gmail account.
    """

    service = get_service()



    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


if __name__ == '__main__':
    main1()
