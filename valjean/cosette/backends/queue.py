# -*- coding: utf-8 -*-
'''This module contains an implementation of a scheduling backend that
leverages Python "threads" (:mod:`~threading` module) and producer-consumer
queues (:mod:`~queue` module).
'''

import threading
from collections.abc import MutableMapping
import logging

from ..task import TaskStatus


logger = logging.getLogger(__name__)


class QueueScheduling:
    '''The default scheduling backend.

    Uses :mod:`threading` and :mod:`queue` to handle concurrent execution of
    tasks.
    '''

    def __init__(self, n_workers=10, sleep_interval=1.0):

        '''Initialize the queue backend.

        :param int n_workers: The number of worker threads to use.
        :param float sleep_interval: The delay (in seconds) to wait before
                                     retrying to execute further jobs if the
                                     worker queue is starving. This typically
                                     happens when there are more workers
                                     available than tasks pending because of
                                     dependencies between the tasks.
        '''

        self.n_workers = n_workers
        self.sleep_interval = sleep_interval

    def execute_tasks(self, tasks, graph, env):
        '''Execute the tasks.

        :param iterable tasks: Iterable over tasks to be executed, possibly
                               sorted according to some order.
        :param DepGraph graph: Dependency graph for the tasks.
        :param env: An initial environment for the scheduled tasks.
        :type env: Env
        '''

        import time
        import queue

        threads = []
        q = queue.Queue(self.n_workers)

        # spawn workers
        for i in range(self.n_workers):
            t = QueueScheduling.WorkerThread(q, env)
            t.start()
            threads.append(t)

        # process tasks
        tasks_left = tasks
        while len(tasks_left) > 0:
            tasks_still_left = []
            n_tasks_left = len(tasks_left)
            for task in tasks_left:
                logger.debug('status of task %s: %s',
                             task, env.get_status(task))

                # skip failed/notrun/completed tasks
                if not env.is_waiting(task):
                    continue

                deps = list(graph.dependencies(task))
                def check_deps(env_):
                    failed_deps = any(env_.is_failed(t) or env_.is_skipped(t)
                                      for t in deps)
                    can_run = all(env_.is_done(t) for t in deps)
                    return failed_deps, can_run
                failed_deps, can_run = env.atomically(check_deps)
                logger.debug('task %s has failed deps: %s', task, failed_deps)
                logger.debug('task %s can run: %s', task, can_run)
                if failed_deps:
                    env.set_skipped(task)
                    n_tasks_left -= 1
                    logger.info('task %s cannot be run, %d left',
                                task, n_tasks_left)
                elif can_run:
                    q.put(task)
                    n_tasks_left -= 1
                    logger.debug('task %s scheduled, %d left',
                                 task, n_tasks_left)
                else:
                    logger.debug('reappending task %s', task)
                    tasks_still_left.append(task)
            tasks_left = tasks_still_left

            if len(tasks_left) == 0:
                # we're done!
                break

            if n_tasks_left == len(tasks_left):
                logger.debug('worker queue is starving because '
                             'of dependencies, sleeping for '
                             '%f seconds...', self.sleep_interval)
                time.sleep(self.sleep_interval)

        # block until all tasks are done
        q.join()

        # stop workers and go home
        for i in range(self.n_workers):
            q.put(None)
        for t in threads:
            t.join()

    class WorkerThread(threading.Thread):
        '''Workhorse class for :class:`QueueScheduling`. This class consumes
        (i.e. executes) tasks passed to it through the queue.
        '''

        def __init__(self, queue, env):
            '''Initialize the thread.

            :param queue: The producer-consumer task queue.
            :param env: The execution environment for the tasks.
            '''
            super().__init__()
            self.queue = queue
            self.env = env

        def run(self):
            '''Main method: run this thread.'''

            logger.debug('worker %s starting', self.name)
            while True:
                task = self.queue.get()
                logger.debug('worker %s got task %s', self.name, task)
                if task is None:
                    logger.debug('worker %s exiting', self.name)
                    break

                # we start to work on the task
                self.env.set_pending(task)

                try:
                    env_update, status = task.do(self.env)
                except Exception as ex:
                    logger.exception('task %s on worker %s failed: %s',
                                     task, self.name, ex)
                    logger.debug('setting FAILED status in the environment...')
                    self.env.set_failed(task)
                else:
                    logger.debug('task %s on worker %s completed with status %s',
                                 task, self.name, status)
                    logger.debug('proposed environment update: %s', env_update)
                    self.env.set_status(task, status)
                    self.env.apply(env_update)

                logger.debug('worker %s wants more!', self.name)
                self.queue.task_done()
