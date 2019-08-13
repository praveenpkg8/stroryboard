import unittest

from models.auth_datastore import User, Tokens, Session
from models.contact import Contact
from models.stories import Story, Comment, Like
#
# from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class TestUserModels(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()
        pass

    def tearDown(self):
        self.testbed.deactivate()
        pass

    def test_user_creation(self):
        User().put()
        self.assertEqual(1, len(User.query().fetch()))
        pass

    def test_get_all_user(self):
        User(
            name="praveen",
            mail="pk@pk.com",
            password="password"
        ).put()
        self.assertEqual(1, len(User.get_all_user()))

    def test_user_by_mail(self):
        User(
            name="praveen",
            mail="pk@pk.com",
            password="password"
        ).put()
        user = User.user_by_mail("pk@pk.com")
        self.assertEqual("pk@pk.com", user.mail)


class TestTokenModel(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_token_creation(self):
        Tokens().put()
        self.assertEqual(1, len(Tokens.query().fetch()))

    def test_get_token(self):
        Tokens(
            token_id='abc'
        ).put()
        self.assertEqual('abc', Tokens.get_token('abc').token_id)


class TestSessionModel(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_session_creation(self):
        Session().put()
        self.assertEqual(1, len(Session.query().fetch()))

    def test_get_session(self):
        Session(
            session_id='abc'
        ).put()
        self.assertEqual('abc', Session.get_session('abc').session_id)

    def test_delete_session(self):
        Session(
            session_id='abc'
        ).put()
        session = Session.query(Session.session_id == 'abc').get()
        Session.delete_session(session)
        self.assertEqual(0, len(Session.query().fetch()))


class TestContactModel(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_contact_creation(self):
        Contact().put()
        self.assertEqual(1, len(Contact.query().fetch()))

    def test_get_contact_by_mail(self):
        Contact(
            email='pk@pk.com'
        ).put()
        self.assertEqual('pk@pk.com', Contact.get_contact_by_mail('pk@pk.com').email)

    def test_remove_contact(self):
        Contact(
            email='pk@pk.com'
        ).put()
        contact = Contact.query(Contact.email == 'pk@pk.com').get()
        Contact.remove_contact(contact)
        self.assertEqual(0, len(Contact.query().fetch()))


class TestStoryModel(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_story_creation(self):
        Story().put()
        self.assertEqual(1, len(Story.query().fetch()))

    def test_get_all_stories(self):
        Story().put()
        Story().put()
        Story().put()
        Story().put()
        story, next_cursor, more = Story.get_all_story()
        self.assertEqual(True, more)

    def test_get_story(self):
        Story(
            story_id='abc'
        ).put()
        story = Story.get_story('abc')
        self.assertEqual('abc', story.story_id)


class DatastoreTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_comment_creation(self):
        Comment().put()
        self.assertEqual(1, len(Comment.query().fetch()))

    def test_like_creation(self):
        Like().put()
        self.assertEqual(1, len(Like.query().fetch()))


if __name__ == '__main__':
    unittest.main()
