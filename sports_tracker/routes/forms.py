import flask
import datetime
from .. import extensions
from .. import models
from .. import sorters
from .. import participation_points

forms = flask.Blueprint('forms', __name__, template_folder='../templates')


@forms.route("/form/create_event", methods=["POST"])
def form_create_event():
    name = flask.request.form.get("name", None)
    if not name:
        flask.flash("Name is a required field")
        return flask.redirect(flask.request.referrer)
    event = models.Event(
        name=name,
        archived=False,
    )
    extensions.db.session.add(event)
    extensions.db.session.commit()
    return flask.redirect(
        flask.url_for(
            "pages.index"
        )
    )


@forms.route("/form/create_competition", methods=["POST"])
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
        ystart = int(flask.request.form.get("ystart", None))
    except ValueError:
        ystart = None

    if ystart == -1:
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
        flask.flash("What have you done!?")
        return flask.redirect(flask.request.referrer)

    competition = models.Competition(
        name=name,
        scored=scored,
        sorting_type=sorting_type,
        gender=gender,
        ystart=ystart,
        start_time=start_time,
        event_id=event_id,
        archived=False,
    )

    extensions.db.session.add(competition)
    extensions.db.session.commit()

    if flask.request.form.get("participation_points", "off") == "on":
        participation_points.add_participation_points(competition)

    # participation_points = flask.request.form.get("scored", False)
    # if str(participation_points).lower() in ["true", "checked", "on"]:
    #     for house in

    return flask.redirect(
        flask.url_for(
            "pages.view_event",
            event_id=event_id,
        )
    )
