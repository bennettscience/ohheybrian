from ohheybrian.extensions import db


class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	last_name = db.Column(db.String(64))
	first_name = db.Column(db.String(64))
	email = db.Column(db.String(128))
	message = db.Column(db.String)
