import base64
from email.mime.text import MIMEText

import dateutil.parser as parser
from apiclient import discovery
from bs4 import BeautifulSoup
from httplib2 import Http
from oauth2client import file, client, tools

# Creating a storage.JSON file with authentication details
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'  # we are using modify and not readonly, as we will be marking the messages Read
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

ME = 'me'
INBOX = 'INBOX'
UNREAD = 'UNREAD'


# Getting all the unread messages from Inbox
# labelIds can be changed accordingly

class GmailClient:
    def send_message(self, to, subject, message_text):
        try:
            msg = self._create_message(to, subject, message_text)
            message = GMAIL.users().messages().send(userId=to, body=message_text).execute()
            print('Message Id: %s' % message['id'])
            return message
        except Exception as error:
            print('An error occurred: %s' % error)
            raise error

    def fetch_unread(self, mark_as_read=False, limit=0):

        unread_msgs = GMAIL.users().messages().list(userId='me', labelIds=[INBOX, UNREAD], maxResults=limit).execute()

        # We get a dictonary. Now reading values for the key 'messages'
        mssg_list = unread_msgs['messages']

        print("Total unread messages in inbox: ", str(len(mssg_list)))

        final_list = []

        for mssg in mssg_list:
            temp_dict = {}
            m_id = mssg['id']  # get id of individual message
            message = GMAIL.users().messages().get(userId=ME, id=m_id).execute()  # fetch the message using API
            payld = message['payload']  # get payload of the message
            headr = payld['headers']  # get header of the payload

            for one in headr:  # getting the Subject
                if one['name'] == 'Subject':
                    msg_subject = one['value']
                    temp_dict['Subject'] = msg_subject
                else:
                    pass

            for two in headr:  # getting the date
                if two['name'] == 'Date':
                    msg_date = two['value']
                    date_parse = (parser.parse(msg_date))
                    m_date = (date_parse.date())
                    temp_dict['Date'] = str(m_date)
                else:
                    pass

            for three in headr:  # getting the Sender
                if three['name'] == 'From':
                    msg_from = three['value']
                    temp_dict['Sender'] = msg_from
                else:
                    pass

            temp_dict['Snippet'] = message['snippet']  # fetching message snippet

            try:

                # Fetching message body
                mssg_parts = payld['parts']  # fetching the message parts
                part_one = mssg_parts[0]  # fetching first element of the part
                part_body = part_one['body']  # fetching body of the message
                part_data = part_body['data']  # fetching data from the body
                clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
                clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
                clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
                soup = BeautifulSoup(clean_two, "lxml")
                mssg_body = soup.body()
                # mssg_body is a readible form of message body
                # depending on the end user's requirements, it can be further cleaned
                # using regex, beautiful soup, or any other method
                temp_dict['Message_body'] = mssg_body

            except:
                pass

            print(temp_dict)

            '''
            The final_list will have dictionary in the following format:
            {	'Sender': '"email.com" <name@email.com>', 
            	'Subject': 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet', 
            	'Date': 'yyyy-mm-dd', 
            	'Snippet': 'Lorem ipsum dolor sit amet'
            	'Message_body': 'Lorem ipsum dolor sit amet'}
            The dictionary can be exported as a .csv or into a databse
            '''
            final_list.append(temp_dict)  # This will create a dictionary item in the final list


            # This will mark the messagea as read
        print("Total messaged retrived: ", str(len(final_list)))
        if mark_as_read:
            GMAIL.users().messages().modify(userId=ME, id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()

    def _create_message(self, to, subject, message_text, sender=ME):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode())}
