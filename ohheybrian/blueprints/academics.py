from flask import abort, current_app, Blueprint, redirect, render_template
from htmx_flask import make_response, request


bp = Blueprint("academics", __name__, url_prefix="/academics")


@bp.get("/goals")
def get_goals():
    return render_template("academics/partials/goals.html")


@bp.get("/academics/showcase/learning-in-out")
def learning_in_out():
    template = "academics/learning-in-out.html"
    resp_data = {}

    if request.htmx:
        resp = render_template(template, **resp_data)
    else:
        resp = render_template(
            "shared/layout-wrap.html", partial=template, data=resp_data
        )

    return resp
