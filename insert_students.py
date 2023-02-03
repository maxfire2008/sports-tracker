from sports_tracker import create_app
from sports_tracker import models
from sports_tracker import extensions
import yaml
import time
import colour as color
import sys

student_db = yaml.safe_load(
    open("reference/student_db.yaml")
)

import_id = str(time.time())


def insert_dummy_data(dry_run=True):
    app = create_app()
    with app.app_context():
        for house in student_db["houses"]:
            # print(house)
            if models.House.query.filter(
                models.House.name == house
            ).first() is None:
                extensions.db.session.add(
                    models.House(
                        name=house,
                        color_code=color.Color(house).hex,
                        color_name=house,
                        archived=False,
                    )
                )
        for student_id, student_data in student_db["students"].items():
            # print(student_id, student_data)
            if models.Student.query.filter(
                models.Student.id == student_id
            ).first() is None:
                extensions.db.session.add(
                    models.Student(
                        id=student_id,
                        name=student_data['name'],
                        preferred_name=student_data.get(
                            "preferred_name", None),
                        ystart=student_data['ystart'],
                        gender=student_data['gender'],
                        house=models.House.query.filter(
                            models.House.name == student_data['house']
                        ).first().id,
                        import_batch_id=import_id,
                        archived = False,
                    )
                )
        if not dry_run:
            print("Committing")
            extensions.db.session.commit()
        extensions.db.session.flush()


if __name__ == "__main__":
    insert_dummy_data(
        sys.argv[1] != "--dry-run=0"
    )
