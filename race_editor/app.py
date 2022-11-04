import flask

app = flask.Flask(__name__)

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/edit_race/<race_id>")
def edit_race(race_id):
    return flask.render_template("edit_race.html")
