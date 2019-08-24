# Filename: __init__.py
# Author: Kenny Yu
# Date: 7/28/19

# Import 
import os

# Import flask functions
from flask import Flask

# Function Name: create_app()
# Function Description: Application factory function, once it's called, it
#     sets up and configures the app.
def create_app ( test_config=None ):
	
	# Create and configure app
	app = Flask( __name__, instance_relative_config=True )
	app.config.from_mapping( SECRET_KEY='dev', 
	    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite' ), )
	
	# If there isn't a test config
	if test_config is None:
		
		# Load the instance config, if it exists, when not testing
		app.config.from_pyfile( 'config.py', silent=True )

	else: 
		
		# Load the test config if passed in
		app.config.from_mapping( test_config )

	# Ensure the instance folder exists
	try:
		os.makedirs( app.instance_path )
	except OSError:
		pass

	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	# Brings in functions from the db.py file
	from . import db

	# Initializes the app
	db.init_app( app )

	# registers new users 
	from . import auth
	app.register_blueprint( auth.bp )

	# initializes the blog
	from . import blog
	app.register_blueprint( blog.bp )
	app.add_url_rule( '/', endpoint='index' )

	return app

