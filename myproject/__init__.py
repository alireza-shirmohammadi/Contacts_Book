from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


app = Flask(__name__, static_url_path="/static")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "sqlite")
app.config["SQLALCHEMY_TRACK_MOFICATIONS"] = False
app.config["SECRET_KEY"] = "mysecretkey"

db = SQLAlchemy(app)
Migrate(app, db)

from myproject.contacts.views import contacts_bluprint

app.register_blueprint(contacts_bluprint, url_prefix="/contacts")
