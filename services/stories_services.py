import uuid


from flask import request


from models.stories import Story, Comment, Like
from utils.helpers import parse_all_story, parse_all_comment, parse_update_story, parse_comment


class StoryServices(object):

    @staticmethod
    def save_story(story_info):
        story_id = uuid.uuid4().hex
        put_url = Story.file_sign(story_id)
        story = Story(
            story_id=story_id,
            name=story_info.get('name'),
            mail=story_info.get('mail'),
            story=story_info.get('story').strip()
        )
        message = Story.create_story(story)
        return parse_update_story(message), put_url

    @staticmethod
    def retrieve_all_story(user, request_next_cursor=None):
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
    def save_comment(comment_info):
        comment_id = uuid.uuid4().hex
        comment = Comment(
            comment_id=comment_id,
            story_id=comment_info.get('story_id'),
            name=comment_info.get('name'),
            mail=comment_info.get('mail'),
            comment=comment_info.get('comment')
        )
        message = Comment.create_comment(comment)

        return parse_comment(message)

    @staticmethod
    def retrieve_all_comment(story_id, request_next_cursor=None):
        comments, next_cursor, more = Comment.get_all_comment(story_id, request_next_cursor)
        comment = parse_all_comment(comments)
        return comment, next_cursor, more


class LikeService(object):

    @staticmethod
    def update_like(story_id, mail):
        like_key = Like.get_like(mail, story_id)
        if like_key is not None:
            Like.delete_like(like_key)
            count = StoryServices.update_like(story_id, False)
            return False, count
        else:
            like_id = uuid.uuid4().hex
            like = Like(
                like_id=like_id,
                story_id=story_id,
                mail=mail
            )
            count = StoryServices.update_like(story_id, True)
            Like.create_like(like)
            return True, count

