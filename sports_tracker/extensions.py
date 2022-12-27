import flask_sqlalchemy
import flask_migrate

db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
