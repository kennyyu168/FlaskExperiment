# Imports flask and all of its functions
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
	return 'Hello, World!'

