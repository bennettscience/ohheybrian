from flask import Flask
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


def create_app(config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config)

    cors = CORS(
        app, resources={r"/comments\/\S*": {"origins": app.config["CORS_ENDPOINT"]}}
    )

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

    return app
