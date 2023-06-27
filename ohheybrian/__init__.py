from flask import Flask 
from ohheybrian.extensions import db, htmx, migrate, partials
from ohheybrian.blueprints import academics, home, leadership

def create_app(config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config)

    db.init_app(app)
    htmx.init_app(app)
    migrate.init_app(app, db)

    partials.register_extensions(app)

    app.register_blueprint(academics.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(leadership.bp)

    return app

