from flask import Blueprint, render_template

from ohheybrian.extensions import db
from ohheybrian.models import Tag


bp = Blueprint("tag", __name__)


@bp.route("/tag")
def tag_index():
    stmt = db.select(Tag)
    tags = db.session.scalars(stmt).all()

    return render_template("tag/index.html", tags=tags)


@bp.route("/tag/<int:tag_id>")
def single_tag(tag_id):
    stmt = db.select(Tag).where(Tag.id == tag_id)
    tag = db.session.scalars(stmt).one()

    return render_template("tag/single.html", tag=tag)
