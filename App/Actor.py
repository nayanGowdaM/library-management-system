from functools import wraps
from flask import g, request, redirect, session



# g: An object for storing data during the request cycle.
# request: An object representing the current request.
# redirect: A function to redirect the client to a different location.
# session: A dictionary-like object to store data across requests (session management).

class Actor():
	sess_key = ""
	route_url = "/"

# A method to return the user ID if the user is logged in.
	def uid(self):
		if self.isLoggedIn():
			return session[self.sess_key]

		return "err"

# A method to set the user in the global g object.
	def set_session(self, session, g):
		g.user = 0

		if self.isLoggedIn():
			g.user = session[self.sess_key]

#  A method to check if a user is logged in.
	def isLoggedIn(self):
		if self.sess_key in session and session[self.sess_key] and session[self.sess_key]>0:
			return True

		return False
# A decorator method to protect routes requiring login
	def login_required(self, f, path="signin"):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if self.sess_key not in session or session[self.sess_key] is None:
				print(path)
				return redirect(self.route_url+path)
			return f(*args, **kwargs)
		return decorated_function
#  A decorator method to redirect users to home if they are already logged in
	def redirect_if_login(self, f, path="/"):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if self.sess_key in session and session[self.sess_key] is not None:
				return redirect(self.route_url+path)
			return f(*args, **kwargs)
		return decorated_function
#  A method to log the user out by setting the session key to None
	def signout(self):
		session[self.sess_key] = None
# A placeholder method for signing in. Currently does nothing but can be implemented as needed.
	def signin(self):
		pass