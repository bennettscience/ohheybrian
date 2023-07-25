from flask import abort, current_app, Blueprint, redirect, render_template
from htmx_flask import make_response, request


bp = Blueprint("leadership", __name__, url_prefix="/leadership")


@bp.get("/")
def get_leadership():
    return render_template("leadership/index.html")


@bp.get("/assessment")
def get_assessment_training():
    return render_template("leadership/partials/assessment.html")


@bp.get("/grants")
def get_grants():
    return render_template("leadership/partials/grants.html")


@bp.get("/institutes")
def get_institutes():
    return render_template("leadership/partials/institutes.html")


@bp.get("/technology")
def get_tech_training():
    return render_template("leadership/partials/technology.html")
