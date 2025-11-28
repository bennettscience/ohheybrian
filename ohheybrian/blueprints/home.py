from flask import Blueprint, request, render_template

bp = Blueprint("home", __name__)


@bp.get("/")
def index():
    template = "home/index.html"
    resp_data = {}

    if request.htmx:
        resp = render_template(template, **resp_data)
    else:
        resp = render_template(
            "shared/layout-wrap.html", partial=template, data=resp_data
        )

    return resp


@bp.get("/about/contact")
def contact():
    template = "about/index.html"
    resp_data = {}

    if request.htmx:
        resp = render_template(template, **resp_data)
    else:
        resp = render_template(
            "shared/layout-wrap.html", partial=template, data=resp_data
        )

    return resp


@bp.get("/privacy/endnote.html")
def endnote_privacy():
    return render_template("privacy/index.html")
