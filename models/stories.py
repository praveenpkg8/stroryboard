import logging
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor


class Story(ndb.Model):
    story_id = ndb.StringProperty()
    name = ndb.StringProperty()
    user_name = ndb.StringProperty()
    story = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now=True)
    updated_on = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create_story(story):
        story_key = story.put()
        return story_key

    @staticmethod
    def get_all_story(cursor=None):
        _cursor = Cursor(urlsafe=cursor)
        stories = Story.query().order(-Story.created_on)
        story, next_cursor, more = stories.fetch_page(2, start_cursor=_cursor)
        next_cursor = next_cursor.urlsafe()
        return story, next_cursor, more

    @staticmethod
    def get_one_page_of_task(cursor=None):
        query = Story.query()
        objects, next_cursor, more = query.fetch_page(2, start_cursor=cursor)
        fire, next_cursor, more = query.fetch_page(2, start_cursor=next_cursor)
        # logging.info(query_iter)
        # page = next(query_iter.pages)
        #
        # tasks = list(page)
        # next_cursor = query_iter.next_page_token

        return fire, next_cursor, more


class Comment(ndb.Model):

    comment_id = ndb.StringProperty()
    story_id = ndb.StringProperty()
    user_name = ndb.StringProperty()
    name = ndb.StringProperty()
    comment = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now=True)
    updated_on = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create_comment(comment):
        comment_key = comment.put()
        return comment_key

    @staticmethod
    def get_all_comment(story_id, cursor=None):
        _cursor = Cursor(urlsafe=cursor)
        comments = Comment.query(Comment.story_id == story_id).order(-Comment.created_on)
        comment, next_cursor, more = comments.fetch_page(2, start_cursor=_cursor)
        if next_cursor is not None:
            next_cursor = next_cursor.urlsafe()
        return comment, next_cursor, more


