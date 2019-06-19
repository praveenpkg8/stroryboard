import json
from flask import Blueprint

from services.stories_services import StoryServices, CommentServices
from services.user_services import UserServices
from utils.helpers import construct_response_message

story = Blueprint('profile', __name__, url_prefix='/api/story')
comment = Blueprint('story', __name__, url_prefix='/api/comment')


@story.route('/', methods=['POST'])
@UserServices.check_user
def upload_stories(user):
    response = StoryServices.save_story()
    message = construct_response_message(message=response)
    return json.dumps(message)


@story.route('/', methods=['GET'])
@UserServices.check_user
def fetch_all_stories(user):
    response = StoryServices.retrieve_all_story()
    message = construct_response_message(message=response)
    return json.dumps(message)


@comment.route('/', methods=['POST'])
@UserServices.check_user
def upload_comment(user):
    response = CommentServices.save_comment()
    message = construct_response_message(message=str(response))
    return json.dumps(message)

