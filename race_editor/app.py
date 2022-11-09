import datetime
import time
import flask
import yaml
import flask_sqlalchemy
import CONFIG

db = flask_sqlalchemy.SQLAlchemy()

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@127.0.0.1:5431"
app.config["SECRET_KEY"] = CONFIG.SECRET_KEY
app.url_map.strict_slashes = False
db.init_app(app)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


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


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer)  # , db.ForeignKey(Competition.id))
    # competition = db.relationship("Competition", backref=db.backref("competition", uselist=False))
    student_id = db.Column(db.String)
    score = db.Column(db.String)
    archived = db.Column(db.Boolean)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return flask.render_template(
        "index.html",
        cookies=flask.request.cookies
    )


@app.route("/create_event")
def create_event():
    return flask.render_template(
        "create_event.html"
    )


@app.route("/form/create_event", methods=["POST"])
def form_create_event():
    name = flask.request.form.get("name", None)
    if not name:
        flask.flash("Name is a required field")
        return flask.redirect(flask.request.referrer)
    event = Event(
        name=name
    )
    db.session.add(event)
    db.session.commit()
    return flask.redirect(
        flask.url_for(
            "view_event",
            event_id=event.id
        )
    )


@app.route("/event/<event_id>/")
def view_event(event_id):
    event = Event.query.filter(Event.id == event_id).first()
    competitions = Competition.query.filter(Competition.event_id == event_id).all()
    if event:
        return flask.render_template(
            "view_event.html",
            event=event,
            competitions=competitions,
        )
    return "404 Event Not Found", 404


@app.route("/event/<event_id>/create_competition")
def create_competition(event_id):
    return flask.render_template(
        "create_competition.html",
        event_id=event_id
    )


@app.route("/form/create_competition", methods=["POST"])
def form_create_competition():
    name = flask.request.form.get("name", None)
    if not name:
        flask.flash("Name is a required field")
        return flask.redirect(flask.request.referrer)
    scored = flask.request.form.get("scored", False)
    if str(scored).lower() in ["true", "checked", "on"]:
        scored = True
    else:
        scored = False
    sorting_type = flask.request.form.get("sorting_type", None)
    if sorting_type not in ["short_time"]:
        flask.flash("Scoring type is invalid")
        return flask.redirect(flask.request.referrer)
    gender = flask.request.form.get("gender", "all")
    if gender not in ["male", "female"]:
        gender = "all"
    try:
        ystart = int(flask.request.form.get("ystart", "-1"))
    except ValueError:
        ystart = None
    try:
        start_time = datetime.datetime.fromisoformat(
            flask.request.form.get("start_time", None)
        )
    except ValueError:
        start_time = None
    try:
        event_id = int(flask.request.form.get("event_id", None))
    except (TypeError, ValueError):
        flask.flash("What have you done")
        return flask.redirect(flask.request.referrer)

    competition = Competition(
        name=name,
        scored=scored,
        sorting_type=sorting_type,
        gender=gender,
        ystart=ystart,
        start_time=start_time,
        event_id=event_id,
    )

    db.session.add(competition)
    db.session.commit()

    return "200 OK", 501


@app.route("/competition/<competition_id>/edit")
def competition_edit(competition_id):
    show_archived = flask.request.cookies.get('show_archived', 0)
    competition = Competition.query.filter(Competition.id == competition_id).first()
    results = Result.query.filter(
        Result.competition_id == competition_id,
        show_archived == "1" or Result.archived != True
    ).all()
    return flask.render_template(
        "edit_competition.html",
        competition_id=competition_id,
        competition=competition,
        student_db=yaml.safe_load(
            open("../reference/student_db.yaml")
        ),
        results=results
    )


@app.route("/api/save_competition/<competition_id>", methods=["PUT"])
def api_save_competition(competition_id):
    # urllib.parse.urlparse("http://127.0.0.1:5000/edit_competition/500m_8_boys.yaml").path.split("/")[-1]
    results = flask.request.get_json()

    for result in results:
        print(result)
        DBResult = Result.query.filter(
            Result.id == result["id"],
            Result.competition_id == competition_id,
        ).first()
        if result["student_id"] != None:
            DBResult.student_id = result["student_id"]
        if result["score"] != None:
            DBResult.score = result["score"]
    db.session.commit()

    return "200 OK", 200


@app.route("/api/add_result/<competition_id>", methods=["POST"])
def api_add_result(competition_id):
    data = flask.request.get_json()
    result = Result(
        competition_id=competition_id,
        student_id=data["student_id"],
        archived=False
    )
    db.session.add(result)
    db.session.commit()
    return str(result.id), 200


@app.route("/api/archive_result/<result_id>", methods=["PATCH"])
def api_archive_result(result_id):
    # return "200 OK", 200
    result = Result.query.filter(Result.id == result_id).first()
    result.archived = True
    db.session.commit()
    return "200 OK", 200


@app.route("/api/delete_result/<result_id>", methods=["DELETE"])
def api_delete_result(result_id):
    # return "200 OK", 200
    Result.query.filter(id == result_id).delete()
    db.session.commit()
    return "200 OK", 200
