from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager ############# added this line

from resources.songs import song # adding this line
from resources.user import user ############ added this line

import models

DEBUG = True
PORT = 8000

login_manager = LoginManager() # sets up the ability to set up the session

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

###################### added these lines

app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD" ## Need this to encode the session
login_manager.init_app(app) # set up the sessions on the app

@login_manager.user_loader # decorator function, that will load the user object whenever we access the session, we can get the user
# by importing current_user from the flask_login
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None
###################### added these lines

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(song, origins=['http://localhost:3000'], supports_credentials=True) 


app.register_blueprint(song, url_prefix='/api/songs')


# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'

################## added these lines
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')
################## added these lines



# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)