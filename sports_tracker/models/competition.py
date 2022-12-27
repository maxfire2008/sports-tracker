from ..extensions import db

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scored = db.Column(db.Boolean)
    sorting_type = db.Column(db.String)  # select of short_time long_time etc
    gender = db.Column(db.String)  # male female all
    ystart = db.Column(db.Integer)  # year
    start_time = db.Column(db.DateTime)  # date and time
    # auto populated just make a input for now
    event_id = db.Column(db.Integer, db.ForeignKey(Event.id))
    archived = db.Column(db.Boolean)  # not in form
    archived_time = db.Column(db.DateTime)
    sorting_options = db.Column(db.JSON)
