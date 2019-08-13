from google.appengine.ext import ndb


class Contact(ndb.Model):
    contact_id = ndb.StringProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    reference = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now=True)
    updated_on = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create_contact(contact):
        contact_key = contact.put()
        return contact_key.get()

    @staticmethod
    def get_contact_by_mail(email):
        contact = Contact.query(Contact.email == email).get()
        return contact

    @staticmethod
    def get_all_contact():
        contact_list = Contact.query().fetch()
        return contact_list

    @staticmethod
    def remove_contact(contact):
        contact.key.delete()


