from ..extensions import db
from .house import House


class Student(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    preferred_name = db.Column(db.String)
    ystart = db.Column(db.Integer)
    gender = db.Column(db.String)  # gender must be one of male, female, nb
    house = db.Column(
        db.Integer,
        db.ForeignKey(
            House.id
        )
    )
    import_batch_id = db.Column(db.String)
    archived = db.Column(db.Boolean)
    archived_time = db.Column(db.DateTime)
