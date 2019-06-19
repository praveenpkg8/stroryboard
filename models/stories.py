from google.appengine.ext import ndb


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
    def get_all_story():
        stories = Story.query().order(-Story.created_on)
        return stories.fetch()


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
    def get_all_comment(story_id):
        comments = Comment.query(Comment.story_id == story_id).order(-Comment.created_on)
        return comments.fetch()
