import json

from flask import request

from google.appengine.api import urlfetch
from google.appengine.api import mail

from urllib import urlencode

from services.google_auth_services import GoogleAuthServices
from config import dict_formation, load_config
from models.contact import Contact


class ContactService(object):

    @staticmethod
    def access_code():
        url = GoogleAuthServices.get_access_code(
            scope='https://www.googleapis.com/auth/contacts.readonly',
            prompt='consent',
            redirect='contact'
        )
        return url

    @staticmethod
    def generate_tokens():
        code = request.args.get('code')
        CONFIG = load_config()
        params = dict_formation(
            code=code,
            client_id=CONFIG.get('client_id'),
            client_secret=CONFIG.get('client_secret'),
            redirect_uri=CONFIG.get('redirect_uris')[2],
            grant_type='authorization_code'
        )
        url = 'https://www.googleapis.com/oauth2/v4/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        res = urlfetch.fetch(url, method='POST',
                             payload=urlencode(params), headers=headers)

        tokens = res.content
        return json.loads(tokens)

    @staticmethod
    def fetch_all_contact(access_token):
        url = 'https://www.google.com/m8/feeds/contacts/default/full?alt=json&max-results=25000&v=3.0'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        res = urlfetch.fetch(url, method='GET',
                             headers=headers)
        contact = json.loads(res.content)
        return contact.get('feed').get('entry'), contact.get('feed').get('id').get('$t')

    @staticmethod
    def store_contacts(contact_list, reference):

        for contact in contact_list:

            if contact.get('gd$email') is None:
                continue

            name = contact.get('title').get('$t')
            email = contact.get('gd$email')[0].get('address')
            contact = Contact.get_contact_by_mail(email)

            if contact is None:
                _contact = Contact(
                    name=name,
                    email=email,
                    reference=reference
                )
                Contact.create_contact(_contact)

        ContactService.mail_to_contact("praveen", "praveensetu@gmail.com")

    @staticmethod
    def mail_to_contact(name, email):

        sender_address = 'admin@full-services.appspotmail.com'

        message = mail.EmailMessage(
            sender=sender_address,
            subject="Your account has been approved")

        message.to = email
        message.body = """Dear """ + name + """:

            Demo
            Your example.com account has been approved.  You can now visit
            http://www.example.com/ and sign in using your Google Account to
            access new features.
            Please let us know if you have any questions.
            The example.com Team
            """
        message.send()
