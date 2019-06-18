import json
from flask import Blueprint

from services.stories_services import StoriesServices
from services.user_services import UserServices
from utils.helpers import construct_response_message

story = Blueprint('profile', __name__, url_prefix='/api/story')


@story.route('/', methods=['POST'])
@UserServices.check_user
def upload_stories(user):
    response = StoriesServices.save_stories()
    message = construct_response_message(message=response)
    return json.dumps(message)


@story.route('/', methods=['GET'])
@UserServices.check_user
def fetch_all_stories(user):
    response = StoriesServices.retrieve_all_stories()
    message = construct_response_message(message=response)
    return json.dumps(message)


