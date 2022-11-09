import pytimeparse.timeparse

class ShortTime:
    def sorter(score, backup=0):
        try:
            return float(pytimeparse.timeparse.timeparse(score))
        except:
            return backup

sorters = {
    "short_time": ShortTime
}
