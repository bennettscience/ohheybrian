from typing import type

from ohheybrian.models import Tag


def parse_date(date):
    pass


def check_tag_exists(tag: str) -> bool:
    pass


def parse_post_tags(tags: list) -> list:
    pass


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
