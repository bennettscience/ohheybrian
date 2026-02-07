# Generate an RSS XML file when a new post is published.
import os
import shutil

from datetime import datetime
from zoneinfo import ZoneInfo

from feedgenerator import Atom1Feed, get_tag_uri
from flask import current_app, url_for

from ohheybrian.extensions import db
from ohheybrian.models import Post

# Based on the FeedGenerator writer from the Pelican project
# https://github.com/getpelican/pelican/blob/main/pelican/writers.py
class FeedGenerator:
    def __init__(self, output_path, limit=None):
        self.output_path = output_path
        self.limit = limit

    def _create_new_feed(self):
        feed_class = Atom1Feed
        feed_title = "ohhey[blog]"

        return feed_class(
            title=feed_title,
            link="http://ohheybrian.com/blog",
            feed_url="https://ohheybrian.com/feed",
            description="",
            subtitle=None
        )

    def _add_item_to_feed(self, feed, item):
        title = item.title
        link = url_for('post.get_single_post', year=item.created_year, month=item.created_month, post_slug=item.slug)

        content = item.post_body

        categories = []
        if hasattr(item, "tags"):
            categories.extend([tag.name for tag in item.tags])

        feed.add_item(
            title=title,
            link=link,
            unique_id=get_tag_uri(link, item.created_on),
            content=content,
            description="",
            categories=categories or None,
            author_name="Brian",
            pubdate=item.created_on.replace(tzinfo=ZoneInfo("America/Indianapolis")),
        )

    def _get_feed_items(self):
        stmt = db.select(Post).where(Post.published).order_by(Post.created_on.desc()).limit(self.limit)
        posts = db.session.scalars(stmt).all()

        return posts

    def write_feed(
        self,
        url=None,
        override_output=False,
        feed_title=None
    ):
        """
            Generate a feed from a list of post objects. Save the file to a specific location to serve from the 'static' folder.
        """
        feed = self._create_new_feed()
        complete_path = os.path.join(self.output_path, "feed.atom.xml")
        elements = self._get_feed_items()

        for element in elements:
            self._add_item_to_feed(feed, element)

        with open(complete_path, "w", encoding="utf-8") as fp:
            feed.write(fp, "utf-8")

        return feed

