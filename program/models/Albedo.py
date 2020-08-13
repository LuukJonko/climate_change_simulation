class Albedo(object):
    def __init__(self):
        self._albedo = 0
        self._observers = []

    @property
    def albedo(self):
        return self._albedo

    @albedo.setter
    def albedo(self, value):
        self._albedo = value
        for callback in self._observers:
            print('change')
            callback(self._albedo)

    def bind_to(self, callback):
        self._observers.append(callback)
