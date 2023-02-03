from ..extensions import db
from .competition import Competition
from .house import House
from .event import Event


class HousePoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(
        db.Integer,
        db.ForeignKey(
            Competition.id
        )
    )
    # event_id = db.Column(db.Integer, db.ForeignKey(Event.id))
    name = db.Column(db.String)
    house = db.Column(
        db.Integer,
        db.ForeignKey(
            House.id
        )
    )
    points = db.Column(db.Integer)
    archived = db.Column(db.Boolean, nullable=False)
    archived_time = db.Column(db.DateTime)
