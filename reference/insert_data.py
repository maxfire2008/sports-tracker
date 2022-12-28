from ..sports_tracker import create_app
from ..sports_tracker import models
from ..sports_tracker import extensions


def insert_dummy_data():
    app = create_app()
    with app.app_context():

        extensions.db.session.add()
        extensions.db.session.commit()


if __name__ == "__main__":
    insert_dummy_data()
