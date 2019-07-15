import datetime
import logging

from models.stories import Comment, Like

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(date):
    return (date - epoch).total_seconds() * 1000.0


def construct_response_message(**kwargs):
    return kwargs


def dict_formation(**kwargs):
    return kwargs


def parse_entity(entity):
    ent = dict_formation(
        id=entity.key.pairs()[0][1],
        name=entity.name.encode("utf-8"),
        mail=entity.mail.encode("utf-8"),
        password=entity.password.encode("utf-8"),
    )
    return ent


def parse_story(story):
    if story is not None:
        logging.info(story)
        logging.info(story.story.encode('utf-8'))
        _story = dict_formation(
            story_id=story.story_id.encode('utf-8'),
            name=story.name.encode('utf-8'),
            story=story.story.encode('utf-8'),
            like_count=story.like_count,
            time=unix_time_millis(story.created_on)
        )
        return _story
    return story


def parse_all_story(stories, user):
    data = []
    for story in stories:
        story_id = story.story_id.encode('utf-8')
        comments, next_cursor, more = Comment.get_all_comment(story_id)
        comment = dict_formation(
            comment=parse_all_comment(comments),
            next_cursor=next_cursor,
            more=more,
        )

        _story = parse_story(story)
        _story['comments'] = comment
        logging.info(user)
        like_key = Like.get_like(user.get('mail'), story_id)
        liked = True if like_key is not None else False
        _story['liked'] = liked
        data.append(_story)
    return data


def parse_session(_session):
    ses = dict_formation(
        session_id=_session.session_id.encode("utf-8"),
        name=_session.name.encode("utf-8"),
        mail=_session.mail.encode('utf-8')
    )
    return ses


def parse_comment(comment):
    _comment = dict_formation(
        comment_id=comment.comment_id.encode("utf-8"),
        story_id=comment.story_id.encode("utf-8"),
        name=comment.name.encode("utf-8"),
        mail=comment.mail.encode("utf-8"),
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


def entity_list(entities):
    _entity_list = []
    mail_list = []
    for entity in entities:
        _entity_list.append(parse_entity(entity))
        mail_list.append(entity.mail.encode("utf-8"))

    return _entity_list
