from ..extensions import db


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    color_code = db.Column(db.String)
    color_name = db.Column(db.String)
    archived = db.Column(db.Boolean, nullable=False)
    archived_time = db.Column(db.DateTime)
