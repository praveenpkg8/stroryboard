from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    user_name = ndb.StringProperty()
    mail = ndb.StringProperty()
    password = ndb.StringProperty()
    mobile_number = ndb.StringProperty()

    @staticmethod
    def create_user(user):
        user_key = user.put()
        return user_key

    @staticmethod
    def get_all_user():
        users = User.query()
        return users.fetch()

    @staticmethod
    def user_by_username(username):
        user = User.query(User.user_name == username).fetch()
        return user


class Session(ndb.Model):
    session_id = ndb.StringProperty()
    user_name = ndb.StringProperty()
    name = ndb.StringProperty()

    @staticmethod
    def create_session(session):
        ses = session.put()
        return ses

    @staticmethod
    def get_session(_session):
        session = Session.query(Session.session_id == _session).get()
        return session

    @staticmethod
    def delete_session(_session):
        _session.key.delete()

