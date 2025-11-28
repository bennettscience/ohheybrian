import imghdr
from slugify import slugify

from ohheybrian.extensions import db
from ohheybrian.models import Category, Post, Tag


def check_tag_or_category_exists(table: str, name: str) -> bool:
    stmt = db.select(table).where(getattr(table, "name") == name)
    return db.session.scalar(stmt)


def check_post_slug(slug: str):
    post_slug = slugify(slug)

    # Check the database for an existing slug of that name
    check_stmt = db.select(Post).where(Post.slug == post_slug)
    slug_exists = db.session.scalars(check_stmt).all()

    if not slug_exists:
        return post_slug
    else:
        # check the length of the returned array
        # and append +1 to the end to create a unique
        # value for the post
        length = len(slug_exists) + 1
        post_slug = "{}-{}".format(post_slug, length)

    return post_slug


def parse_post_tags(tags: list) -> list:
    result = []
    for tag in tags:
        # TODO: wrap this in the db client
        tag_exists = check_tag_or_category_exists(Tag, tag)
        if tag_exists:
            result.append(tag_exists)
        else:
            new_tag = create_new_tag(tag)
            result.append(new_tag)

    return result


def check_category(category: str) -> type(Category):
    stmt = db.select(Category).where(Category.name == category)
    result = db.session.scalar(stmt)

    if not result:
        result = create_new_category(category)

    return result


def create_new_tag(tag: str) -> type("Tag"):
    """
    Create a new tag for a submitted string if one does not exist.
    Return the new Tag object
    """
    new_tag = Tag(name=tag)
    db.session.add(new_tag)
    db.session.commit()

    return new_tag


def create_new_category(category: str) -> type(Category):
    """
    Create a new category if it does not exist.
    returns Category object
    """
    category = Category(name=category)
    db.session.add(category)
    db.session.commit()

    return category


def validate_image(stream):
    """
    Ensure an upload is actually an image.
    Modified from a post by Miguel Grinberg detailing how to handle file uploads with Flask for dummies like myself.
    https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
    """
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")
