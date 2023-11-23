from flask import Blueprint, jsonify, redirect, render_template
from htmx_flask import make_response, request

from ohheybrian.extensions import db
from ohheybrian.models import Comment

bp = Blueprint("comments", __name__)


@bp.get("/comments")
def get_comments():
	comments = Comment.query.filter(Comment.approved == True).all()
	
	return jsonify(comments)
	
@bp.get("/comments/<string:slug>")
def get_post_comments(slug):
	comments = Comment.query.filter(Comment.slug == slug and Comment.approved == True).order_by(Comment.occurred).all()
	return jsonify(comments)


@bp.put("/comments/<int:id>")
def moderate(id):
	comment = Comment.query.filter(Comment.id == id).first()
	comment.toggle_state()
	return make_response(
		trigger={"showToast": "Comment status updated"}
	)