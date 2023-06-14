from flask import abort, current_app, Blueprint, redirect, render_template
from htmx_flask import make_response, request


bp = Blueprint("comments", __name__)


@bp.get("/")
def index():
	pass

