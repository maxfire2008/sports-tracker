import flask
import yaml
from ..update_points_awarded import update_points_awarded
from .. import models
from .. import sorters

pages = flask.Blueprint('pages', __name__, template_folder='../templates')


@pages.route("/")
def index():
    events = models.event.Event.query.all()
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
    event = models.event.Event.query.filter(
        models.event.Event.id == event_id).first()
    competitions = models.competition.Competition.query.filter(
        models.competition.Competition.event_id == event_id).all()
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
    competition = models.competition.Competition.query.filter(
        models.competition.Competition.id == competition_id).first()
    if not competition:
        return "404 Not Found", 404

    update_points_awarded(competition_id)

    results = models.result.Result.query.filter(
        models.result.Result.competition_id == competition_id,
        show_archived == "1" or models.result.Result.archived is not True
    ).all()

    bonus_points = models.bonus_points.BonusPoints.query.filter(
        models.bonus_points.BonusPoints.competition_id == competition_id,
        show_archived == "1" or models.result.Result.archived is not True
    ).all()

    score_parser = sorters.sorters[competition.sorting_type](
        competition.sorting_options)

    return flask.render_template(
        "edit_results.html",
        competition_id=competition_id,
        competition=competition,
        student_db=yaml.safe_load(
            open("reference/student_db.yaml")
        ),
        results=score_parser.sorted(results),
        bonus_points=sorted(
            bonus_points,
            key=lambda x: x.house
        )
    )
