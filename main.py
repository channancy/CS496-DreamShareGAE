#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import oauth

app = webapp2.WSGIApplication([
	('/users', 'user.User'),
], debug=True)
app.router.add(webapp2.Route(r'/users/<id:[0-9]+><:/?>', 'user.User'))
app.router.add(webapp2.Route(r'/dreams', 'dream.Dream'))
app.router.add(webapp2.Route(r'/dreams/<id:[0-9]+><:/?>', 'dream.Dream'))
app.router.add(webapp2.Route(r'/dreams/users/<uid:[0-9]+><:/?>', 'dream.Dream'))
