from App.Actor import Actor

class User(Actor):
	id = 0
	name = ""
	lock = False # A class attribute to indicate whether the user is locked, initialized to False

	user = {}

	def __init__(self, UserDAO):
		self.dao = UserDAO
		self.sess_key = "user" # session key