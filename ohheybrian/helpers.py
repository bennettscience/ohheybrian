from ohheybrian.extensions import db
from ohheybrian.models import Tag


def parse_date(date):
    pass


def check_tag_exists(tag: str) -> int:
    query = Tag.query.filter(Tag.name == tag).first()
    if query:
        result = query
    else:
        result = Tag(name=tag)
        db.session.add(result)
        db.session.commit()

    return result.id


def parse_post_tags(tags: str) -> list:
    """
    Accept a list of string tags and return a list
    of Tag ids to use in the database.
    """
    tag_list = []

    for tag in tags.split(","):
        tag_list.append(check_tag_exists(tag))

    return tag_list


def create_new_tag(tag: str) -> type("Tag"):
    """
    Create a new tag for a submitted string if one does not exist.
    Return the new Tag object
    """
    pass


def create_new_category(category: str) -> object:
    """
    Create a new category if it does not exist.
    returns Category object
    """
    pass
