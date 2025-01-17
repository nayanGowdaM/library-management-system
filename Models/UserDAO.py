class UserDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "users"


	def list(self):
		query = """
		SELECT
			@table.id,
			@table.name,
			@table.email,
			@table.bio,
			@table.mob,
			@table.lock,
			@table.created_at,
			COUNT(reserve.book_id) as books_owned
		FROM @table
		LEFT JOIN reserve ON reserve.user_id=@table.id
		GROUP BY
			@table.id,
			@table.name,
			@table.email,
			@table.bio,
			@table.mob,
			@table.lock,
			@table.created_at
		"""
		users = self.db.query(query).fetchall()
		return users

	def getById(self, id):
		q = self.db.query("select * from @table where id='{}'".format(id))

		user = q.fetchone()

		return user

	def getUsersByBook(self, book_id):
		q = self.db.query("select * from @table LEFT JOIN reserve ON reserve.user_id = @table.id WHERE reserve.book_id={}".format(book_id))

		user = q.fetchall()

		return user

	def getByEmail(self, email):
		q = self.db.query("select * from @table where email='{}'".format(email))

		user = q.fetchone()

		return user

	def add(self, user):
		name = user['name']
		email = user['email']
		password = user['password']
		bio = user['bio']
		mob = user['mobile']
		lock = user['lock']

		q = self.db.query("INSERT INTO @table (name, email, password, bio, mob) VALUES('{}', '{}', '{}', '{}', '{}');".format(name, email, password, bio, mob))
		self.db.commit()
		
		return q


	def update(self, user, _id):
		name = user['name']
		email = user['email']
		password = user['password']
		bio = user['bio']

		q = self.db.query("UPDATE @table SET name = '{}', email='{}', password='{}', bio='{}' WHERE id={}".format(name, email, password, bio, _id))
		self.db.commit()
		
		return q
