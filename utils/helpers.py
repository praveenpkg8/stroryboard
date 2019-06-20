import datetime

from models.stories import Comment

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
        story_id=story.story_id.encode('utf-8'),
        name=story.name.encode('utf-8'),
        story=story.story.encode('utf-8'),
        time=story.created_on.isoformat()
    )
    return _story


def parse_all_story(stories):
    data = []
    for story in stories:
        story_id = str(story.story_id.encode('utf-8'))
        comments, next_cursor, more = Comment.get_all_comment(story_id)
        comment = dict_formation(
            comment=parse_all_comment(comments),
            next_cursor=next_cursor,
            more=more,
        )

        _story = parse_story(story)
        _story['comments'] = comment
        data.append(_story)
    return data


def parse_session(_session):
    ses = dict_formation(
        session_id=_session.session_id.encode("utf-8"),
        name=_session.name.encode("utf-8"),
        user_name=_session.user_name.encode('utf-8')
    )
    return ses


def parse_comment(comment):
    _comment = dict_formation(
        comment_id=comment.comment_id.encode("utf-8"),
        story_id=comment.story_id.encode("utf-8"),
        name=comment.name.encode("utf-8"),
        user_name=comment.user_name.encode("utf-8"),
        comment=comment.comment.encode("utf-8")
    )
    return _comment


def parse_all_comment(comments):
    data = []
    for comment in comments:
        data.append(parse_comment(comment))
    return data


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
