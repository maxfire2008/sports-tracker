import time
import flask
import yaml
import flask_sqlalchemy
import CONFIG

db = flask_sqlalchemy.SQLAlchemy()

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@127.0.0.1:5431"
app.config["SECRET_KEY"] = CONFIG.SECRET_KEY
db.init_app(app)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scored = db.Column(db.Boolean)
    sorting_type = db.Column(db.String)#select of short_time long_time etc
    gender = db.Column(db.String)# male female all
    ystart = db.Column(db.Integer)# year
    start_time = db.Column(db.DateTime)# date and time
    event_id = db.Column(db.Integer, db.ForeignKey(Event.id))# auto populated just make a input for now
    archived = db.Column(db.Boolean) # not in form


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


@app.route("/create_competition/")
def create_competition():
    return flask.render_template(
        "create_competition.html"
    )


@app.route("/form/create_competition/", methods=["POST"])
def form_create_competition():
    name = flask.request.form.get("name", None)
    if not name:
        flask.flash("Name is a required field")
        return "400 Bad Request", 400
    scored = flask.request.form.get("scored", False)
    if scored.lower() in ["true", "checked", "on"]:
        scored = True
    else:
        scored = False
    sorting_type = flask.request.form.get("sorting_type", None)
    if sorting_type not in ["lowest_time"]:
        flask.flash("Scoring Type is invalid")
    gender = None
    ystart = None
    start_time = None
    event_id = None
    archived = None
    return "501 Not Implemented", 501


@app.route("/edit_competition/<competition_id>")
def edit_competition(competition_id):
    show_archived = flask.request.cookies.get('show_archived', 0)
    results = Result.query.filter(
        Result.competition_id == competition_id,
        show_archived == "1" or Result.archived != True
    ).all()
    return flask.render_template(
        "edit_competition.html",
        competition_id=competition_id,
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
    Result.query.filter_by(id=result_id).delete()
    db.session.commit()
    return "200 OK", 200
