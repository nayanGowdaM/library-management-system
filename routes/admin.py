from flask import Blueprint, g, escape, session, redirect, render_template, request, flash ,  jsonify, Response, url_for
from app import DAO
from Misc.functions import *

from Controllers.AdminManager import AdminManager
from Controllers.BookManager import BookManager
from Controllers.UserManager import UserManager

admin_view = Blueprint('admin_routes', __name__, template_folder='/templates/')

book_manager = BookManager(DAO)
user_manager = UserManager(DAO)
admin_manager = AdminManager(DAO)


@admin_view.route('/', methods=['GET'])
# @admin_manager.admin.login_required
def home():
	g.bg = 1
	admin_manager.admin.set_session(session, g)

	return render_template('admin/home.html', g=g)



@admin_view.route('/signin/', methods=['GET', 'POST'])
@admin_manager.admin.redirect_if_login
def signin():
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('admin/signin.html', error="Email and password are required")

		d = admin_manager.signin(email, hash(password))

		if d and len(d)>0:
			session['admin'] = int(d["id"])

			return redirect("/admin")

		return render_template('admin/signin.html', error="Email or password incorrect")

	return render_template('/admin/signin.html')


@admin_view.route('/signup/', methods=['GET', 'POST'])
@admin_manager.admin.redirect_if_login
def signup():

	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		if  len(email) < 1 or len(password) < 1 :
			return render_template('admin/signup.html', error="All fields are required")

		new_admin = admin_manager.signup( email, hash(password))

		if new_admin == "already_exists":
			return render_template('admin/signup.html', error="User already exists with this email")

		return render_template('admin/signin.html', msg="You've been registered!")

	return render_template('admin/signup.html')


@admin_view.route('/signout/', methods=['GET'])
@admin_manager.admin.login_required
def signout():
	admin_manager.signout()

	return redirect(url_for('admin_routes.home'), code=302)


@admin_view.route('/users/view/', methods=['GET'])
@admin_manager.admin.login_required
def users_view():
	admin_manager.admin.set_session(session, g)

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)
	myusers = admin_manager.getUsersList()

	return render_template('admin/users.html', g=g, admin=admin, users=myusers)



@admin_view.route('/books/', methods=['GET'])
@admin_manager.admin.login_required
def books():
	admin_manager.admin.set_session(session, g)

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)
	mybooks = book_manager.list(availability=0)

	return render_template('admin/books/views.html', g=g, books=mybooks, admin=admin)

@admin_view.route('/books/<int:id>')
@admin_manager.admin.login_required
def view_book(id):
	admin_manager.admin.set_session(session, g)

	if id != None:
		b = book_manager.getBook(id)
		users = user_manager.getUsersByBook(id)

		print('----------------------------')
		print(users)
		
		if b and len(b) <1:
			return render_template('books/book_view.html', error="No book found!")

		return render_template("admin/books/book_view.html", books=b, books_owners=users, g=g)


@admin_view.route('/books/add', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def book_add():
	admin_manager.admin.set_session(session, g)
	
	return render_template('admin/books/add.html', g=g)




@admin_view.route('/books/delete/<int:id>', methods=['GET'])
@admin_manager.admin.login_required
def book_delete(id):
	id = int(id)

	if id is not None:
		book_manager.delete(id)
	
	return redirect('/admin/books/')


@admin_view.route('/books/search', methods=['GET'])
def search():
	admin_manager.admin.set_session(session, g)

	if "keyword" not in request.args:
		return render_template("books/view.html")

	keyword = request.args["keyword"]

	if len(keyword)<1:
		return redirect('/admin/books')

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)

	d=book_manager.search(keyword, 0)

	if len(d) >0:
		return render_template("admin/books/views.html", search=True, books=d, count=len(d), keyword=escape(keyword), g=g, admin=admin)

	return render_template('admin/books/views.html', error="No books found!", keyword=escape(keyword))



@admin_view.route('/books/edit/<int:id>', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def book_edit(id):
    admin_manager.admin.set_session(session, g)
    
    # Handle POST request for form submission
    if request.method == 'POST':
        title = request.form.get('title')
        qty = request.form.get('qty')
        available = int('available' in request.form)
        description = request.form.get('desc')

        # Ensure all required fields are filled
        if not title or not qty:
            flash('Please fill out all required fields', 'danger')
            return redirect(url_for('admin_routes.book_edit', id=id))
        
        
        book_manager.updateBook( id, title, qty, available, description)
        return redirect(url_for('admin_routes.books'))

		
    
    # Handle GET request to display edit form
    if id is not None:
        b = book_manager.getBook(id)

        if b is None or len(b) < 1:
            return render_template('admin/books/edit.html', error="No book found!")

        return render_template("admin/books/edit.html", book=b, g=g)
    
    return redirect('admin/books')