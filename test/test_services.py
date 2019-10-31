import unittest

from models.auth_datastore import User

from services.auth_services import AuthServices
from services.stories_services import StoryServices, CommentServices, LikeService

from google.appengine.ext import ndb
from google.appengine.ext import testbed


class TestAuthServices(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_new_user(self):
        user_detials = {
            "name": 'praveen',
            "mail": 'pk@pk.com',
            "password": 'password'
        }
        message = AuthServices.new_user(user_detials)
        self.assertEqual('Account Created Successfully', message)

    def test_check_for_user(self):
        User(
            mail='pk@pk.com'
        ).put()
        user = AuthServices.check_for_user('pk@pk.com')
        self.assertEqual('pk@pk.com', user.mail)

    def test_google_oauth_new_user(self):
        user_info = {
            'name': 'praveen',
            'mail': 'pk@pk.com',
        }
        message = AuthServices.google_oauth_new_user(user_info)
        self.assertEqual('Account Created Successfully', message)

    def test_authenticate_user(self):
        user = {
            'name': 'tokyo',
            'mail': 'rio@tokyo.com'
        }
        session_id = AuthServices.authenticate_user(user)
        self.assertEqual(36, len(session_id))


class TestStoryService(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_save_story(self):
        story_info = {
            'name': 'jon snow',
            'mail': 'js@got.com',
            'story': 'king in the north'
        }
        story, url = StoryServices.save_story(story_info)
        self.assertEqual('js@got.com', story.get('mail'))

    def test_retrieve_all(self):
        user = {
            'name': 'jon snow',
            'mail': 'js@got.com'
        }
        story_info = {
            'name': 'jon snow',
            'mail': 'js@got.com',
            'story': 'king in the north'
        }
        StoryServices.save_story(story_info)
        StoryServices.save_story(story_info)
        StoryServices.save_story(story_info)
        StoryServices.save_story(story_info)
        story_entity = StoryServices.retrieve_all_story(user)
        self.assertEqual(True, story_entity[2])

    def test_update_like(self):
        story_info = {
            'name': 'jon snow',
            'mail': 'js@got.com',
            'story': 'king in the north'
        }
        story = StoryServices.save_story(story_info)
        like_count = StoryServices.update_like(story[0].get('story_id'), True)
        self.assertEqual(1, like_count)


class TestCommentServices(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_save_comment(self):
        comment_info = {
            'story_id': 'abc',
            'name': 'jon snow',
            'mail': 'js@got.com',
            'comment': 'I know nothing'
        }
        comment = CommentServices.save_comment(comment_info)
        self.assertEqual('js@got.com', comment.get('mail'))

    def test_retrieve_all_comment(self):
        comment_info = {
            'story_id': 'abc',
            'name': 'jon snow',
            'mail': 'js@got.com',
            'comment': 'I know nothing'
        }
        CommentServices.save_comment(comment_info)
        CommentServices.save_comment(comment_info)
        CommentServices.save_comment(comment_info)
        CommentServices.save_comment(comment_info)
        comment_entity = CommentServices.retrieve_all_comment('abc')
        self.assertEqual(True, comment_entity[2])


class TestLikeServices(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_update_like(self):
        story_info = {
            'name': 'jon snow',
            'mail': 'js@got.com',
            'story': 'king in the north'
        }
        story = StoryServices.save_story(story_info)
        like_entity = LikeService.update_like(story[0].get('story_id'), story[0].get('mail'))
        self.assertEqual(True, like_entity[0])



if __name__ == '__main__':
    unittest.main()
