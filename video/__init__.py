from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config.from_object('video.settings')

db = MongoAlchemy(app)

from views import *
