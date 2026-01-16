from datetime import datetime
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

import click
from flask.cli import with_appcontext
import docutils.nodes
from docutils.core import publish_doctree, publish_parts
import markdown

from ohheybrian.extensions import db
from ohheybrian.functions.helpers import (
    parse_post_tags,
    check_post_slug,
)
from ohheybrian.models import Category, Post, Tag

def save_post(data):
    if isinstance(data, dict):
        date_format = "%Y-%m-%d %I:%M"
        date = datetime.strptime(data.get("meta", {}).get("date"), date_format)

        args = {}

        args["title"] = data.get("meta", {}).get("title")

        # Check that the slug is unique and create
        # a new one if needed
        args["slug"] = check_post_slug(data.get("meta", {}).get("slug"))

        # set the post publish date. include the timezone for RSS creation
        args["created_on"] = datetime.strptime(data.get("meta", {}).get("date"), date_format).replace(tzinfo=ZoneInfo('America/Indianapolis'))

        args["author"] = "Brian"

        args["post_body"] = data.get("body")

        args["published"] = True

        # At this point, the post is complete and can be added to the database.
        post = Post(
            title=args["title"],
            slug=args["slug"],
            created_on=args["created_on"],
            author=1,
            post_body=args["post_body"],
            published=args["published"],
        )

        db.session.add(post)

        # Add the tags to the new post object
        # check the tags and create new ones if necessary
        # Turn the tags field into a list
        args["tags"] = parse_post_tags(data.get("meta", {}).get("tags").split(", "))
        post.tags.extend(args["tags"])

        # check the post category
        # Can only be single, so checking here isn't awful
        # This is redundant - assign directly if it works?
        # DISABLED FOR NOW
        # args["category"] = check_category(form.get("category"))
        # post.category = args["category"]

        # If the tags or category fail, flip the post to "draft" and flash and error?
        db.session.commit()
    else:
        return False

def get_rst_metadata(document):
    # The title is not part of the metadata block, so it has to be extracted separately.
    metadata = {}
    
    metadata['title'] = document.next_node(docutils.nodes.title).astext()

    # Collect all of the header nodes into a list that can be iterated
    headers_nodes = list(document.findall(docutils.nodes.docinfo))

    if headers_nodes:
        docinfo = headers_nodes[0]
        for node in docinfo:
            if isinstance(node, docutils.nodes.TextElement):
                key = node.__class__.__name__
                value = node.astext()
            elif isinstance(node, docutils.nodes.field):
                key = node.children[0].astext()
                value = node.children[1].astext()

            metadata[key] = value

    return metadata
        

def parse_rst(file):
    # open up the file and create the document object
    post_data = {}
    with open(file, "r") as f:
        file_string = f.read()
        body = publish_parts(file_string, writer_name="html")["body"]
        document = publish_doctree(file_string)

    # extract the metadata
    post_data['meta'] = get_rst_metadata(document)
    post_data['body'] = body

    return save_post(post_data)

def parse_markdown(file_path):
    # Load the meta extension to extract frontmatter from any *.md post.
    # https://python-markdown.github.io/extensions/meta_data/
    md = markdown.Markdown(extensions=["meta"])
    meta = {}
    file = file_path.open('r')

    body = md.convert(file.read())

    # The markdown meta extension has values for each key in a list, so they need to be extractd.
    for key, val in md.Meta.items():
        meta[key] = val[0]
    
    post_data = {
        "body": body,
        "meta": meta
    }

    return save_post(post_data)


def sync_posts(dir):
    """
        Read files from a directory and handle importng content
    """
    directory = Path(dir)
    for item in directory.iterdir():
        if item.is_file:
            if item.suffix == ".rst":
                parse_rst(item)
            elif item.suffix == ".md":
                parse_markdown(item)
            else:
                continue


if __name__ == "__main__":    
    if len(sys.argv) < 1:
        print("Pass a directory to scan")
        sys.exit(1)

    path_str = sys.argv[1]

    sync_posts(path_str)

