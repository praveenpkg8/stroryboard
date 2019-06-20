import json
from flask import Blueprint, request

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
    response, next_cursor, more = StoryServices.retrieve_all_story()
    message = construct_response_message(
        message=response,
        next_cursor=next_cursor,
        more=more
    )
    return json.dumps(message)


@story.route('/page', methods=['GET'])
@UserServices.check_user
def fetch_all_page(user):
    response = StoryServices.pagination_check()
    message = construct_response_message(message=str(response))
    return json.dumps(message)


@comment.route('/', methods=['POST'])
@UserServices.check_user
def upload_comment(user):
    response = CommentServices.save_comment()
    message = construct_response_message(message=str(response))
    return json.dumps(message)


@comment.route('/', methods=['GET'])
@UserServices.check_user
def get_comment(user):
    story_id = request.args.get('story_id');
    response, next_cursor, more = CommentServices.retrieve_all_comment(story_id)
    message = construct_response_message(
        message=response,
        next_cursor=next_cursor,
        more=more
    )
    return json.dumps(message)

