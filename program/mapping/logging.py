import sys
from os.path import join
from datetime import datetime

def time():
	now = datetime.now()
	return now.strftime("%H:%M:%S")


class Logging:
    def __init__(self, BASEPATH):
        self.BASEPATH = BASEPATH

        self.log_file = open(join(self.BASEPATH, 'mapping/log.txt'), 'w')

    def log_event(self, event, orgin):
        self.log_file.write(f"[{ time() }] { orgin }: { event }")

    def log_error(self, error, orgin):
        self.log_file.write(f"[ERROR] [{ time() }] { orgin }: { error }")
