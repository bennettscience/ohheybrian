from dataclasses import dataclass

from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from ohheybrian.extensions import db, lm

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
	id:int = db.Column(db.Integer, primary_key=True)
	slug:str = db.Column(db.String(128))
	occurred:str = db.Column(db.DateTime(timezone=True), default=func.now())
	name:str = db.Column(db.String(64), default="Anonymous Internet Person")
	url:str = db.Column(db.String(128))
	message:str = db.Column(db.String)
	approved = db.Column(db.Boolean, default=False)

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