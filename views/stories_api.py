import json
import logging

from flask import Blueprint, request


from services.stories_services import StoryServices, CommentServices, LikeService
from services.user_services import UserServices
from utils.helpers import construct_response_message

story = Blueprint('profile', __name__, url_prefix='/api/story')
comment = Blueprint('story', __name__, url_prefix='/api/comment')
like = Blueprint('like', __name__, url_prefix='/api/like')


@story.route('/', methods=['POST'])
@UserServices.check_user
def upload_stories(user):
    if user:
        story_info = request.get_json()
        response, url = StoryServices.save_story(story_info)
        message = construct_response_message(
            message=response,
            url=url
        )
        return json.dumps(message)



@story.route('/', methods=['GET'])
@UserServices.check_user
def fetch_all_stories(user):
    request_next_cursor = request.args.get('next_cursor')
    response, next_cursor, more = StoryServices.retrieve_all_story(user, request_next_cursor)
    message = construct_response_message(
        message=response,
        next_cursor=next_cursor,
        more=more
    )
    return json.dumps(message)


@comment.route('/', methods=['POST'])
@UserServices.check_user
def upload_comment(user):
    comment_info = request.get_json()
    comments = CommentServices.save_comment(comment_info)
    message = construct_response_message(
        message=comments
         )
    return json.dumps(message)


@comment.route('/', methods=['GET'])
@UserServices.check_user
def get_comment(user):
    story_id = request.args.get('story_id')
    request_next_cursor = request.args.get('next_cursor')
    response, next_cursor, more = CommentServices.retrieve_all_comment(story_id, request_next_cursor)
    message = construct_response_message(
        comment=response,
        next_cursor=next_cursor,
        more=more
    )
    return json.dumps(message)


@like.route('/', methods=['GET'])
@UserServices.check_user
def update_like(user):
    story_id = request.args.get('story_id')
    mail = request.args.get('mail')
    status, count = LikeService.update_like(story_id, mail)
    message = construct_response_message(
        status=status,
        count=count
    )
    return json.dumps(message)





