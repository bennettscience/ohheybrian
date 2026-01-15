from pathlib import Path
import sys

import markdown
import docutils.nodes
from docutils.core import publish_doctree

from ohheybrian.extensions import db
from ohheybrian.models import Category, Post, Tag

def save_post(data):
    if isinstance(data, dict):
        print(data)
        return True
    else:
        return False

def get_rst_meta(document):
    pass

def get_rst_post_body(document):
    pass

def parse_rst(file):
    print(f"Received {file.name}")

def parse_markdown(file_path):
    # Load the meta extension to extract frontmatter from any *.md post.
    # https://python-markdown.github.io/extensions/meta_data/
    md = markdown.Markdown(extensions=["meta"])
    file = file_path.open('r')
    post_data = {
        "post_body": md.convert(file.read()),
        "post_meta": md.Meta
    }

    return save_post(post_data)

def process_files(dir):
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

    process_files(path_str)

