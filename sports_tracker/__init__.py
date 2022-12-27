import flask
from . import CONFIG
from . import extensions
from . import routes


def create_app():
    app = flask.Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "postgresql://postgres:postgres@127.0.0.1:5431"
    app.config["SECRET_KEY"] = CONFIG.SECRET_KEY
    app.url_map.strict_slashes = False

    extensions.db.init_app(app)
    extensions.migrate.init_app(app, extensions.db)

    app.register_blueprint(routes.api)
    app.register_blueprint(routes.forms)
    app.register_blueprint(routes.pages)

    return app
