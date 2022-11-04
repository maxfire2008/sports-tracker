import flask
import yaml
import json

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/edit_race/<race_file>")
def edit_race(race_file):
    return flask.render_template(
        "edit_race.html",
        race_file=race_file,
        student_db=json.dumps(yaml.safe_load(open("../reference/student_db.yaml")))
    )
