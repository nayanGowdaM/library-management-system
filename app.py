from flask import Flask, g, escape, session, redirect, render_template, request, jsonify, Response, url_for
from Misc.functions import *

app = Flask(__name__)
app.secret_key = '#$ab9&^BB00_.'  # secret key is set for session management.

# Setting DAO Class
from Models.DAO import DAO

DAO = DAO(app)

# Registering blueprints
from routes.user import user_view
from routes.book import book_view
from routes.admin import admin_view

# Registering custom functions to be used within templates
app.jinja_env.globals.update(
    ago=ago,
    str=str,
)


# connects the blueprint with the main application
app.register_blueprint(user_view,  url_prefix='/users/')
app.register_blueprint(book_view,  url_prefix='/books/')
app.register_blueprint(admin_view,  url_prefix='/admin/')



@app.route('/', methods=['GET'])
def home():


	return redirect( url_for('user_routes.home'))