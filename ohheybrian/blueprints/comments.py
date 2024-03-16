from flask import Blueprint, jsonify, redirect, render_template
from htmx_flask import make_response, request

import nh3
from webargs import fields
from webargs.flaskparser import parser
from webargs.multidictproxy import MultiDictProxy

from ohheybrian.extensions import db
from ohheybrian.models import Comment

bp = Blueprint("comments", __name__)


# Load data for mixted locations
# https://webargs.readthedocs.io/en/latest/advanced.html
@parser.location_loader("form_and_query")
def load_data(request, schema):
    newdata = request.args.copy()
    newdata.update(request.form)
    return MultiDictProxy(newdata, schema)


# Get all comments, admin view only. Essentially just a dump of everything in the database.
@bp.get("/comments")
def get_comments():
    comments = Comment.query.filter(Comment.approved == True).all()
    return jsonify(comments)


# Get approved top-level comments for a single post.
# This is fetched on load. Replies can be fetched with a user interaction.
@bp.get("/comments/<string:slug>")
def get_post_comments(slug):
    args = parser.parse({"reply_id": fields.Int()}, request, location="query")
    if args.get("reply_id"):
        comments = (
            Comment.query.filter(Comment.id == args["reply_id"])
            .first()
            .replies.order_by(Comment.occurred)
            .all()
        )
    else:
        comments = (
            Comment.query.filter_by(slug=slug, approved=True, is_reply=False)
            .order_by(Comment.occurred)
            .all()
        )
    return render_template("comments/comments.html", comments=comments)


@bp.post("/comments/<string:slug>")
def post_comment(slug):
    args = parser.parse(
        {
            "name": fields.Str(),
            "slug": fields.Str(),
            "url": fields.Str(),
            "message": fields.Str(),
            "user_email": fields.Bool(),
        },
        location="form",
    )

    clean_text = nh3.clean(args["message"])

    comment = Comment(
        slug=args["slug"],
        name=args["name"],
        url=args["url"],
        message=args["message"],
    )

    if hasattr(args, "user_email"):
        comment.is_spam = True

    db.session.add(comment)

    # If the comment has a reply_to key, do that now
    if hasattr(request, "query_string"):
        comment.is_reply = True
        replied_to = Comment.query.filter(
            Comment.id == request.args.get("reply_to")
        ).first()
        replied_to.add_reply(comment)

    db.session.commit()

    return "Thanks! All comments are moderated, so yours will appear once approved."


@bp.put("/comments/<int:id>")
def moderate(id):
    comment = Comment.query.filter(Comment.id == id).first()
    comment.toggle_state()
    value = "Approved" if comment.approved else "Pending"
    return make_response(value, trigger={"showToast": "Comment status updated"})


@bp.delete("/comments/<int:id>")
def delete_comment(id):
    comment = Comment.query.filter(Comment.id == id).first()
    db.session.delete(comment)

    db.session.commit()
    return make_response(trigger={"showToast": "Comment deleted"})


# Get a form to reply to a comment
@bp.get("/comments/<string:slug>/reply/<int:id>")
def get_comment_form(slug, id):
    return render_template("shared/forms/comment-reply.html", slug=slug, comment_id=id)
