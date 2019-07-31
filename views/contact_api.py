
from flask import Blueprint, redirect, request
from google.appengine.api import taskqueue

from services.contact_services import ContactService
from services.user_services import UserServices
from status import Status

from config import frontend_config

contact = Blueprint('contact', __name__, url_prefix='/api/contact')


@contact.route('/oauth', methods=['GET'])
@UserServices.check_user
def contact_api(user):
    url = ContactService.access_code()
    return redirect(url)


@contact.route('/callback', methods=['GET'])
@UserServices.check_user
def contact_callback(user):
    tokens = ContactService.generate_tokens()
    taskqueue.add(
        url='/api/contact/fetch-contact',
        params={'access_token': tokens.get('access_token')},
        method='GET'
    )

    return redirect(frontend_config().get('frontend_url'))


@contact.route('/fetch-contact', methods=['GET'])
@UserServices.check_user
def fetch_contact(user):
    access_token = request.args.get('access_token')
    contact_list, reference = ContactService.fetch_all_contact(access_token)
    ContactService.store_contacts(contact_list, reference)
    return 'Invite sent successfully', Status.HTTP_200_OK


