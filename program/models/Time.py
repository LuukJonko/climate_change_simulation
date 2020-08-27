class Time:
    def __init__(self):
        self._time = 0
        self._observers = []

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        for callback in self._observers:
            callback(self._time)

    def bind_to(self, callback):
        self._observers.append(callback)
