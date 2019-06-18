from flask import request

from models.stories import Stories
from utils.helpers import parse_all_stories


class StoriesServices(object):

    @staticmethod
    def save_stories():
        request_data = request.get_json()
        story = Stories(
            name=request_data.get('name'),
            user_name=request_data.get('user_name'),
            story=request_data.get('story')
        )
        message = Stories.create_story(story)
        return str(message)

    @staticmethod
    def retrieve_all_stories():
        stories = Stories.get_all_stories()
        _stories = parse_all_stories(stories)
        return _stories

