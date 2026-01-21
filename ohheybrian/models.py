from dataclasses import dataclass

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped
from sqlalchemy import func, select, union_all
from werkzeug.security import generate_password_hash, check_password_hash

from ohheybrian.extensions import db, lm


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


comment_replies = db.Table(
    "comment_replies",
    db.metadata,
    db.Column("original_id", db.Integer, db.ForeignKey("comment.id"), primary_key=True),
    db.Column("reply_id", db.Integer, db.ForeignKey("comment.id"), primary_key=True),
)


class Base:

    def toggle_state(self, prop):
        if hasattr(self, prop):
            self.prop = not self.prop
            db.session.commit()
        else:
            return False
        return True


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    message = db.Column(db.String)


@dataclass
class Comment(db.Model, Base):
    id: int = db.Column(db.Integer, primary_key=True)
    slug: str = db.Column(db.String(128))
    occurred: str = db.Column(db.DateTime(timezone=True), default=func.now())
    name: str = db.Column(db.String(64), default="Anonymous Internet Person")
    url: str = db.Column(db.String(128))
    message: str = db.Column(db.String)
    approved: bool = db.Column(db.Boolean, default=False)
    is_spam: bool = db.Column(db.Boolean, default=False)
    is_reply = db.Column(db.Boolean, default=False)
    has_replies: bool
    num_replies: int

    replies = db.relationship(
        "Comment",
        secondary="comment_replies",
        primaryjoin=(comment_replies.c.original_id == id),
        secondaryjoin=(comment_replies.c.reply_id == id),
        lazy="dynamic",
    )

    def add_reply(self, comment):
        if not self.has_reply(comment):
            self.replies.append(comment)

    def has_reply(self, comment):
        query = self.replies.filter(Comment.id == comment.id).first()
        return query is not None

    @property
    def num_replies(self):
        return len(self.replies.all())

    @property
    def has_replies(self) -> bool:
        return len(self.replies.all()) > 0


class Page(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    page_body = db.Column(db.String)
    published = db.Column(db.Boolean, default=False)
    show_in_nav = db.Column(db.Boolean, default=True)


class Post(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    category = db.relationship(
        "Category",
        secondary="postcategory_association",
        uselist=False,
        lazy="subquery",
        backref=db.backref("posts", lazy="subquery"),
    )
    tags = db.relationship(
        "Tag",
        secondary="posttag_association",
        uselist=True,
        lazy="subquery",
        backref=db.backref("posts", lazy="subquery"),
    )
    post_body = db.Column(db.String)
    published = db.Column(db.Boolean, default=False)
    slug = db.Column(db.String)

    comments = db.relationship(
        "Comment",
        secondary="post_comment",
        uselist=True,
        lazy="subquery",
        backref=db.backref("post", lazy="subquery")
    )

    # Load neighbor posts for individual posts
    def load_neighbors(self):
        prev_q = db.select(Post).where(Post.created_on < self.created_on).order_by(Post.created_on.desc())

        next_q = db.select(Post).where(Post.created_on > self.created_on).order_by(Post.created_on.asc())

        # It is not possible to do this against an SQLite database
        # https://github.com/sqlalchemy/sqlalchemy/issues/8094:w
        # neighbors = db.session.scalars(prev_q.union_all(next_q))

        self.prev = db.session.scalar(prev_q.limit(1))
        self.next = db.session.scalar(next_q.limit(1))

        return self

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()
        return self


class Category(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)

    @classmethod
    def category_names(cls):
        return Category.query.filter()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)

    @classmethod
    def tag_names(cls):
        return Tag.query.filter()


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


# Associations

posttag_association = db.Table(
    "posttag_association",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
)

postcategory_association = db.Table(
    "postcategory_association",
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
)

post_comment = db.Table(
    "post_comment",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
    db.Column("comment_id", db.Integer, db.ForeignKey("comment.id"))
)
