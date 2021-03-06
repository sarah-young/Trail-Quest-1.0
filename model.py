
from flask_sqlalchemy import SQLAlchemy
from requests import sessions
from flask import Flask
import json
import secrets


db = SQLAlchemy()

#####################################################################

# Trail Quest Database

class Trail(db.Model):
	"""Trails that are generated from user requests."""

	__tablename__ = "trails"

	trail_id = db.Column(db.Integer, primary_key=True)
	trail_name = db.Column(db.String(200), nullable=False, unique=False)
	trailhead_latitude = db.Column(db.Float, nullable=False)
	trailhead_longitude = db.Column(db.Float, nullable=False)
	trail_length = db.Column(db.Float, nullable=False)
	trail_difficulty = db.Column(db.String(30), nullable=False)
	trail_description = db.Column(db.UnicodeText, nullable=True)
	trail_high_alt = db.Column(db.Float, nullable=True)
	trail_low_alt = db.Column(db.Float, nullable=True)
	trail_location = db.Column(db.String(100))
	trail_picture = db.Column(db.String(300))
	# Will calculate ascent & descent with trail_high_alt & trail_low_alt

	reviews = db.relationship('Review')
	treks = db.relationship('Trek')
	trail_badges = db.relationship('TrailBadge')

	def __repr__(self):
		return "<Trail name: %s Trail_length: %s >" % (self.trail_name, self.trail_length)


class User(db.Model):
	"""Trail Quest user database
	Phase 2
	"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_name = db.Column(db.String(50), nullable=False)
	user_password = db.Column(db.String(500), nullable=False)

	reviews = db.relationship('Review')
	trek = db.relationship('Trek')
	merit = db.relationship('Merit')

	def __repr__(self):
		return "<User id: %s User name: %s >" % (self.user_id, self.user_name)

class Review(db.Model):
	"""Reviews made by users"""

	__tablename__ = "reviews"
 	# If lagging, look @ indexing trail_id and/or user_id

	review_id = db.Column(db.Integer, primary_key=True)
	trail_id = db.Column(db.Integer, db.ForeignKey('trails.trail_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	review_text = db.Column(db.UnicodeText)

	trails = db.relationship('Trail')
	users = db.relationship('User')

	def __repr__(self):
		return "<Review id: %s Review: %s >" % (self.review_id, self.review)


class Trek(db.Model):
	"""All trails the user has been on

	Alternate name: UsersTrails
	"""

	__tablename__ = "user_trails"

	trek_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	trail_id = db.Column(db.Integer, db.ForeignKey('trails.trail_id'))
	trek_date = db.Column(db.DateTime)
	trail = db.relationship('Trail')
	user = db.relationship('User')

	def __repr__(self):
		return "<Trek id: %s, Trek date: %s >" % (self.trek_id, self.trek_date)


class Badge(db.Model):
	"""Badges that the user can be assigned for completing trails"""

	__tablename__ = "badges"

	badge_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	badge_name = db.Column(db.String(50))
	badge_description = db.Column(db.UnicodeText)

	merits = db.relation('Merit')

	def __repr__(self):
		return "< Badge id: %s Badge name: %s >" % (self.badge_id, self.badge_name)

class Merit(db.Model):
	"""All the types of badges that have been assigned and which user they have been assigned to"""

	__tablename__ = "merit_badges"

	merit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	badge_id = db.Column(db.Integer, db.ForeignKey('badges.badge_id'))
	merit_date = db.Column(db.DateTime)

	badges = db.relationship('Badge')
	users = db.relationship('User')

	def __repr__(self):
		return "< Merit id: %s Badge: %s User %s >" % (self.merit_id, self.badge_id, self.user_id)


class TrailBadge(db.Model):
	"""Table of which trails have which badges associated with them"""

	__tablename__ = "trail_badges"

	tb_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	trail_id = db.Column(db.Integer, db.ForeignKey('trails.trail_id'))
	badge_id = db.Column(db.Integer, db.ForeignKey('badges.badge_id'))

	trails = db.relationship('Trail')
	badges = db.relationship('Badge')

	def __repr__(self):
		return "< Trail/Badge object id: %s >" % (self.tb_id)


def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///trailquest'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    db.create_all()
