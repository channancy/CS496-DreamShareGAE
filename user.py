import webapp2
from google.appengine.ext import ndb
import db_models
import json

class User(webapp2.RequestHandler):
	def post(self):
		"""Creates a User entity

		POST Body Variables:
		name - user name (Required)
		location - user location (Required)
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return

		new_user = db_models.User()
		name = self.request.get('name', default_value=None)
		
		if name:
			new_user.name = name
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, name is required"
			return

		location = self.request.get('location', default_value=None)
		
		if location:
			new_user.location = location
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, location is required"
			return

		key = new_user.put()
		out = new_user.to_dict()
		self.response.write(json.dumps(out))
		return

	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return

		if 'id' in kwargs:
			user = ndb.Key(db_models.User, int(kwargs['id'])).get()
			if not user:
				self.response.status = 404
				self.response.status_message = "User Not Found"
				return

			# Dump that to a json string and write that back as a response
			out = user.to_dict()
			self.response.write(json.dumps(out))

		# Else no 'id' in keyword arguments, then return all the users
		else:
			q = db_models.User.query()
			keys = q.fetch(keys_only=True)
			results = { 'users' : [ndb.Key(db_models.User, x.id()).get().to_dict() for x in keys]}
			self.response.write(json.dumps(results))