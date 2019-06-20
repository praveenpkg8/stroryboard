from flask import request
import uuid

from models.stories import Story, Comment
from utils.helpers import parse_all_story, parse_all_comment


class StoryServices(object):

    @staticmethod
    def save_story():
        story_id = uuid.uuid4().hex
        request_data = request.get_json()
        story = Story(
            story_id=story_id,
            name=request_data.get('name'),
            user_name=request_data.get('user_name'),
            story=request_data.get('story')
        )
        message = Story.create_story(story)
        return str(message)

    @staticmethod
    def retrieve_all_story():
        request_next_cursor = request.args.get('next_cursor')
        stories, next_cursor, more = Story.get_all_story(request_next_cursor)
        _stories = parse_all_story(stories)
        return _stories, next_cursor, more

    @staticmethod
    def pagination_check():
        return Story.get_one_page_of_task()


class CommentServices(object):

    @staticmethod
    def save_comment():
        comment_id = uuid.uuid4().hex
        request_data = request.get_json()
        comment = Comment(
            comment_id=comment_id,
            story_id=request_data.get('story_id'),
            name=request_data.get('name'),
            user_name=request_data.get('user_name'),
            comment=request_data.get('comment')
        )
        message = Comment.create_comment(comment)
        return message

    @staticmethod
    def retrieve_all_comment(story_id):
        cursor = request.args.get('next_cursor')
        comments, next_cursor, more = Comment.get_all_comment(story_id, cursor)
        comment = parse_all_comment(comments)
        return comment, next_cursor, more


