import flask
import yaml
from ..update_points_awarded import update_points_awarded
from .. import models
from .. import sorters

pages = flask.Blueprint('pages', __name__, template_folder='../templates')


@pages.route("/")
def index():
    events = models.Event.query.all()
    return flask.render_template(
        "index.html",
        cookies=flask.request.cookies,
        events=events,
    )


@pages.route("/create_event")
def create_event():
    return flask.render_template(
        "create_event.html"
    )


@pages.route("/event/<event_id>/")
def view_event(event_id):
    event = models.Event.query.filter(
        models.Event.id == event_id).first()
    competitions = models.Competition.query.filter(
        models.Competition.event_id == event_id).all()
    if event:
        return flask.render_template(
            "view_event.html",
            event=event,
            competitions=competitions,
        )
    return "404 Event Not Found", 404


@pages.route("/event/<event_id>/create_competition")
def create_competition(event_id):
    return flask.render_template(
        "create_competition.html",
        event_id=event_id
    )


@pages.route("/competition/<competition_id>/edit")
def competition_edit(competition_id):
    show_archived = flask.request.cookies.get('show_archived', 0)
    competition = models.Competition.query.filter(
        models.Competition.id == competition_id).first()
    if not competition:
        return "404 Not Found", 404

    update_points_awarded(competition_id)

    results = models.Result.query.filter(
        models.Result.competition_id == competition_id,
        show_archived == "1" or models.Result.archived is not True
    ).all()

    house_points = models.HousePoints.query.filter(
        models.HousePoints.competition_id == competition_id,
        show_archived == "1" or models.Result.archived is not True
    ).all()

    score_parser = sorters.sorters[competition.sorting_type](
        competition.sorting_options)

    student_db = {
        "students": {},
    }

    for student in models.Student.query.all():
        student_db["students"][student.id] = {
            "id": student.id,
            "name": student.name,
            "preferred_name": student.preferred_name,
            "ystart": student.ystart,
            "gender": student.gender,
            "house": student.house,
            "import_batch_id": student.import_batch_id,
            "archived": student.archived,
            "archived_time": student.archived_time,
        }

    return flask.render_template(
        "edit_results.html",
        competition_id=competition_id,
        competition=competition,
        student_db=student_db,
        results=score_parser.sorted(results),
        house_points=sorted(
            house_points,
            key=lambda x: x.name
        )
    )
