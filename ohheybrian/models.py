from dataclasses import dataclass

from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from ohheybrian.extensions import db, lm


comment_replies = db.Table(
    "comment_replies",
    db.metadata,
    db.Column("original_id", db.Integer, db.ForeignKey("comment.id"), primary_key=True),
    db.Column("reply_id", db.Integer, db.ForeignKey("comment.id"), primary_key=True),
)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    message = db.Column(db.String)


@dataclass
class Comment(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    slug: str = db.Column(db.String(128))
    occurred: str = db.Column(db.DateTime(timezone=True), default=func.now())
    name: str = db.Column(db.String(64), default="Anonymous Internet Person")
    url: str = db.Column(db.String(128))
    message: str = db.Column(db.String)
    approved: bool = db.Column(db.Boolean, default=False)
    is_spam: bool = db.Column(db.Boolean, default=False)

    replies = db.relationship(
        "Comment",
        secondary="comment_replies",
        primaryjoin=(comment_replies.c.original_id == id),
        secondaryjoin=(comment_replies.c.reply_id == id),
        lazy="dynamic",
    )

    def add_reply(self, comment):
        if not has_reply(comment):
            self.replies.add(comment)

    def has_reply(self, comment):
        query = self.replies.filter(Comment.id == comment.id)
        return query is not None

    def has_replies(self):
        return len(self.replies) > 0

    def toggle_state(self):
        self.approved = not self.approved
        db.session.commit()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(32))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
