import json
from flask import Blueprint, request

from services.stories_services import StoryServices, CommentServices, LikeService, FileServices
from services.user_services import UserServices
from utils.helpers import construct_response_message

story = Blueprint('profile', __name__, url_prefix='/api/story')
comment = Blueprint('story', __name__, url_prefix='/api/comment')
like = Blueprint('like', __name__, url_prefix='/api/like')


@story.route('/', methods=['POST'])
@UserServices.check_user
def upload_stories(user):
    response = StoryServices.save_story()
    message = construct_response_message(message=response)
    return json.dumps(message)


@story.route('/', methods=['GET'])
@UserServices.check_user
def fetch_all_stories(user):
    response, next_cursor, more = StoryServices.retrieve_all_story(user)
    message = construct_response_message(
        message=response,
        next_cursor=next_cursor,
        more=more
    )
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


@like.route('/', methods=['GET'])
@UserServices.check_user
def update_like(user):
    status, count = LikeService.update_like()
    message = construct_response_message(
        status=status,
        count=count
    )
    return json.dumps(message)
