from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, flash,url_for
from app import DAO  # Data object model that has been initialized with the app 
from Misc.functions import *

from Controllers.UserManager import UserManager


#  Blueprint in Flask is a way to organize your application into modular components
# A new Blueprint instance named user_view is created.
# This blueprint is associated with the name 'user_routes'.
# The __name__ variable helps Flask to know where this blueprint is defined.
# The template_folder='/templates' argument tells Flask to look for templates in the /templates directory when rendering views associated with this blueprint.
user_view = Blueprint('user_routes', __name__, template_folder='/templates')  

user_manager = UserManager(DAO)

@user_view.route('/', methods=['GET'])
def home():
	g.bg = 1

	user_manager.user.set_session(session, g)
	print(g.user)

	return render_template('home.html', g=g)


@user_view.route('/signin', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signin():
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('signin.html', error="Email and password are required")

		d = user_manager.signin(email, hash(password))

		if d and len(d)>0:
			session['user'] = int(d['id'])

			return redirect("/")

		return render_template('signin.html', error="Email or password incorrect")


	return render_template('signin.html')


@user_view.route('/signup', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        bio = request.form.get('bio')
        mobile = request.form.get('mobile')

        if len(name) < 1 or len(email) < 1 or len(password) < 1 or len(bio) < 1 or len(mobile) < 1:
            return render_template('signup.html', error="All fields are required")

        new_user = user_manager.signup(name, email, hash(password), bio, mobile)

        if new_user == "already_exists":
            return render_template('signup.html', error="User already exists with this email")

        return render_template('signup.html', msg="You've been registered!")

    return render_template('signin.html')


@user_view.route('/signout/', methods=['GET'])
@user_manager.user.login_required
def signout():
	user_manager.signout()

	return redirect("/", code=302)

@user_view.route('/user/', methods=['GET'])
@user_manager.user.login_required
def show_user(id=None):
	user_manager.user.set_session(session, g)
	
	if id is None:
		id = int(user_manager.user.uid())

	d = user_manager.get(id)
	mybooks = user_manager.getBooksList(id)

	return render_template("profile.html", user=d, books=mybooks, g=g)

@user_view.route('/user/', methods=['POST'])
@user_manager.user.login_required
def update():
	user_manager.user.set_session(session, g)
	
	_form = request.form
	name = str(_form["name"])
	email = str(_form["email"])
	password = str(_form["password"])
	bio = str(_form["bio"])

	user_manager.update(name, email, hash(password), bio, user_manager.user.uid())

	flash('Your info has been updated!')
	return redirect(url_for('user_routes.show_user'))