from flask import Flask, render_template, request, session, jsonify
import secrets
import functions
from flask import Flask, redirect, request, render_template, session, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import send_sms
import twilio

from model import connect_to_db
import model

app = Flask(__name__)

app.secret_key = "SECRETSECRETSECRET"

########### USER LOGIN & REGISTER LOGIC #######################

@app.route('/remove_trail', methods =['POST'])
def trail_removal_route():
	"""
	SQLAlchemy query allowing user to remove trail from their trail list.
	"""
	t_id = request.form.get('trail_id')
	trail_to_remove = model.Trek.query.filter_by(user_id=session['user_id'], trail_id=t_id).delete()
	model.db.session.commit()
	# Trek is the table holding user trails.
	# Finding correct trek object via user_id in session & trail_id passed from the front end.
	# TODO: Add button to front end to remove trails.
	# TODO: Add similar route for removing reviews?

	return "Success"


@app.route('/welcome')
def show_registration_page():
	"""Show user registration form
	TODO:
	First test: (define *who* & *action*)
	> user enters /welcome url on browser
	> text appears in user's browser (*expected result*)
	>> look for trailquest, login, other expected words
	> so that the user can login to application
	"""
	return render_template('/welcome.html')


@app.route('/register', methods=['POST'])
def register_user():
	"""Take entries from registration form, check to see if user is in database.

	If user is not in database, add to database and redirect to login page w/
	appropriate flash message.
	If user is in database, redirect to login page w/ appropriate flash message"""

	username = request.form.get("username")
	password = request.form.get("password")

	a_new_user = functions.add_user_to_database(username, password)

	if a_new_user:

		flash("Thanks for registering for Trail Quest! Please login.")
		return render_template('/login.html')
	else:
		flash("User already in database. Please login with credentials.")
		return redirect('/login')


@app.route('/login', methods=['POST'])
def user_login():
	"""Take user login information, check database, return:
		> Homepage if user login information is correct w/ appropriate flash
		message
		> Welcome page if user login information is incorrect w/ appropriate
		flash message.
	"""
	username = request.form.get("loginemail")
	# print username
	password = request.form.get("loginpassword")
	# print password
	user = functions.check_user_credentials(username, password)

	if user:
		flash('Logged in successfully.')
		session['user_id'] = user.user_id

		return redirect('/homepage')


	else:
		flash('Please try your login again.')
		return redirect('/welcome')


@app.route('/logout')#, methods=['POST']
def user_logout():
	"""Log users out of trail quest"""

	del session['user_id']
	flash("Logged Out.")
	return redirect("/welcome")


########### INNER APP FUNCTIONALITY #######################


@app.route('/')
def display_trail_form():
	"""Displays form that takes in user input"""

	if session.get('user_id'):
	# check to see if username is in the session --if not, login page!
		return render_template('/homepage.html')
	else:
		flash("Please login to begin your adventure.")
		return render_template('/welcome.html')

@app.route('/homepage')
def render_homepage():

	if session.get('user_id'):
	# check to see if username is in the session --if not, login page!
		return render_template('/homepage.html')
	else:
		flash("Please login to begin your adventure.")
		return render_template('/welcome.html')


@app.route('/trails_asychronous', methods=['POST'])
def asynchronous_info_load():

	city = request.form.get("city")
	print "CITY: ", city
	state = request.form.get("state")
	print "STATE: ", state
	radius = request.form.get("radius")
	print "RADIUS: ", radius
	trek_length = request.form.get("trek_length")
	print "TREK LENGTH: ", trek_length
	trail_difficulty = request.form.get("trail_difficulty")
	print "DIFFICULTY SELECTED: ", trail_difficulty

	coordinates = functions.find_lat_lng(city,state)
	# ***Google Map API gets called here!***
	print "COORDINATES: ", coordinates

	if coordinates == None:
		print "!!!LOCATION OR RANGE ERROR!!!"
		return "FOO"

	trek_length = int(trek_length)

	radius_to_meters = int(radius) * 1609.34


	trails = functions.find_trails(coordinates, radius)
	# ***Hiking API gets called here!***

	if len(trails) == 0:

		print "!!!LOCATION OR RANGE ERROR!!! NO TRAILS"
		return "BAR"

	trails_to_db = functions.add_trails_to_db(trails)
	# Adds all trails from hiking project API to database
	trails_l = functions.filter_trek_length(trails, trek_length)
	# filters trail returned by API by user trail length preference
	# print "TRAILS AFTER LENGTH FILTER: ", trails

	trails_d = functions.filter_trek_difficulty(trails_l, trail_difficulty)
	# filters trails returned by API for user trail difficulty preference

	# print "TRAILS AFTER DIFFICULTY FILTER: ", trails

 	selected_trails = functions.select_trails(trails_d)
		# If selected trails == none, send back STRING which triggers different
		# in JavaScript

	# check each trail in selected trail starting at [-1]
	# if trail.trail_id == trek.trail_id
	# append to treks list, remove from trail selected_trails
	# check each trek in trek list starting @ [-1]
	# if trek.trail_id == review.trail_id
	# append to completed_trails_list, remove from trek list

	user_trails = model.db.session.query(model.Trek).filter(model.Trek.user_id==session['user_id']).all()
	user_reviews = model.db.session.query(model.Review).filter(model.Review.user_id==session['user_id']).all()
	# TODO: Looks for completed trails and trails in user's database...
	# TODO: See if you can make this information display on front end...


	# ids_from_reviews = set()
	# for review in user_reviews:
	# 	ids_from_reviews.add(review.trail_id)
	#
	# ids_from_user_trails = set()
	# for trek in user_trails:
	# 	ids_from_user_trails.add(trek.trail_id)


	lat, lng = coordinates
	lat = float(lat)
	lng = float(lng)

	selected_trails[0]["city_lat"] = float(lat)
	selected_trails[0]["city_long"] = float(lng)
	selected_trails[0]["radius_in_meters"] = radius_to_meters
	# print "SELECTED TRAILS: ", selected_trails

	if selected_trails > 1:
		return jsonify(selected_trails)
	# Keeping for now to see if this works with other routes... Not sure if this is needed.

	else:
		print "***LOCATION OR RANGE ERROR***"
		return "STRING"


@app.route('/trek', methods=['POST'])
def get_trail_id():
	"""Bring trail id of chosen trail to the back end for processing.
	Return trail deets from trail object.
	"""
	trail_id = request.form.get('chosentrail')
	trek_add = functions.add_trek_to_users_trails(trail_id)
	print "TREK ADD RESULT: ",trek_add
	# trail_conditions = functions.get_trail_conditions(trail_id)
	# print trail_conditions
	trail_object = functions.get_trail_object_by_id(trail_id)
	trail_details = functions.extract_relevant_trail_info(trail_object)

	trail_deets = [trail_details]
	print "TRAIL DEETS: ", trail_deets

	return jsonify(trail_deets)


@app.route('/mytrails', methods=['GET'])
def show_user_trails():
	"""Show user trails on mytrails.html page.

	Trails will show up as points on a map.

	Stars will show up when user has marked trails as completed.
	"""
	if session.get('user_id'):
		remaining_trails, completed_trails = functions.find_uncompleted_trails()
		if len(remaining_trails) == 0:
			remaining_trails = 0

		merit_list = model.db.session.query(model.Merit).filter(model.Merit.user_id==session['user_id']).all()

		merit_set = set()
		for merit in merit_list:
			thing = merit.badges.badge_name
			thing = thing.replace(' ', '-')
			merit_set.add(thing)

		return render_template('/mytrails.html', remaining_trails=remaining_trails,
												 completed_trails=completed_trails,
												 merit_list=merit_set)
	else:
		flash("Please login to begin your adventure.")
		return render_template('/welcome.html')


@app.route('/trail/<trail_id>')
def show_trail_info(trail_id):

	# This one does not need a session.
	trail = model.db.session.query(model.Trail).filter(model.Trail.trail_id==trail_id).first()
	all_users_trails = model.db.session.query(model.Trek).filter(model.Trek.user_id==session['user_id']).all()
	if all_users_trails:
		for trek in all_users_trails:
			if trek.trail_id == trail.trail_id:
				in_my_trails = []
			else:
				in_my_trails = [" "]
	else:
		in_my_trails = [" "]

	return render_template('/trail.html', trail=trail, in_my_trails = in_my_trails)


@app.route('/directions', methods=['POST'])
def make_google_maps_link():
	"""Logic for creating Google Maps Directions link <3"""

	trail_name = request.form.get('trail_name')
	trail_id = request.form.get('trail_id')
	origin = request.form.get('origin')
	origin = origin.replace(',','')
	origin = origin.split()
	origin = "+".join(origin)
	print 'ORIGIN: ', origin

	destination = request.form.get('destination')
	phone_number = request.form.get('phone_number')
	print 'PHONE NUMBER: ', phone_number
	print 'DESTINATION: ', destination
	print 'TRAIL ID', trail_id
	google_maps_url = "https://www.google.com/maps/dir/" + origin + "/" + destination
	body = "Trail Quest Google Map Link to " + trail_name + ": " + google_maps_url
	send_sms.send_message(phone_number, body)
	functions.add_trek_to_users_trails(trail_id)

	return "User sent link."


@app.route('/submit_review', methods=['POST'])
def submit_trail_review():
	"""Logic for submitting trail_reviews"""

	review_text = request.form.get('review_text')
	user_id = session['user_id']
	trail_id = request.form.get('trail_id')
	functions.add_review_to_db(review_text, user_id, trail_id)
	functions.add_badge_if_applicable(trail_id)

	return "Success"


if __name__ == "__main__":
	app.debug = False
	# DebugToolbarExtension(app)
	connect_to_db(app)
	# functions.load_badges()
	app.run(host='0.0.0.0')
