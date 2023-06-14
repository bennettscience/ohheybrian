from flask import abort, current_app, Blueprint, redirect, render_template
from htmx_flask import make_response, request


bp = Blueprint("academics", __name__, url_prefix='/academics')


@bp.get("/goals")
def get_goals():
	return render_template('academics/partials/goals.html')

