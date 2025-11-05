from flask import Blueprint, redirect, render_template
from flask_login import current_user
from htmx_flask import make_response

from ohheybrian.extensions import db
from ohheybrian.models import Comment

bp = Blueprint("categories", __name__)


# Get all cats
@bp.get("/categories")
def categories():
    pass


# Start a new cat
@bp.get("/categories/new")
def create_category():
    pass


# Create the new cat
@bp.post("/categories/new")
def save_new_category():
    pass


# Edit a cat
@bp.get("/categories/<int:cat_id>")
def edit_category(cat_id: int):
    pass
