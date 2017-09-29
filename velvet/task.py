import time
import random
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class Task:
    def __init__(self, name, average=1.):
        self.name = name
        self.average = float(average)

    def __repr__(self):
        return '"Task {}"'.format(self.name)

    def do(self):
        lapse = random.expovariate(1./self.average)
        logger.info('Task %s sleeping %f seconds...',
                    self, lapse)
        time.sleep(lapse)
        logger.info('Task %s waking up!', self)
