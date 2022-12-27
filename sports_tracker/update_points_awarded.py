from . import extensions
from . import models
from . import sorters


def update_points_awarded(competition_id):
    competition = models.competition.Competition.query.filter(
        models.competition.Competition.id == competition_id).first()

    results = models.result.Result.query.filter(
        models.result.Result.competition_id == competition_id
    ).all()

    score_parser = sorters.sorters[competition.sorting_type](
        competition.sorting_options)

    results_sorted = score_parser.sorted(results)

    results_placed = sorters.placed(
        results_sorted,
        score_parser.pure_key,
        sorting_type=score_parser,
    )

    for result in results_placed:
        # print(result, result[1].student_id)
        result[1].place = result[0]
        result[1].points_awarded = score_parser.get_points(
            result[0], result[1].score)

    extensions.db.session.commit()
