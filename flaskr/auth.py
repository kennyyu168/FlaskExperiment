# Filename: auth.py
# Author: Kenny Yu
# Date: 8/6/19

import functools

from flask import( Blueprint, flash, g, redirect, render_template, request,
    session, url_for ) 
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Creates a Blueprint named 'auth' for authentication 
bp = Blueprint( 'auth', __name__, url_prefix='/auth' )

# Function Name: register()
# Function Description: Returns HTML with a form for user to fill out, 
#     when form is submitted, either an error message will show or
#     the user is created and is prompted to log in
@bp.route( '/register', methods=( 'GET', 'POST' ) )
def register(): 
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		if not username: 
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif db.execute('SELECT if FROM user WHERE username = ?', 
		     (username,) ).fetchone() is not NONE:
		     error = 'User {} is already registered.'.format(username)

		if error is None:
			db.execute( 'INSERT INTO user (username, password) VALUES (?, ?)',
			    ( username, generate_password_hash(password) ) )
			db.commit()
			return redirect( url_for( 'auth.login' ) )

		flash( error )

	return render_template( 'auth/register.html' )

# Function Name: login()
# Function Description: 
@bp.route( '/login', methods=( 'GET', 'POST' ) )
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute( 'SELECT * FROM user WHERE username = ?', 
		    (username,).fetchone()

		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash( user['password'], password ):
			error = 'Incorrect password.'

		if error is None: 
			session.clear()
			session['user_id'] = user['id']
			return redirect( url_for( 'index' ) )

		flash( error )

	return render_template( 'auth/login.html' )



