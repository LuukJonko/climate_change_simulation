class Time(object):
    def __init__(self):
        self._time = 0  

        self.time_interval = 'days'  # Either days, weeks, months or years

        self._date = []
        self._total = 0

        self._observers = []

    def proceed(self):
        self._time += 1
        self.correct_formulation()

    def correct_formulation(self):
        options = {'years': 365, 'months': 30, 'weeks': 7, 'days': 1}
        date_list = [None] * len(options)
        remaining = self._time * options[self.time_interval]
        for index, option in enumerate(options): 
            date_list[index], remaining = self.divRem(remaining, options[option])
        # date_list = date_list[list(options.keys()).index(self.time_interval):] = None
        self._date = date_list
        self._total = self.divRem(self._total, options['years'])[1]

    @staticmethod
    def divRem(number, divider):
        return [int((number - (number % divider)) / divider), number % divider]

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
