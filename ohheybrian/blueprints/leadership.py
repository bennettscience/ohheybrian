from flask import abort, current_app, Blueprint, redirect, render_template
from htmx_flask import make_response, request


bp = Blueprint("leadership", __name__, url_prefix='/leadership')


@bp.get("/institutes")
def get_institutes():
	return render_template('leadership/partials/institutes.html')

@bp.get("/grants")
def get_grants():
	return render_template('leadership/partials/grants.html')