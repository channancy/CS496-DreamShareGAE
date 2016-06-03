import webapp2
from google.appengine.ext import ndb
import db_models
import json

class User(webapp2.RequestHandler):
	def post(self):
		"""Creates a User entity

		POST Body Variables:
		fname - user's first name (Required)
		lname - user's last name (Required)
		email - user email address (Required)
		password - user password (Required)
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return

		# Create user
		new_user = db_models.User()

		# Set first name
		fname = self.request.get('fname', default_value=None)
		if fname:
			new_user.fname = fname
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, first name is required"
			return

		# Set last name
		lname = self.request.get('lname', default_value=None)
		if lname:
			new_user.lname = lname
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, last name is required"
			return

		# Set email
		email = self.request.get('email', default_value=None)
		if email:
			# Convert to lowercase
			new_user.email = email.lower()
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, email is required"
			return

		# Set password
		password = self.request.get('password', default_value=None)
		if password:
			new_user.password = password
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, password is required"
			return

		# Save to database
		key = new_user.put()
		out = new_user.to_dict()
		self.response.write(json.dumps(out))
		return

	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return

		# Get user by id
		if 'id' in kwargs:
			user = ndb.Key(db_models.User, int(kwargs['id'])).get()
			if not user:
				self.response.status = 404
				self.response.status_message = "User Not Found"
				return

			# Dump that to a json string and write that back as a response
			out = user.to_dict()
			self.response.write(json.dumps(out))

		# Get user by email
		elif 'email' in kwargs:
			# Case-insensitive search
			user_email = kwargs['email'].lower()
			user = db_models.User.query().filter(db_models.User.email == user_email).get()
			if not user:
				self.response.status = 404
				self.response.status_message = "User Not Found"
				return
			
			out = user.to_dict()
			self.response.write(json.dumps(out))

		# Else return all the users
		else:
			q = db_models.User.query()
			keys = q.fetch(keys_only=True)
			results = { 'users' : [ndb.Key(db_models.User, x.id()).get().to_dict() for x in keys]}
			self.response.write(json.dumps(results))