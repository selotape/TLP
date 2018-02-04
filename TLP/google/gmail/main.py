from typing import List

from gmail.util import *


def print_unread():
    service = get_service()
    messages_service = service.users().messages()
    results = messages_service.list(userId='me', q='is:unread').execute()
    unread_messages = results.get('messages', [])  # type: : List[dict]
    unread_ids = [msg['id'] for msg in unread_messages]
    for id_ in unread_ids:
        msg = messages_service.get(userId='me', id=id_).execute()
        print(msg)



def main():
    """
    outputs a list of label names
    of the user's Gmail account.
    """

    service = get_service()

    msg = create_message('me', 'me', 'testing', 'one-two-three')

    send_message(service, 'me', msg)


if __name__ == '__main__':
    main()
