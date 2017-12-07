# -*- coding: utf-8 -*-
'''This module contains an implementation of a scheduling backend that
leverages Python "threads" (:mod:`~threading` module) and producer-consumer
queues (:mod:`~queue` module).
'''

import threading
import logging


LOGGER = logging.getLogger(__name__)


class QueueScheduling:
    '''The default scheduling backend.

    Uses :mod:`threading` and :mod:`queue` to handle concurrent execution of
    tasks.
    '''

    def __init__(self, n_workers=10):

        '''Initialize the queue backend.

        :param int n_workers: The number of worker threads to use.
        '''

        import queue
        self.n_workers = n_workers
        self.queue = queue.Queue(0)

    def _enqueue(self, tasks, graph, env):
        '''Enqueue as many tasks as the dependencies permit.'''

        n_tasks = len(tasks)
        tasks_left = []
        LOGGER.debug('master: %d tasks left to schedule', n_tasks)
        for task in tasks:
            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug('master: status of task %s: %s',
                             task, env.get_status(task))

            # skip failed/notrun/completed tasks
            if not env.is_waiting(task):
                LOGGER.debug('master: task %s removed from queue', task)
                continue

            deps = graph.dependencies(task)

            def _check_deps(env_):
                '''Check deps to see if there are failures or if we can run.'''
                failed_deps = any(env_.is_failed(t) or env_.is_skipped(t)
                                  for t in deps)
                can_run = all(env_.is_done(t) for t in deps)
                return failed_deps, can_run

            failed_deps, can_run = env.atomically(_check_deps)
            LOGGER.debug('master: task %s has failed deps: %s',
                         task, failed_deps)
            LOGGER.debug('master: task %s can run: %s', task, can_run)
            if failed_deps:
                env.set_skipped(task)
                n_tasks -= 1
                LOGGER.info('task %s cannot be run, %d left',
                            task, n_tasks)
            elif can_run:
                self.queue.put(task)
                n_tasks -= 1
                LOGGER.debug('master: task %s scheduled, %d left',
                             task, n_tasks)
            else:
                LOGGER.debug('master: task %s blocked by dependencies', task)
                tasks_left.append(task)

        return tasks_left

    def execute_tasks(self, tasks, graph, env):
        '''Execute the tasks.

        :param iterable tasks: Iterable over tasks to be executed, possibly
                               sorted according to some order.
        :param DepGraph graph: Dependency graph for the tasks.
        :param env: An initial environment for the scheduled tasks.
        :type env: Env
        '''

        threads = []
        # Use a condition variable to block when no more tasks can be submitted
        # because of dependencies. The master calls cond_var.wait() and the
        # worker threads call cond_var.notify() when they are finished with a
        # task.
        cond_var = threading.Condition()

        # spawn workers
        LOGGER.debug('master: spawning %s workers...', self.n_workers)
        for _ in range(self.n_workers):
            thread = QueueScheduling.WorkerThread(self.queue, env, cond_var)
            thread.start()
            threads.append(thread)

        # process tasks
        tasks_left = tasks
        while tasks_left:
            n_tasks_left = len(tasks_left)
            with cond_var:
                tasks_left = self._enqueue(tasks_left, graph, env)

                if not tasks_left:
                    # we're done!
                    break

                if n_tasks_left == len(tasks_left):
                    LOGGER.debug('master: worker queue is starving because of '
                                 'dependencies, going to sleep...')
                    # release the cond_var lock and wait for workers to call
                    # cond_var.notify()
                    cond_var.wait()
                    LOGGER.debug('master: ...woke up!')

        # block until all tasks are done
        self.queue.join()

        # stop workers and go home
        for _ in range(self.n_workers):
            self.queue.put(None)
        for thread in threads:
            thread.join()

    class WorkerThread(threading.Thread):
        '''Workhorse class for :class:`QueueScheduling`. This class consumes
        (i.e. executes) tasks passed to it through the queue.
        '''

        def __init__(self, queue, env, cond_var):
            '''Initialize the thread.

            :param queue: The producer-consumer task queue.
            :param env: The execution environment for the tasks.
            :param cond_var: A condition variable to notify when we are
                             finished running a task
            '''
            super().__init__()
            self.queue = queue
            self.env = env
            self.cond_var = cond_var

        def run(self):
            '''Main method: run this thread.'''

            LOGGER.debug('worker %s: starting', self.name)
            while True:
                task = self.queue.get()
                if task is None:
                    LOGGER.debug('worker %s: exiting', self.name)
                    break
                LOGGER.debug('worker %s: got task %s', self.name, task)

                # we start to work on the task
                self.env.set_pending(task)

                try:
                    env_update, status = task.do(self.env)
                except Exception as ex:  # pylint: disable=broad-except
                    LOGGER.exception('task %s on worker %s failed: %s',
                                     task, self.name, ex)
                    LOGGER.debug('worker %s: setting FAILED status in the '
                                 'environment...', self.name)
                    self.env.set_failed(task)
                else:
                    LOGGER.debug('worker %s: task %s completed '
                                 'with status %s', self.name, task, status)
                    LOGGER.debug('worker %s: proposed environment update: %s',
                                 self.name, env_update)
                    self.env.set_status(task, status)
                    self.env.apply(env_update)

                LOGGER.debug('worker %s: wants more!', self.name)
                self.queue.task_done()

                # notify the master that a new task has completed
                with self.cond_var:
                    LOGGER.debug('worker %s: notifies master', self.name)
                    self.cond_var.notify_all()
