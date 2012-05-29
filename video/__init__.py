from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy

app = Flask(__name__)

#mongolab
#mongo ds033047.mongolab.com:33047/video -u video -p video1

#mongodb://video:video1@ds033047.mongolab.com:33047/video

app.config['MONGOALCHEMY_SERVER'] = 'ds033047.mongolab.com'
app.config['MONGOALCHEMY_PORT'] = '33047'
app.config['MONGOALCHEMY_USER'] = 'video'
app.config['MONGOALCHEMY_PASSWORD'] = 'video1'
app.config['MONGOALCHEMY_DATABASE'] = 'video'
app.config['MONGOALCHEMY_SERVER_AUTH'] = False

app.config['SECRET_KEY'] = 'very secret, do you believe?'
app.config['DEBUG'] = True

db = MongoAlchemy(app)

from views import *
