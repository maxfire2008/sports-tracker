from ..extensions import db

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey(Competition.id))
    # competition = db.relationship("Competition", backref=db.backref("competition", uselist=False))
    student_id = db.Column(db.String)
    score = db.Column(db.String)
    points_awarded = db.Column(db.Integer)
    place = db.Column(db.Integer)
    archived = db.Column(db.Boolean)
    archived_time = db.Column(db.DateTime)
