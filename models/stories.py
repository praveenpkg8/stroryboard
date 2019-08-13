from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
import datetime


class Story(ndb.Model):
    story_id = ndb.StringProperty()
    name = ndb.StringProperty()
    mail = ndb.StringProperty()
    story = ndb.StringProperty()
    like_count = ndb.IntegerProperty(default=0)
    created_on = ndb.DateTimeProperty(auto_now=True)
    updated_on = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create_story(story):
        story_key = story.put()
        return story_key.get()

    @staticmethod
    def get_all_story(cursor=None):
        _cursor = Cursor(urlsafe=cursor)
        stories = Story.query().order(-Story.created_on)
        story, next_cursor, more = stories.fetch_page(3, start_cursor=_cursor)
        next_cursor = next_cursor.urlsafe() if next_cursor is not None else next_cursor
        return story, next_cursor, more

    @staticmethod
    def get_story(story_id):
        story = Story.query(Story.story_id == story_id).get()
        return story

    @staticmethod
    def update_story(story):
        story.put()

    @staticmethod
    def file_sign(story_id):

        # from google.cloud import storage
        #
        # storage_client = storage.Client()
        # bucket = storage_client.get_bucket("full-services.appspot.com")
        #
        # blob = bucket.blob("story/" + story_id + ".jpg")
        # url = blob.generate_signed_url(
        #     version='v4',
        #     expiration=datetime.timedelta(minutes=30),
        #     method='PUT',
        # )
        # return url
        return None


class Comment(ndb.Model):
    comment_id = ndb.StringProperty()
    story_id = ndb.StringProperty()
    mail = ndb.StringProperty()
    name = ndb.StringProperty()
    comment = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now=True)
    updated_on = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create_comment(comment):
        comment_key = comment.put()
        return comment_key.get()

    @staticmethod
    def get_all_comment(story_id, cursor=None):
        _cursor = Cursor(urlsafe=cursor)
        comments = Comment.query(Comment.story_id == story_id).order(-Comment.created_on)
        comment, next_cursor, more = comments.fetch_page(2, start_cursor=_cursor)
        if next_cursor is not None:
            next_cursor = next_cursor.urlsafe()
        return comment, next_cursor, more


class Like(ndb.Model):
    like_id = ndb.StringProperty()
    story_id = ndb.StringProperty()
    mail = ndb.StringProperty()
    is_active = ndb.BooleanProperty(default=True)

    @staticmethod
    def create_like(like):
        like_key = like.put()
        return like_key

    @staticmethod
    def get_like(mail, story_id):
        like = Like.query(Like.mail == mail, Like.story_id == story_id).get()
        return like

    @staticmethod
    def delete_like(like):
        like.key.delete()
