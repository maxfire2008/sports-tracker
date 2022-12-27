import pytimeparse.timeparse
import json


class ShortTime:
    def __init__(self, options={}):
        if options:
            self._options = json.loads(options)
    def pure_key(self, result):
        try:
            return float(pytimeparse.timeparse.timeparse(result.score))
        except:
            pass
        try:
            return int(result.score)
        except Exception as e:
            print(e)
        return -1

    def key(self, result):
        try:
            return [
                result.archived,
                self.pure_key(result)
            ]
        except Exception as e:
            print(e)
        return [
            result.archived,
            result.score,
            result.student_id
        ]

    def sorted(self, results):
        return sorted(results, key=self.key)

    def get_points(self, place, score):
        if place == -1:
            return 0
        return max(20-place, 0)

    def valid(self, score):
        try:
            float(pytimeparse.timeparse.timeparse(score))
            return True
        except Exception:
            pass
        try:
            int(score)
            return True
        except Exception as e:
            print(e)
        return False


def placed(results_sorted, key, sorting_type):
    current_place = 0
    next_place = 0
    last_score = None

    placed_results = []

    for result in results_sorted:
        result_key = key(result)
        # print(repr(result.score))
        print(sorting_type.valid(result.score))
        if result.archived == False and sorting_type.valid(result.score):
            if result_key != last_score:
                current_place = next_place

            placed_results.append([
                current_place,
                result
            ])
            last_score = result_key

            next_place += 1
        else:
            # print("invalid for sorting")
            # print(result)
            placed_results.append([
                -1,
                result
            ])
        print(placed_results[-1][0], placed_results[-1][1].student_id)
    return placed_results


sorters = {
    "short_time": ShortTime
}
