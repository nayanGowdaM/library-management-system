class Books(): # Data structure for book info 
	id = 0
	name = ""
	edition = ""
	year = ""
	count = 0
	availability = False

	course = {}

	def __init__(self, BookDAO):
		self.dao = BookDAO
		self.route_url = "/books/"