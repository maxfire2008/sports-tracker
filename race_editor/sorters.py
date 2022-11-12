import pytimeparse.timeparse


class ShortTime:
    def pure_key(result):
        try:
            return float(pytimeparse.timeparse.timeparse(result.score))
        except:
            pass
        try:
            return int(result.score)
        except Exception as e:
            print(e)

    def key(result):
        try:
            return [
                result.archived,
                ShortTime.pure_key(result)
            ]
        except Exception as e:
            print(e)
        return [
            result.archived,
            result.score,
            result.student_id
        ]

    def sorted(results):
        return sorted(results, key=ShortTime.key)


def placed(results_sorted, key):
    current_place = 1
    next_place = 1
    last_score = None

    placed_results = []

    for result in results_sorted:
        result_key = key(result)
        if result_key != last_score:
            current_place = next_place

        placed_results.append([
            current_place,
            result
        ])
        last_score = result_key

        next_place += 1
    return placed_results


sorters = {
    "short_time": ShortTime
}
