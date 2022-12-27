import flask
from .. import extensions
from .. import models
from ..update_points_awarded import update_points_awarded

api = flask.Blueprint('api', __name__, template_folder='../templates')


@api.route("/api/save_results/<competition_id>", methods=["PUT"])
def api_save_competition(competition_id):
    # urllib.parse.urlparse("http://127.0.0.1:5000/edit_results/500m_8_boys.yaml").path.split("/")[-1]
    save_data = flask.request.get_json()

    results = save_data["students"]

    bonus_points = save_data["bonus_points"]
    for result in results:
        print(result)
        already_exists_query = models.Result.query.filter(
            models.Result.student_id == result["student_id"],
            models.Result.competition_id == competition_id,
            models.Result.archived == False,  # noqa: E712
        )
        already_exists = bool(already_exists_query.first())
        print(already_exists)
        if result.get("id", "null") != "null":
            DBResult = models.Result.query.filter(
                models.Result.id == result["id"],
                models.Result.competition_id == competition_id,
            ).first()
            if result.get("student_id") is not None:
                DBResult.student_id = result["student_id"]
            if result.get("score") is not None:
                DBResult.score = result["score"]
        elif already_exists:
            extensions.db.session.rollback()
            return "409 Conflict", 409
        else:
            NewDBEntry = models.Result(
                competition_id=competition_id,
                student_id=result["student_id"],
                archived=False
            )
            if result.get("score") is not None:
                NewDBEntry.score = result["score"]
            extensions.db.session.add(NewDBEntry)

    for bonus_point in bonus_points:
        BonusPointResult = models.BonusPoints.query.filter(
            models.BonusPoints.id == bonus_point["id"],
            models.BonusPoints.competition_id == competition_id,
        ).first()
        if bonus_point["points"] is not None:
            BonusPointResult.points = bonus_point["points"]

    extensions.db.session.commit()
    update_points_awarded(competition_id)

    return "200 OK", 200


@api.route("/api/archive_result/<result_id>", methods=["PATCH"])
def api_archive_result(result_id):
    # return "200 OK", 200
    result = models.Result.query.filter(
        models.Result.id == result_id).first()
    result.archived = True
    extensions.db.session.commit()
    update_points_awarded(result.competition_id)
    return "200 OK", 200


@api.route("/api/restore_result/<result_id>", methods=["PATCH"])
def api_restore_result(result_id):
    # return "200 OK", 200
    result = models.Result.query.filter(
        models.Result.id == result_id).first()
    result.archived = False
    extensions.db.session.commit()
    update_points_awarded(result.competition_id)
    return "200 OK", 200


@api.route("/api/delete_result/<result_id>", methods=["DELETE"])
def api_delete_result(result_id):
    # return "200 OK", 200
    query = models.Result.query.filter(
        models.Result.id == result_id)
    competition_id = query.first().competition_id
    query.delete()
    extensions.db.session.commit()
    update_points_awarded(competition_id)
    return "200 OK", 200
