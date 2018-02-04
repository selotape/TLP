import time

from TLP.google.gmail.client import GmailClient


def test_send_email():
    client = GmailClient()
    client.send_message('me', 'this is the subject', 'this is the body')
    time.sleep(10)
    messages = client.fetch_unread(limit=1)
    assert any('this is the subject' == msg.title for msg in messages)
    assert any('this is the body' in msg.body for msg in messages)
