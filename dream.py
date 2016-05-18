import webapp2
from google.appengine.ext import ndb
import db_models
import json
from django.utils import simplejson
import datetime

class Dream(webapp2.RequestHandler):
	def post(self, **kwargs):
		"""Creates a Dream entity

		POST Body Variables:
		description - description of the user dream (Required)
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"

		if 'uid' in kwargs:
			# Pull out user id
			user_key = ndb.Key(db_models.User, int(kwargs['uid']))
			if not user_key:
				self.response.status = 404
				self.response.status_message = "User Not Found"
				return
			user = user_key.get()

		new_dream = db_models.Dream()
		new_dream.user = user_key

		description = self.request.get('description', default_value=None)
		if description:
			new_dream.description = description
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, dream description is required"
			return

		# Save to database
		dream_key = new_dream.put()

		# Add dream to user
		user.dreams.append(dream_key)
		# Save changes to user
		user.put()

		# simplejson for serialization of datetime
		self.response.out.write(simplejson.dumps(new_dream.to_dict()))
		return

	def get(self, **kwargs):
		"""
		Show a dream by id or list all dreams
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return

		# If 'id' specified in keyword arguments
		# See main.py: r'/dream/<id:[0-9]+><:/?>'
		if 'id' in kwargs:
			# Make a key: ndb.Key('type', 'id')
			# Every key takes a type and an id
			# db_models.Dream is the type that is passed in
			# kwargs['id'] is the id that is passed in
			# .get(): From the key, get the dream
			# .to_dict(): Turn the dream into a dictionary
			dream = ndb.Key(db_models.Dream, int(kwargs['id'])).get()
			if not dream:
				self.response.status = 404
				self.response.status_message = "Dream Not Found"
				return

			# Dump that to a json string and write that back as a response
			out = dream.to_dict()
			self.response.write(json.dumps(out))

		# Else no 'id' in keyword arguments, then return all the dreams
		else:
			q = db_models.Dream.query()
			keys = q.fetch(keys_only=True)
			# Make Key by passing in Type and ID
			# Make dictionary of all database properties and values for each dream
			# and dump that to a json string and write that back as a response
			results = { 'dreams' : [ndb.Key(db_models.Dream, x.id()).get().to_dict() for x in keys]}
			self.response.write(json.dumps(results))

	def put(self, **kwargs):
		"""
		Edit a dream
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return

		if 'id' in kwargs:
			dream = ndb.Key(db_models.Dream, int(kwargs['id'])).get()
			if not dream:
				self.response.status = 404
				self.response.status_message = "Dream Not Found"
				return

			description = self.request.get('description', default_value=None)
			if description:
				# Update description and date of dream
				dream.description = description
				dream.date = datetime.datetime.now()

			# Save changes to dream
			dream.put()

			# Dump that to a json string and write that back as a response
			out = dream.to_dict()
			self.response.write(json.dumps(out))
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, Dream ID is Required"
			return		
	
	def delete(self, **kwargs):
		"""
		Delete a dream
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return

		if 'id' in kwargs:
			dream_key = ndb.Key(db_models.Dream, int(kwargs['id']))
			if not dream_key:
				self.response.status = 404
				self.response.status_message = "Dream Not Found"
				return

			# Get dream to delete the entity
			# Get user to delete references to the dream
			dream = dream_key.get()
			user = ndb.Key(db_models.User, dream.user.id()).get()

			# Delete dream from user
			if dream_key in user.dreams:
				index = user.dreams.index(dream_key)
				del user.dreams[index]
			# Save changes to user
			user.put()

			# Before deleting, get dream as dictionary for response
			out = dream.to_dict()
			# Now delete the dream and write back the response
			dream.key.delete()
			self.response.write(json.dumps(out))
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, Dream ID is Required"
			return