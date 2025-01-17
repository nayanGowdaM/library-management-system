class BookDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "books"

	def delete(self, id):
		q = self.db.query("DELETE FROM @table where id={}".format(id))
		self.db.commit()

		return q


	def reserve(self, user_id, book_id):
		if not self.available(book_id):
			return "err_out"

		q = self.db.query("INSERT INTO reserve (user_id, book_id) VALUES('{}', '{}');".format(user_id, book_id))
		
		self.db.query("UPDATE @table set count=count-1 where id={};".format(book_id))
		self.db.commit()

		return q

	def getBooksByUser(self, user_id):
		q = self.db.query("select * from @table left join reserve on reserve.book_id = @table.id where reserve.user_id={}".format(user_id))

		books = q.fetchall()

		print(books)
		return books

	def getBooksCountByUser(self, user_id):
		q = self.db.query("select count(reserve.book_id) as books_count from @table left join reserve on reserve.book_id = @table.id where reserve.user_id={}".format(user_id))

		books = q.fetchall()

		print(books)
		return books

	def getBook(self, id):
		q = self.db.query("select * from @table where id={}".format(id))

		book = q.fetchone()

		print(book)
		return book

	def available(self, id):
		book = self.getById(id)
		count = book['count']

		if count < 1:
			return False

		return True

	def getById(self, id):
		q = self.db.query("select * from @table where id='{}'".format(id))

		book = q.fetchone()

		return book

	def list(self, availability=1):
		query="select * from @table"
		# Usually when no-admin user query for book
		if availability==1: query= query+"  WHERE availability={}".format(availability)
		
		books = self.db.query(query)
		
		books = books.fetchall()


		return books

	def getReserverdBooksByUser(self, user_id):
		query="select concat(book_id,',') as user_books from reserve WHERE user_id={}".format(user_id)
		
		books = self.db.query(query)
		
		books = books.fetchone()


		return books

	def search_book(self, name, availability=1):
		query="select * from @table where name LIKE '%{}%'".format(name)

		# Usually when no-admin user query for book
		if availability==1: query= query+"  AND availability={}".format(availability)

		q = self.db.query(query)
		books = q.fetchall()
		
		return books


	def update_book( self, book_info):
		id = book_info['id']
		title = book_info['title']
		qty = book_info['qty']
		available = book_info['available']
		desc = book_info['desc']
		q = self.db.query("UPDATE @table SET name = '{}',count='{}', availability='{}', @table.desc='{}' WHERE id={}".format(title,qty, available, desc,  id))
		self.db.commit()
  
	def add_book( self, book_info):
		name = book_info['name']
		author  = book_info['author']
		edition = book_info['edition']
		count = book_info['count']
		availability = book_info['availabilityv']
		desc = book_info['desc']
		q = self.db.query("INSERT INTO @table (name,author, edition,count, availability, @table.desc) VALUES('{}', '{}', '{}','{}', '{}', '{}');".format(name, author, edition, count, availability, desc))
		self.db.commit()