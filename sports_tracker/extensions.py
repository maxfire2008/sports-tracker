import flask_sqlalchemy
import flask_migrate

db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()


def compare_gender(gender_1, gender_2, strict=False):
    # if gender_1 is
    if gender_1 == gender_2:
        return True
    elif gender_1 in ["male", "female"] and gender_2 in ["male", "female"]:
        return False
    if strict:
        return False
    return True
