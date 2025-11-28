# Generate an RSS XML file when a new post is published.
from datetime import datetime
from zoneinfo import ZoneInfo
from feedgen.feed import FeedGenerator


def create_feed(items):
    fg = FeedGenerator()

    fg.title("the otherblog")
    fg.id("https://ohheybrian.com/otherblog")
    fg.link(href="http://ohheybrian.com/otherblog", rel="alternate")
    fg.link(href="http://ohheybrian.com/otherblog/feed", rel="self")
    fg.contributor(name="Brian", email="brian@ohheybrian.com")
    fg.description("A place for other thoughts")
    fg.updated(datetime.now(ZoneInfo("America/Indianapolis")))

    for item in items:
        entry = fg.add_entry()

        # replace the decimal with an underscore
        entry.id(f"https://ohheybrian.com/otherblog/{item.slug}")
        entry.link(href=f"https://ohheybrian.com/otherblog/{item.slug}")
        entry.title(item.title)
        entry.author({"name": "Brian", "email": "brian@ohheybrian.com"})

        # SQLite and SQLAlchemy don't play well with timezones. All of my
        # posts are written in EST, so do that here manually for now.

        entry.published(
            item.created_on.replace(tzinfo=ZoneInfo("America/Indianapolis"))
        )
        entry.content(type="html", content=item.post_body)

        for tag in item.tags:
            entry.category(term=tag.name)

    return fg.atom_str(pretty=True)
