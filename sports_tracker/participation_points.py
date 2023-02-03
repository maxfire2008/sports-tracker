from . import extensions
from . import models


def add_participation_points(competition):
    houses = models.House.query.filter(
        models.House.archived == False,  # noqa: E712
    ).all()

    for house in houses:
        print(house.name)
        participation_point = models.HousePoints(
            competition_id=competition.id,
            # event_id=competition.event_id,
            name="Participation Points for "+house.name,
            house=house.id,
            points=0,
            archived=False,
        )
        extensions.db.session.add(participation_point)
    extensions.db.session.commit()
