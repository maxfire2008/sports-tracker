import flask
from .. import extensions
from .. import models

api = flask.Blueprint('api', __name__, template_folder='../templates')


def api_save_competition(competition_id):
    # urllib.parse.urlparse("http://127.0.0.1:5000/edit_competition/500m_8_boys.yaml").path.split("/")[-1]
    save_data = flask.request.get_json()

    results = save_data["students"]

    bonus_points = save_data["bonus_points"]

    for result in results:
        if result.get("id", "null") != "null":
            DBResult = Result.query.filter(
                Result.id == result["id"],
                Result.competition_id == competition_id,
            ).first()
            if result.get("student_id") != None:
                DBResult.student_id = result["student_id"]
            if result.get("score") != None:
                DBResult.score = result["score"]
        else:
            NewDBEntry = Result(
                competition_id=competition_id,
                student_id=result["student_id"],
                archived=False
            )
            if result.get("score") != None:
                NewDBEntry.score = result["score"]
            db.session.add(NewDBEntry)
            db.session.commit()
    for bonus_point in bonus_points:
        print(bonus_point)
        BonusPointResult = BonusPoints.query.filter(
            BonusPoints.id == bonus_point["id"],
            BonusPoints.competition_id == competition_id,
        ).first()
        if bonus_point["points"] != None:
            BonusPointResult.points = bonus_point["points"]
        print(bonus_point)

    db.session.commit()

    return "200 OK", 200


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
