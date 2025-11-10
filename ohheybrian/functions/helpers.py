from ohheybrian.extensions import db
from ohheybrian.models import Tag


def parse_date(date):
    pass


def check_tag_or_category_exists(table: str, name: str) -> bool:
    stmt = db.select(table).where(getattr(table, "name") == name)
    return db.session.scalar(stmt)


def parse_post_tags(tags: list) -> list:
    result = []
    for tag in tags:
        # TODO: wrap this in the db client
        tag = check_tag_or_category_exists("Tag", tag)
        if tag:
            result.append(tag)
        else:
            new_tag = create_new_tag(tag)
            result.append(new_tag)

    return result


def create_new_tag(tag: str) -> type("Tag"):
    """
    Create a new tag for a submitted string if one does not exist.
    Return the new Tag object
    """
    new_tag = db.session.add(Tag(name=tag))
    db.session.commit()

    return new_tag


def create_new_category(category: str) -> object:
    """
    Create a new category if it does not exist.
    returns Category object
    """
    pass
