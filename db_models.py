from google.appengine.ext import ndb

class Model(ndb.Model):
	# A key cannot be jsonified
	# (cannot just turn key into a json string)
	# Override to_dict() method
	def to_dict(self):
		# Call the super (the original) to_dict() which doesn't include the key
		d = super(Model, self).to_dict()
		# Then we add the key by pulling out its id
		d['key'] = self.key.id()		
		return d

class Dream(Model):
	user = ndb.KeyProperty(required=True)
	username = ndb.StringProperty(required=True)
	description = ndb.StringProperty(required=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

	def to_dict(self):
		# http://stackoverflow.com/questions/1531501/json-serialization-of-google-app-engine-models
		# jsonify datetime
		d = dict([(p, unicode(getattr(self, p))) for p in self._properties])
		# Pull out ids for dream and user
		d['key'] = self.key.id()
		d['user'] = self.user.id()
		return d

class User(Model):
	name = ndb.StringProperty(required=True)
	location = ndb.StringProperty(required=True)
	dreams = ndb.KeyProperty(repeated=True)

	def to_dict(self):
		# super, so it will call to_dict() in class Model which in turn
		# calls to_dict() of ndb.Model
		d = super(User, self).to_dict()
		# Replacing what is there that cannot be handled because it's a list of keys
		# Pull out ids from each key
		# (Override a method and replace a property)
		d['dreams'] = [r.id() for r in d['dreams']]
		return d