from . import db
import datetime


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    phone = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __repr__(self):
        return self.name
