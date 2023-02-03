from ..extensions import db
from .competition import Competition
from .student import Student


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(
        db.Integer,
        db.ForeignKey(
            Competition.id
        )
    )
    # competition = db.relationship(
    #   "Competition",
    #   backref=db.backref(
    #       "competition",
    #       uselist=False
    #   )
    # )
    student_id = db.Column(
        db.String,
        db.ForeignKey(
            Student.id
        )
    )
    score = db.Column(db.String)
    points_awarded = db.Column(db.Integer)
    place = db.Column(db.Integer)
    archived = db.Column(db.Boolean, nullable=False)
    archived_time = db.Column(db.DateTime)
