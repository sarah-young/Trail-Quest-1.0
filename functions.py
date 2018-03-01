"""Functions for Trail Quest"""

import secrets
import requests
import random
import model
#from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session

gm_api_key = secrets.GOOGLE_MAPS_API_KEY
hp_api_key = secrets.HIKING_PROJECT_API_KEY
satellite_map_api_key =secrets.SATELLITE_MAP_GM_API_KEY

#db = SQLAlchemy()

def load_badges():
	"""Create badges"""

	for i, row in enumerate(open("badge_seed_data.csv")):
	    row = row.rstrip()
	    badge_name, badge_description = row.split(",")

	    badge = model.Badge(badge_name=badge_name,
	                badge_description=badge_description)

	    # We need to add to the session or it won't ever be stored
	    model.db.session.add(badge)

	    # provide some sense of progress
	    if i % 100 == 0:
	        print i

	model.db.session.commit()
	print "Completed."


def add_badge_if_applicable(trail_id):
	"""
	When review is posted, check to see if badge should be added to user page.
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	badge_id = db.Column(db.Integer, db.ForeignKey('badges.badge_id'))
	merit_date = db.Column(db.DateTime)

	badges = db.relationship('Badge')
	users = db.relationship('User')
	"""

	trail = model.db.session.query(model.Trail).filter(model.Trail.trail_id==trail_id).first()
	badge_ownership_check = model.db.session.query(model.Merit).filter(model.Merit.badges.badge_name==badge_name, model.Merit.users.user_id==session['user_id']).first()
	if 'waterfall' in trail.trail_description or 'water fall' in trail.trail_description:
		badge_name = "water fall badge"
		b_o_c = badge_ownership_check
		if badge_ownership_check == None:
			merit = Merit(user_id = session['user_id'],
						  badge_id = 1)
			model.db.session.add(merit)
			print 'waterfall'

	if 'creek' in trail.trail_description:
		badge_name = "creek_badge"
		badge_ownership_check = model.db.session.query(model.Merit).filter(model.Merit.badges.badge_name==badge_name, model.Merit.users.user_id==session['user_id']).first()
		if badge_ownership_check == None:
			merit = Merit(user_id = session['user_id'],
						  badge_id = 2)
			model.db.session.add(merit)

	if "river" in trail.trail_description:
		badge_name = "river badge"
		badge_ownership_check = model.db.session.query(model.Merit).filter(model.Merit.badges.badge_name==badge_name, model.Merit.users.user_id==session['user_id']).first()
		if badge_ownership_check == None:
			merit = Merit(user_id = session['user_id'],
						  badge_id = 3)
			model.db.session.add(merit)

	if "outlook" in trail.trail_description:
		badge_name = "outlook_badge"
		badge_ownership_check = model.db.session.query(model.Merit).filter(model.Merit.badges.badge_name==badge_name, model.Merit.users.user_id==session['user_id']).first()
		if badge_ownership_check == None:
			merit = Merit(user_id = session['user_id'],
						  badge_id = 4)
			model.db.session.add(merit)

	if int(trail.trail_high_alt) - int(trail.trail_low_alt) > 500:
		badge_name = "outlook_badge"
		badge_ownership_check = model.db.session.query(model.Merit).filter(model.Merit.badges.badge_name==badge_name, model.Merit.users.user_id==session['user_id']).first()
		if badge_ownership_check == None:
			merit = Merit(user_id = session['user_id'],
						  badge_id = 5)
			model.db.session.add(merit)

	if "redwood" in trail.trail_description:
		badge_name = "redwood badge"
		badge_ownership_check = model.db.session.query(model.Merit).filter(model.Merit.badges.badge_name==badge_name, model.Merit.users.user_id==session['user_id']).first()
		if badge_ownership_check == None:
			merit = Merit(user_id = session['user_id'],
						  badge_id = 6)
			model.db.session.add(merit)

	if "wild flower" in trail.trail_description or "wildflower" in trail.trail_description:
		print 'wild flower'
	if "fern" in trail.trail_description:
		print 'fern'
	if "meadow" in trail.trail_description:
		print 'meadow'
	if "mountain" in trail.trail_description:
		print 'mountain'
	if "deer" in trail.trail_description:
		print 'deer'
	# if query for how many reviews have been submitted > 0:
		# print first trek
	# if query for how many reviews have been submitted > 4:
		# print high five
	# if quest for how many treks are in trek database for user > 0:
		# print trailhead

def add_review_to_db(review_text, user_id, trail_id):
	""" Add review from user to DB """

	review_check = model.db.session.query(model.Review).filter(model.Review.user_id==user_id, model.Review.trail_id==trail_id).first()

	if review_check == None:
		review = model.Review(user_id = user_id,
						  trail_id = trail_id,
						  review_text = review_text)
		model.db.session.add(review)
		model.db.session.commit()
	else:
		print "Review for this trail by user already in database."

def add_trek_to_users_trails(id_of_trail):
	"""Check to see if trek is already in user's trails.

	If it isn't, add to Trek database"""

	user_treks = check_user_treks(id_of_trail)
	print "PRINT USER TREKS: ", user_treks
	if user_treks == None:
		print "HERE - NONE"

		trek = model.Trek(user_id = session['user_id'],
					  	trail_id = id_of_trail)
		model.db.session.add(trek)
		model.db.session.commit()
		return "NEW TRAIL ADDED TO TREK DB."

	elif user_treks != None:
		return "TRAIL ALREADY EXISTS IN DATABASE."

def get_all_user_treks():
	"""Get all user treks from user_trails table by querying database using
	session['user_id']
	"""
	all_user_treks = model.db.session.query(model.Trek).filter(model.Trek.user_id==session['user_id']).all()

	return all_user_treks

def check_user_treks(id_of_trail):
	"""Query database to see if user has trails.

	"""
	user_treks = model.db.session.query(model.Trek).filter(model.Trek.user_id==session['user_id'], model.Trek.trail_id==id_of_trail).first()
	# see if a trek that matches the user_id from the session AND the trail_id argument is in the database

	if user_treks == None:
		return None
	else:
		return 'Trek in database'


def extract_relevant_trail_info(trail_object):
	"""Extract relevant trail info from trail object for use in
	map on front end

	"""

	trail = trail_object

	difficulty = trail_difficulty_conversion(trail.trail_difficulty)
	print "RELEVANT TRAIL INFO PRINT TESTS"
	print "Difficulty: ", difficulty
	alt_delta = trail.trail_high_alt - trail.trail_low_alt
	print "Alt Delta: ",alt_delta
	trailhead_lat = trail.trailhead_latitude
	trailhead_long = trail.trailhead_longitude
	print trailhead_lat, trailhead_long

	return [trailhead_lat, trailhead_long, trail.trail_name, trail.trail_length, trail.trail_id, difficulty, trail.trail_description, alt_delta, trail.trail_picture]

def get_dirxns(starting_address, trail_coordinates):
	"""Return dirxns from Google API based on trail lat/long"""

	dirxns = requests.get("http://maps.googleapis.com/maps/api/directions/json?origin="+starting_address+"&destination="+trail_coordinates+"&key=AIzaSyBZF-t6AgPD_FNUmxTd5M9gITpYKJDOmHs")

	dirxns_post_json = dirxns.json()
	print dirxns_post_json

	return dirxns


def get_trail_object_by_id(trail_id):
	"""Query database for trail object by trail id."""

	trail_object = model.db.session.query(model.Trail).filter(model.Trail.trail_id==trail_id).first()
	if trail_id:
		return trail_object

	else:
		return None

def add_user_to_database(username, password):
	"""Check to see if user is in database. If they aren't add them."""

	user_name_check = model.db.session.query(model.User).filter(model.User.user_name==username).first()

	if user_name_check == None:
		user = model.User(user_name = username,
					  user_password = password)
		model.db.session.add(user)
		model.db.session.commit()
		print "<Added user %s to database>" % username
		return True
	else:
		print "<User %s is already in the database>" % username
		return False

def find_lat_lng(city, state):
	"""
	Find lat/long for address given by user.

	Uses Google Maps API & Hiking Project API.

	Information passed from HTML form to this function.

	"""
	try:
		geocode_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+city+","+state+"US&key="+gm_api_key)
		json_geocode = geocode_request.json()
		lat,lng = json_geocode['results'][0].get('geometry').get('location').values()
		coordinates = (str(lat),str(lng),)

		return coordinates

	except:

		return None

def check_user_credentials(username, password):
	"""
	Compare user entered credentials to credentials in database!

	"""
	user = model.db.session.query(model.User).filter(model.User.user_name==username).first()

	if user:
		if user.user_password == password:
			print "BLUEBERRIES!!!!"
			return user
		else:
			return False
	else:
		return False

def find_trails(coordinates, radius='25'):
	"""Find trails based on GPS coordinates from find_lat_lng

	Uses Hiking Project API

	"""

	lat, lng = coordinates
	# Unpacking coordinates from Google Maps API
	trail_request = requests.get("https://www.hikingproject.com/data/get-trails?lat="+lat+"&lon="+lng+"&maxDistance="+radius+"&minLength=1&key="+hp_api_key)
	# Requesting trails near GPS coordinate from Hiking Project API
	trail_packet = trail_request.json()
	#
	trails = trail_packet["trails"]

	return trails


def select_three_trails(trails):
	"""Selects three random trails from trail_packet from find_trails

	"""

	print "***PRINT TRAIL TYPE*** ", type(trails)



	if len(trails) == 0:
		return None
	else:
		return trails

	# NOTE: Keeping logic below in case I want to revert
	# elif len(trails) < 4:
	# 	selected_trails = trails
	# 	# TODO: give message on route side that states user may want to widen search criteria
	#
	# 	return selected_trails
	#
	# elif len(trails) >=4:
	# 	selected_trails = []
	# 	random.shuffle(trails)
	# 	first_trail = trails.pop()
	# 	selected_trails.append(first_trail)
	# 	second_trail = trails.pop()
	# 	selected_trails.append(second_trail)
	# 	third_trail = trails.pop()
	# 	selected_trails.append(third_trail)
	#
	# 	return selected_trails


def add_trails_to_db(trails):
	"""Adds user selected trail to db"""

	for trail in trails:
		# print "LENGTH OF TRAILS: ", len(trails)
		# print "TRAIL NAME: ", trail['name']
		# print "TYPE: ", type(trail)
		trail_difficulty = trail_difficulty_conversion(trail['difficulty'])


		#FIXME: Should I move this under the if statement for optimization???

		trail_status = model.db.session.query(model.Trail).filter(model.Trail.trail_id==trail['id']).first()

		if trail_status == None:
		# If there is no trail with a matching trail id in the database, create new trail_object
			trail_object = model.Trail(trail_id = trail['id'],
			trail_name = trail['name'],
			trailhead_latitude = trail['latitude'],
			trailhead_longitude = trail['longitude'],
			trail_length = trail['length'],
			trail_difficulty = trail_difficulty,
			trail_description = trail['summary'],
			trail_high_alt = trail['high'],
			trail_low_alt = trail['low'],
			trail_location = trail['location'],
			trail_picture = trail['imgMedium'])

			model.db.session.add(trail_object)
			model.db.session.commit()
			print "<Added trail %s to database>" % trail['id']
		else:
			print "<Trail %s is already in the database>"



def get_trail_conditions(trail_id):
	"""Calls Hiking Project API for trail conditions using trail_id."""

	trail_id = str(trail_id)
	conditions_request = requests.get("https://www.hikingproject.com/data/get-conditions?ids="+trail_id+"&key="+hp_api_key)
	json_conditions = conditions_request.json()
	response = json_conditions["0"]
	trail_name_by_id = response.get("name")#.values()
	print "TRAIL NAME BY ID: ", trail_name_by_id
	trail_status_details =response.get("conditionStatus")#.values()
	print "TRAIL STATUS DETAILS: ", trail_status_details
	trail_status_color = response.get("conditionColor")#.values()
	print "TRAIL STATUS COLOR: ", trail_status_color
	trail_status_date = response.get("conditionDate")

	if trail_status_date.startswith("1970"):
	# Checks to see if there's a relevant trail condition report
		trail_deets = None
		print "NO REPORT AVAILABLE"
		return trail_deets
	elif trail_status_details.lower().startswith("unknown"):
		trail_deets = None
		print "NO REPORT AVAILABLE"
		return trail_deets

	trail_deets = (trail_name_by_id, trail_status_details, trail_status_color, trail_status_date,)

	return trail_deets

def filter_trek_length(trails, trek_length):
	"""Take trail list-object & filter for trails by trek length

	Called in select_three_trails()"""

	trail_list = []

	for trail in trails:
		if trail['length'] <= trek_length:
		# filters out trails that are too long
		# only appends trails to trail_list that are the same as the user's preference
			trail_list.append(trail)

	return trail_list


def filter_trek_difficulty(trails_filtered_by_length, trail_difficulty):
	"""Take trail list-object & filter trails by difficulty

	Called in select_three_trails()"""


	if trail_difficulty == "no-preference":
	# don't filter by difficulty --this list is the list we want to return.
		list_of_trails = trails_filtered_by_length
		return list_of_trails

	else:

		list_of_trails = []

		for trail in trails_filtered_by_length:

			trail_difficulty_rating = trail['difficulty']
			# from trail object, passed to conversion function
			print trail_difficulty_rating
			difficulty = trail_difficulty_conversion(trail_difficulty_rating)

			print "DIFFICULTY: ", difficulty

			if (difficulty == "easy" or difficulty == "easy/intermediate") and trail_difficulty == "easy":
				list_of_trails.append(trail)

			elif (difficulty == "intermediate" or difficulty == "easy/intermediate" or difficulty == "intermediate/difficult") and trail_difficulty == "moderate":
				list_of_trails.append(trail)

			elif (difficulty == "intermediate/difficult" or difficulty == "difficult" or difficulty == "very difficult") and trail_difficulty == "difficult":
				list_of_trails.append(trail)

		return list_of_trails


def trail_difficulty_conversion(trail_difficulty_rating):
	"""Take API's trail difficulty selection and return easy, moderate, difficult.

	Called in filter_trek_difficulty() """

	# trail_difficulty comes from user, difficulty is conversion from 'attribute' on trail object
	#trail['difficulty'] comes from API
	# handles one trail at a time

	if trail_difficulty_rating == "green":
		difficulty = "easy"

	elif trail_difficulty_rating == "greenBlue":
		difficulty = "easy/intermediate"

	elif trail_difficulty_rating == "blue":
		difficulty = "intermediate"

	elif trail_difficulty_rating == "blueBlack":
		difficulty = "intermediate/difficult"


	elif trail_difficulty_rating == "black":
		difficulty = "difficult"

	elif trail_difficulty_rating == "dblack":
		difficulty = "very difficult"

	else:
		difficulty = "unknown"

	return difficulty


def show_logout_button():
	"""Returns logic prompt frontend to show logout button when user is logged in"""

	if session.get('user_id'):
		show_logout_button = True
	else:
		show_logout_button = False
	return show_logout_button
