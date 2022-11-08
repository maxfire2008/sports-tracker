import time
import flask
import yaml
import flask_sqlalchemy
import flask_wtf
import wtforms
import wtforms.validators

db = flask_sqlalchemy.SQLAlchemy()

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@127.0.0.1:5431"
db.init_app(app)


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scoring_type = db.Column(db.String)
    gender = db.Column(db.String)
    ystart = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey(Competition.id))
    # competition = db.relationship("Competition", backref=db.backref("competition", uselist=False))
    student_id = db.Column(db.String)
    score = db.Column(db.String)
    __table_args__ = (
        db.UniqueConstraint(
            competition_id,
            student_id,
            name="student_unique_in_competition"
        ),
    )


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return flask.render_template("index.html")


class CreateCompetitionForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(
        'name',
        validators=[
            wtforms.validators.DataRequired()
        ]
    )
    scoring_type = wtforms.StringField(
        'scoring_type',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.AnyOf(
                [
                    "shortest_time",
                    "highest_score"
                ]
            )
        ]
    )
    gender = wtforms.StringField(
        'gender',
        validators=[
            wtforms.validators.AnyOf(
                [
                    "male",
                    "female",
                    "any"
                ]
            )
        ]
    )
    ystart = wtforms.IntegerField(
        'ystart'
    )
    start_time = wtforms.DateTimeField(
        'start_time'
    )


@app.route("/create_competition/", methods=["GET"]):
def create_competition():
    return flask.render_template(
        "create_competition.html",

    )


@app.route("/api/create_competition/", methods=["POST"])
def api_create_competition():
    return "501 Not Implemented", 501

@app.route("/edit_competition/<competition_id>")
def edit_competition(competition_id):
    results = Result.query.filter_by(competition_id=competition_id).all()
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
        DBResult = Result.query.filter_by(
            id=result["id"],
            competition_id=competition_id,
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
        student_id=data["student_id"]
    )
    db.session.add(result)
    db.session.commit()
    return str(result.id), 200


@app.route("/api/delete_result/<result_id>", methods=["DELETE"])
def api_delete_result(result_id):
    # return "200 OK", 200
    Result.query.filter_by(id=result_id).delete()
    db.session.commit()
    return "200 OK", 200
