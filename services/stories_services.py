from flask import request
import uuid

from models.stories import Story, Comment, Like
from utils.helpers import parse_all_story, parse_all_comment


class StoryServices(object):

    @staticmethod
    def save_story():
        story_id = uuid.uuid4().hex
        request_data = request.get_json()
        put_url = Story.file_sign(story_id)
        story = Story(
            story_id=story_id,
            name=request_data.get('name'),
            user_name=request_data.get('user_name'),
            story=request_data.get('story')
        )
        message = Story.create_story(story)
        return put_url

    @staticmethod
    def retrieve_all_story(user):
        request_next_cursor = request.args.get('next_cursor')
        stories, next_cursor, more = Story.get_all_story(request_next_cursor)
        if stories is not None:
            _stories = parse_all_story(stories, user)
        return _stories, next_cursor, more

    @staticmethod
    def update_like(story_id, flag):
        story = Story.get_story(story_id)
        if flag:
            story.like_count += 1
        else:
            story.like_count -= 1
        Story.update_story(story)
        return story.like_count


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


class LikeService(object):

    @staticmethod
    def update_like():
        story_id = request.args.get('story_id')
        user_name = request.args.get('user_name')
        like_key = Like.get_like(user_name, story_id)
        if like_key is not None:
            Like.delete_like(like_key)
            count = StoryServices.update_like(story_id, False)
            return False, count
        else:
            like_id = uuid.uuid4().hex
            like = Like(
                like_id=like_id,
                story_id=story_id,
                user_name=user_name
            )
            count = StoryServices.update_like(story_id, True)
            like_key = Like.create_like(like)
            return True, count


class FileServices(object):

    @staticmethod
    def sign_url():
        comment_file = Comment.file_sign()
        return comment_file
