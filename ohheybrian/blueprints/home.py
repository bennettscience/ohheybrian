from flask import abort, current_app, Blueprint, redirect, render_template
from htmx_flask import make_response, request
from ohheybrian.extensions import db
from ohheybrian.models import Contact
from ohheybrian.templates.icons import icons

import nh3

from webargs import fields
from webargs.flaskparser import parser

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
