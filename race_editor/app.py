import time
import flask
import yaml
import flask_sqlalchemy
import sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    competition_type = db.Column(db.String)
    distance = db.Column(db.String)
    gender = db.Column(db.String)
    ystart = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey(Competition.id))
    student_id = db.Column(db.String)  # , db.ForeignKey('competitions.id'))
    #student = db.relationship("Student", backref=backref("competitions", uselist=False))
    score = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return flask.render_template("index.html")


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


@app.route("/save_competition/<competition_id>", methods=["POST"])
def save_competition(competition_id):
    # urllib.parse.urlparse("http://127.0.0.1:5000/edit_competition/500m_8_boys.yaml").path.split("/")[-1]
    results = flask.request.get_json()

    for result in results:
        print(result)

    return "200 OK", 200


@app.route("/add_result/<competition_id>", methods=["POST"])
def add_result(competition_id):
    data = flask.request.get_json()
    result = Result(
        competition_id=competition_id,
        student_id=data["student_id"]
    )
    db.session.add(result)
    db.session.commit()
    return str(result.id), 200


@app.route("/delete_result/<result_id>", methods=["DELETE"])
def delete_result(result_id):
    # return "200 OK", 200
    Result.query.filter_by(id=result_id).delete()
    return "200 OK", 200
