from App.Admin import Admin

class AdminManager():
	def __init__(self, DAO):
		self.admin = Admin(DAO.db.admin)  # It has a admin object
		self.user = DAO.db.user # DB Users 
		self.dao = self.admin.dao # To know to which dao each obj belongs

# Method to handle admin sign-in
	def signin(self, email, password):
		admin = self.dao.getByEmail(email) # Retrieve the admin record from the database using the provided email

		if admin is None: # Check if the admin record exists
			return False

		admin_pass = admin["password"] 
		if admin_pass != password:
			return False

		return admin # Return the admin record if the email and password match
		
  
#    Method to retrieve an admin record by ID
	def get(self, id):
		admin = self.dao.getById(id)

		return admin
		
#   # Method to retrieve and print a list of users
	def getUsersList(self):
		admin = self.user.list()
		print(admin)

		return admin

# Method to handle admin sign-out
	def signout(self):
		self.admin.signout()   #Removes admin from the session 

# Method to retrieve a list of users
	def user_list(self):
		return self.user.list()