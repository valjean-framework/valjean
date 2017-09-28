from time import sleep
from random import expovariate


class Task:
    def __init__(self, name):
        self.name = name

    def do(self):
        self.lapse = random.expovariate(1.)
        print('Task {self.name} sleeping {self.lapse} seconds...'
              .format(self=self))
        sleep(self.lapse)
        print('Task {self.name} waking up!'.format(self=self))
