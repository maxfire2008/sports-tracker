import datetime
import time
import flask
import yaml
import flask_sqlalchemy
import CONFIG
import sorters

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
    sorting_options = db.Column(db.JSON)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey(Competition.id))
    # competition = db.relationship("Competition", backref=db.backref("competition", uselist=False))
    student_id = db.Column(db.String)
    score = db.Column(db.String)
    points_awarded = db.Column(db.Integer)
    place = db.Column(db.Integer)
    archived = db.Column(db.Boolean)


class BonusPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey(Competition.id))
    event_id = db.Column(db.Integer, db.ForeignKey(Event.id))
    name = db.Column(db.String)
    house = db.Column(db.String)
    points = db.Column(db.Integer)
    archived = db.Column(db.Boolean)


with app.app_context():
    db.create_all()


def update_points_awarded(competition_id):
    competition = Competition.query.filter(
        Competition.id == competition_id).first()

    results = Result.query.filter(
        Result.competition_id == competition_id
    ).all()

    score_parser = sorters.sorters[competition.sorting_type](competition.sorting_options)

    results_sorted = score_parser.sorted(results)

    results_placed = sorters.placed(
        results_sorted,
        score_parser.pure_key,
        sorting_type=score_parser,
    )

    for result in results_placed:
        # print(result, result[1].student_id)
        result[1].place = result[0]
        result[1].points_awarded = score_parser.get_points(result[0], result[1].score)

    db.session.commit()


@app.route("/")
def index():
    events = Event.query.all()
    return flask.render_template(
        "index.html",
        cookies=flask.request.cookies,
        events=events,
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
    competitions = Competition.query.filter(
        Competition.event_id == event_id).all()
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
    if sorting_type not in sorters.sorters:
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
    competition = Competition.query.filter(
        Competition.id == competition_id).first()
    if not competition:
        return "404 Not Found", 404

    update_points_awarded(competition_id)

    results = Result.query.filter(
        Result.competition_id == competition_id,
        show_archived == "1" or Result.archived != True
    ).all()

    bonus_points = BonusPoints.query.filter(
        BonusPoints.competition_id == competition_id,
        show_archived == "1" or Result.archived != True
    ).all()

    score_parser = sorters.sorters[competition.sorting_type](competition.sorting_options)

    return flask.render_template(
        "edit_competition.html",
        competition_id=competition_id,
        competition=competition,
        student_db=yaml.safe_load(
            open("../reference/student_db.yaml")
        ),
        results=score_parser.sorted(results),
        bonus_points=sorted(
            bonus_points,
            key=lambda x: x.house
        )
    )


@app.route("/api/save_competition/<competition_id>", methods=["PUT"])
def api_save_competition(competition_id):
    # urllib.parse.urlparse("http://127.0.0.1:5000/edit_competition/500m_8_boys.yaml").path.split("/")[-1]
    save_data = flask.request.get_json()

    results = save_data["students"]

    bonus_points = save_data["bonus_points"]

    for result in results:
        if result.get("id", "null") != "null":
            DBResult = Result.query.filter(
                Result.id == result["id"],
                Result.competition_id == competition_id,
            ).first()
            if result.get("student_id") != None:
                DBResult.student_id = result["student_id"]
            if result.get("score") != None:
                DBResult.score = result["score"]
        else:
            NewDBEntry = Result(
                competition_id=competition_id,
                student_id=result["student_id"],
                archived=False
            )
            if result.get("score") != None:
                NewDBEntry.score = result["score"]
            db.session.add(NewDBEntry)
            db.session.commit()
    for bonus_point in bonus_points:
        print(bonus_point)
        BonusPointResult = BonusPoints.query.filter(
            BonusPoints.id == bonus_point["id"],
            BonusPoints.competition_id == competition_id,
        ).first()
        if bonus_point["points"] != None:
            BonusPointResult.points = bonus_point["points"]
        print(bonus_point)

    db.session.commit()

    return "200 OK", 200


@app.route("/api/archive_result/<result_id>", methods=["PATCH"])
def api_archive_result(result_id):
    # return "200 OK", 200
    result = Result.query.filter(Result.id == result_id).first()
    result.archived = True
    db.session.commit()
    return "200 OK", 200


@app.route("/api/restore_result/<result_id>", methods=["PATCH"])
def api_restore_result(result_id):
    # return "200 OK", 200
    result = Result.query.filter(Result.id == result_id).first()
    result.archived = False
    db.session.commit()
    return "200 OK", 200


@app.route("/api/delete_result/<result_id>", methods=["DELETE"])
def api_delete_result(result_id):
    # return "200 OK", 200
    Result.query.filter(Result.id == result_id).delete()
    db.session.commit()
    return "200 OK", 200
