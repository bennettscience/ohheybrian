from flask import abort, current_app, Blueprint, redirect, render_template
from htmx_flask import make_response, request
from ohheybrian.extensions import db
from ohheybrian.models import Contact
 
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
		resp = render_template("shared/layout-wrap.html", partial=template, data=resp_data)

	return resp

@bp.get("/about/contact")
def contact():
	template = "about/index.html"
	resp_data = {}

	if request.htmx:
		resp = render_template(template, **resp_data)
	else:
		resp = render_template("shared/layout-wrap.html", partial=template, data=resp_data)

	return resp

@bp.post("/about/contact")
def submit_contact():
	template = "about/contact-confirm.html"
	resp_data = {}
	
	args = parser.parse({
		"last_name": fields.Str(), 
		"first_name": fields.Str(),
		"email": fields.Str(),
		"message": fields.Str()
	}, location="form")

	db.session.add(Contact(**args))
	db.session.commit()

	if request.htmx:
		resp = render_template(template, **resp_data)
	else:
		resp = render_template("shared/layout-wrap.html", partial=template, data=resp_data)

	return resp

@bp.get("/leadership")
def leadership():
	template = "leadership/index.html"
	resp_data = {}
	
	if request.htmx:
		resp = render_template(template, **resp_data)
	else:
		resp = render_template("shared/layout-wrap.html", partial=template, data=resp_data)

	return resp


@bp.get("/academics")
def academics():
	template = "academics/index.html"
	resp_data = {}

	if request.htmx:
		resp = render_template(template, **resp_data)
	else:
		resp = render_template(
			"shared/layout-wrap.html",
			partial=template,
			data=resp_data
		)

	return resp