import datetime
def construct_response_message(**kwargs):
    return kwargs


def dict_formation(**kwargs):
    return kwargs


def parse_entity(entity):
    ent = dict_formation(
        id=entity.key.pairs()[0][1],
        name=entity.name.encode("utf-8"),
        user_name=entity.user_name.encode("utf-8"),
        mail=entity.mail.encode("utf-8"),
        password=entity.password.encode("utf-8"),
        mobile_number=entity.mobile_number.encode("utf-8")
    )
    return ent


def parse_story(story):
    _story = dict_formation(
        name=story.name.encode('utf-8'),
        story=story.story.encode('utf-8'),
        time=story.created_on.isoformat()
    )
    return _story


def parse_all_stories(stories):
    data = []
    for story in stories:
        data.append(parse_story(story))
    return data


def parse_session(_session):
    ses = dict_formation(
        session_id=_session.session_id.encode("utf-8"),
        name=_session.name.encode("utf-8"),
        user_name=_session.user_name.encode('utf-8')
    )
    return ses


builtin_list = list


def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    return entity


def entity_list(entities, check=False):
    _entity_list = []
    user_name_list = []
    mail_list = []
    for entity in entities:
        _entity_list.append(parse_entity(entity))
        mail_list.append(entity.mail.encode("utf-8"))
        user_name_list.append(entity.user_name.encode("utf-8"))

    if check:
        return user_name_list, mail_list

    return _entity_list
