from flask import Flask 
from flask_cors import CORS
from ohheybrian.extensions import db, htmx, lm, migrate, partials
from ohheybrian.blueprints import admin, auth, comments, home

def create_app(config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config)

    cors = CORS(app, resources={r"/comments/*": {"origins": "https://blog.ohheybrian.com"}})

    db.init_app(app)
    htmx.init_app(app)
    lm.init_app(app)
    migrate.init_app(app, db)

    partials.register_extensions(app)

    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(comments.bp)
    app.register_blueprint(home.bp)

    return app

