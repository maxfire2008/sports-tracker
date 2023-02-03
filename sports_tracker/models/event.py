from ..extensions import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    archived = db.Column(db.Boolean, nullable=False)
    archived_time = db.Column(db.DateTime)
