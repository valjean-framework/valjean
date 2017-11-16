# -*- coding: utf-8 -*-
'''Thread-based scheduling backend.

This module contains an implementation of a scheduling backend that leverages
Python "threads" (:mod:`~threading` module) and producer-consumer queues
(:mod:`~queue` module).
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

    :param int n_workers: The number of worker threads to use.
    :param float sleep_interval: The delay (in seconds) to wait before retrying
        to execute further jobs if the worker queue is starving. This typically
        happens when there are more workers available than tasks pending
        because of dependencies between the tasks.
    '''

    def __init__(self, n_workers=1, sleep_interval=1.0):

        self.n_workers = n_workers
        self.sleep_interval = sleep_interval

    def execute_tasks(self, tasks, graph, env):
        '''Execute the tasks.

        :param iterable tasks: Iterable over tasks to be executed, possibly
                               sorted according to some order.
        :param DepGraph graph: Dependency graph for the tasks.
        :param env: An initial environment for the scheduled tasks.
        :type env: mapping or None
        '''

        import time
        import queue

        threads = []
        q = queue.Queue(self.n_workers)
        env_lock = threading.Lock()

        # initialize the environment
        for task in tasks:
            env.setdefault('tasks', {}).setdefault(task.name, {
                'status': TaskStatus.SCHEDULED
                })

        # spawn workers
        for i in range(self.n_workers):
            t = QueueScheduling.WorkerThread(q, env, env_lock)
            t.start()
            threads.append(t)

        # process tasks
        tasks_left = tasks
        while len(tasks_left) > 0:
            tasks_still_left = []
            n_tasks_left = len(tasks_left)
            for task in tasks_left:
                with env_lock:
                    status = env['tasks'][task.name]['status']
                logger.debug('status of task %s: %s', task, status)

                # skip failed/notrun/completed tasks
                if status != TaskStatus.SCHEDULED:
                    continue

                deps = list(graph.dependencies(task))
                with env_lock:
                    failed_deps = any(
                        env['tasks'][t.name]['status'] == TaskStatus.FAILURE
                        or env['tasks'][t.name]['status'] == TaskStatus.NOTRUN
                        for t in deps)
                    can_run = all(
                        env['tasks'][t.name]['status'] == TaskStatus.SUCCESS
                        for t in deps)
                logger.debug('task %s has failed deps: %s', task, failed_deps)
                logger.debug('task %s can run: %s', task, can_run)
                if failed_deps:
                    with env_lock:
                        env['tasks'][task.name]['status'] = TaskStatus.NOTRUN
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

        :param queue: The producer-consumer task queue.
        :param env: The execution environment for the tasks.
        :param env_lock: A lock that must be held for any atomic modification
                         of `env`.
        '''

        def __init__(self, queue, env, env_lock):
            super().__init__()
            self.queue = queue
            self.env = env
            self.env_lock = env_lock

        def apply(self, env_update, task_name, status):
            '''Apply un update to an existing environment.'''

            def apply_worker(update, old):
                for k, v in update.items():
                    if isinstance(v, MutableMapping):
                        if k in old:
                            # recursively update this dictionary
                            apply_worker(v, old[k])
                        else:
                            old[k] = v
                    else:
                        old[k] = v

            with self.env_lock:
                if env_update is not None:
                    apply_worker(env_update, self.env)
                self.env.setdefault('tasks', {}).setdefault(task_name, {
                    'status': status
                    })

        def run(self):
            '''Main method: run this thread.'''

            logger.debug('worker %s starting', self.name)
            while True:
                task = self.queue.get()
                logger.debug('worker %s got task %s', self.name, task)
                if task is None:
                    logger.debug('worker %s exiting', self.name)
                    break

                with self.env_lock:
                    # we start to work on the task
                    self.env['tasks'][task.name]['status'] = TaskStatus.PENDING

                try:
                    env_update = task.do(self.env)
                except Exception as ex:
                    logger.exception('task %s on worker %s failed: %s',
                                     task, self.name, ex)
                    with self.env_lock:
                        self.env['tasks'][task.name]['status'] = \
                                TaskStatus.FAILURE
                        logger.error('task %s failed', task)
                    logger.debug('saving FAILURE status in the environment...')
                    self.apply(None, task.name, TaskStatus.FAILURE)
                    logger.debug('environment updated: %s', self.env)
                else:
                    logger.debug('task %s on worker %s succeeded',
                                 task, self.name)
                    with self.env_lock:
                        self.env['tasks'][task.name]['status'] = \
                                TaskStatus.SUCCESS
                    logger.debug('proposed environment update: %s', env_update)
                    self.apply(env_update, task.name, TaskStatus.SUCCESS)

                logger.debug('worker %s wants more!', self.name)
                self.queue.task_done()
