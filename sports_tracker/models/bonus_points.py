from ..extensions import db

class BonusPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey(Competition.id))
    event_id = db.Column(db.Integer, db.ForeignKey(Event.id))
    name = db.Column(db.String)
    house = db.Column(db.String)
    points = db.Column(db.Integer)
    archived = db.Column(db.Boolean)
    archived_time = db.Column(db.DateTime)
