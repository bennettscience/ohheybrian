from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from htmx_flask import Htmx
import jinja_partials as partials

db = SQLAlchemy()
htmx = Htmx()
migrate = Migrate()