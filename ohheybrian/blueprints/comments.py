from flask import Blueprint, jsonify, redirect, render_template
from htmx_flask import make_response, request

import nh3
from webargs import fields
from webargs.flaskparser import parser

from ohheybrian.extensions import db
from ohheybrian.models import Comment

bp = Blueprint("comments", __name__)


@bp.get("/comments")
def get_comments():
	comments = Comment.query.filter(Comment.approved == True).all()
	
	return jsonify(comments)

@bp.post("/comments/<string:slug>")
def post_comment(slug):
	args = parser.parse(
		{
			"name": fields.Str(),
			"slug": fields.Str(),
            "url": fields.Str(),
            "message": fields.Str(),
			"user_email": fields.Bool()
        },
        location="form"
    )

	clean_text = nh3.clean(args["message"])

	if not hasattr(args, "user_email"):
		db.session.add(
			Comment(
				slug=args["slug"],
				name=args["name"],
				url=args["url"],
				message=args["message"],
				is_spam=args["user_email"]
			)
	    )
		db.session.commit()

	return "Thanks! All comments are moderated, so yours will appear soon."

@bp.get("/comments/<string:slug>")
def get_post_comments(slug):
	comments = Comment.query.filter_by(slug=slug, approved=True).order_by(Comment.occurred).all()
	return jsonify(comments)


@bp.put("/comments/<int:id>")
def moderate(id):
	comment = Comment.query.filter(Comment.id == id).first()
	comment.toggle_state()
	value = "Approved" if comment.approved else "Pending"
	return make_response(
		value,
		trigger={"showToast": "Comment status updated"}
	)

@bp.delete("/comments/<int:id>")
def delete_comment(id):
	comment = Comment.query.filter(Comment.id == id).first()
	db.session.delete(comment)

	db.session.commit()
	return make_response(
		trigger={"showToast": "Comment deleted"}
	)