from google.appengine.ext import ndb


class Stories(ndb.Model):
    name = ndb.StringProperty()
    user_name = ndb.StringProperty()
    story = ndb.StringProperty()
    time = ndb.TimeProperty(auto_now_add=True)
    created_on = ndb.DateTimeProperty(auto_now=True)
    updated_on = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create_story(story):
        story_key = story.put()
        return story_key

    @staticmethod
    def get_all_stories():
        stories = Stories.query().order(-Stories.created_on)
        return stories.fetch()
