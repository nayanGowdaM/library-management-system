from App.Books import Books

class BookManager():
	def __init__(self, DAO):
		self.misc = Books(DAO.db.book)  # It has a book object
		self.dao = self.misc.dao  # Tells which dao each obj is using 

# List Books 
	def list(self, availability=1,user_id=None):
		if user_id!= None:  
			book_list = self.dao.listByUser(user_id)  #lists books reserved by that user.
		else:
			book_list = self.dao.list(availability) #t lists books based on availability.

		return book_list


# #lists books reserved by that user.
	def getReserverdBooksByUser(self, user_id):
		books = self.dao.getReserverdBooksByUser(user_id)

		return books


#  retrieves a book by its ID.
	def getBook(self, id):
		books = self.dao.getBook(id)

		return books

# searches for books by a keyword and availability status.
	def search(self, keyword, availability=1):
		books = self.dao.search_book(keyword, availability)

		return books

#  Reserves book_id for user_id
	def reserve(self, user_id, book_id):
		books = self.dao.reserve(user_id, book_id)

		return books

# retrieves books associated with a specific user.
	def getUserBooks(self, user_id):
		books = self.dao.getBooksByUser(user_id)

		return books

# retrieves the count of books associated with a specific user.
	def getUserBooksCount(self, user_id):
		books = self.dao.getBooksCountByUser(user_id)

		return books

# deletes a book by its ID.
	def delete(self, id):
		self.dao.delete(id)