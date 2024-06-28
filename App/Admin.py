from App.Actor import Actor

class Admin(Actor):  #Inherits from actor class 
	admin = {}
	
	def __init__(self, AdminDAO):
		self.sess_key = "admin" #Sets the session key to "admin"
		self.dao = AdminDAO #assigns the AdminDAO object to the dao attribute of the Admin instance. AdminDAO is presumably a Data Access Object that handles database operations related to admin users.
		self.route_url = "/admin/" # Sets the base URL for routing to "/admin/"