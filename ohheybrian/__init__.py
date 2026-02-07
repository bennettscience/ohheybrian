import os
import shutil

import click
from flask import Flask, current_app, send_from_directory
from flask_cors import CORS
from ohheybrian.extensions import db, htmx, lm, migrate, partials
from ohheybrian.blueprints import (
    admin,
    auth,
    category,
    comment,
    home,
    microblog,
    post,
    search,
    tag,
)
from ohheybrian.functions.rss import FeedGenerator
from ohheybrian.functions.sync_client.sync import sync_posts, migrate_comments
from ohheybrian.models import Post


def create_app(config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config)

    db.init_app(app)
    htmx.init_app(app)
    lm.init_app(app)
    migrate.init_app(app, db)

    partials.register_extensions(app)

    app.register_blueprint(admin.bp, url_prefix="/admin")
    app.register_blueprint(auth.bp)
    app.register_blueprint(category.bp)
    app.register_blueprint(comment.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(post.bp, url_prefix="/blog")
    app.register_blueprint(search.bp)
    app.register_blueprint(tag.bp)

    @app.cli.command("sync")
    @click.argument('dir')
    def run(dir):
        sync_posts(dir)

    @app.cli.command("migrate_comments")
    def run():
        migrate_comments()

    @app.route("/feed")
    def rss_feed():

        return send_from_directory("static", "feed.atom.xml")

    return app
