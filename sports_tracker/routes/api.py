import flask
from .. import extensions
from .. import models

api = flask.Blueprint('api', __name__, template_folder='../templates')


@api.route("/api/save_competition/<competition_id>", methods=["PUT"])
def api_save_competition(competition_id):
    # urllib.parse.urlparse("http://127.0.0.1:5000/edit_competition/500m_8_boys.yaml").path.split("/")[-1]
    save_data = flask.request.get_json()

    results = save_data["students"]

    bonus_points = save_data["bonus_points"]

    for result in results:
        DBResult = models.result.Result.query.filter(
            models.result.Result.id == result["id"],
            models.result.Result.competition_id == competition_id,
        ).first()
        if result["student_id"] is not None:
            DBResult.student_id = result["student_id"]
        if result["score"] is not None:
            DBResult.score = result["score"]

    for bonus_point in bonus_points:
        print(bonus_point)
        BonusPointResult = models.bonus_points.BonusPoints.query.filter(
            models.bonus_points.BonusPoints.id == bonus_point["id"],
            models.bonus_points.BonusPoints.competition_id == competition_id,
        ).first()
        if bonus_point["points"] is not None:
            BonusPointResult.points = bonus_point["points"]
        print(bonus_point)

    extensions.db.session.commit()

    return "200 OK", 200


@api.route("/api/add_result/<competition_id>", methods=["POST"])
def api_add_result(competition_id):
    data = flask.request.get_json()
    result = models.result.Result(
        competition_id=competition_id,
        student_id=data["student_id"],
        archived=False
    )
    extensions.db.session.add(result)
    extensions.db.session.commit()
    return str(result.id), 200


@api.route("/api/archive_result/<result_id>", methods=["PATCH"])
def api_archive_result(result_id):
    # return "200 OK", 200
    result = models.result.Result.query.filter(
        models.result.Result.id == result_id).first()
    result.archived = True
    extensions.db.session.commit()
    return "200 OK", 200


@api.route("/api/restore_result/<result_id>", methods=["PATCH"])
def api_restore_result(result_id):
    # return "200 OK", 200
    result = models.result.Result.query.filter(
        models.result.Result.id == result_id).first()
    result.archived = False
    extensions.db.session.commit()
    return "200 OK", 200


@api.route("/api/delete_result/<result_id>", methods=["DELETE"])
def api_delete_result(result_id):
    # return "200 OK", 200
    models.result.Result.query.filter(
        models.result.Result.id == result_id).delete()
    extensions.db.session.commit()
    return "200 OK", 200
