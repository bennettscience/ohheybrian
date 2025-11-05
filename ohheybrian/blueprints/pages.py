from flask import Blueprint, redirect, render_template
from flask_login import current_user
from htmx_flask import make_response

from ohheybrian.extensions import db
from ohheybrian.models import Comment

bp = Blueprint("pages", __name__)


# Get all pages
@bp.get("/pages")
def pages():
    pass


# Start a new page
@bp.get("/pages/new")
def create_page():
    pass


# Create the new page
@bp.post("/pages/new")
def save_new_page():
    pass


# Edit a page
@bp.get("/pages/<int:page_id>")
def edit_page(page_id: int):
    pass
