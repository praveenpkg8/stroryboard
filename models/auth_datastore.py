from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    mail = ndb.StringProperty()
    password = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now=True)
    updated_on = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create_user(user):
        user_key = user.put()
        return user_key

    @staticmethod
    def get_all_user():
        users = User.query()
        return users.fetch()


    @staticmethod
    def user_by_mail(mail):
        user = User.query(User.mail == mail).get()
        return user


class Session(ndb.Model):
    session_id = ndb.StringProperty()
    mail = ndb.StringProperty()
    name = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now=True)
    updated_on = ndb.DateTimeProperty(auto_now_add=True)

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

