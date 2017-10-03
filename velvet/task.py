# -*- coding: utf-8 -*-
'''Task specification.

This module collects a few useful Task classes that can be used with the
:mod:`~.scheduler` module.

Any class with a :meth:`do()` method qualifies as a Task.
'''

import time
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class DelayTask:
    '''Task that waits for the specified number of seconds.

    This task is useful to test scheduling algorithms under different load
    conditions.

    :param name str: The name of the task
    :param delay float: The amount of time (in seconds) that this task will
                        wait when executed.
    '''

    def __init__(self, name, delay=1.):
        self.name = name
        self.delay = float(delay)

    def __repr__(self):
        return '"DelayTask {}"'.format(self.name)

    def do(self):
        '''Perform the task (i.e. sleep; I wish my life was like that).'''

        logger.info('DelayTask %s sleeping %f seconds...',
                    self, self.delay)
        time.sleep(self.delay)
        logger.info('DelayTask %s waking up!', self)
