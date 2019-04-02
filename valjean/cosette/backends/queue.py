# -*- coding: utf-8 -*-
'''This module contains an implementation of a scheduling backend that
leverages Python "threads" (:mod:`~threading` module) and producer-consumer
queues (:mod:`~queue` module).
'''

import threading
import logging
import time


LOGGER = logging.getLogger('valjean')


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

    def _enqueue(self, tasks, full_graph, hard_graph, env):
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
                if env.is_done(task):
                    LOGGER.info("task %s is already done and won't be rerun",
                                task)
                LOGGER.debug('master: task %s removed from queue', task)
                continue

            deps = full_graph.dependencies(task)
            hard_deps = hard_graph.dependencies(task)
            assert all(task in deps for task in hard_deps)

            def _check_deps(env_):
                '''Check dependencies of the current task and make a decision
                about what we should do with this task.

                This function returns the list of failed hard dependencies for
                the task and a bool telling whether all the dependencies have
                completed (regardless of their success).

                :param Env env_: the environment.
                :rtype: (list(Task), bool)
                '''
                hard_failed_deps = [t for t in hard_deps
                                    if env_.is_failed(t) or env_.is_skipped(t)]
                deps_finished = all(env_.is_done(t)
                                    or env_.is_failed(t)
                                    or env_.is_skipped(t) for t in deps)
                return hard_failed_deps, deps_finished

            hard_failed_deps, deps_finished = env.atomically(_check_deps)

            if hard_failed_deps:
                LOGGER.debug('master: task %s has failed deps: %s',
                             task, hard_failed_deps)
                env.set_skipped(task)
                n_tasks -= 1
                LOGGER.info('task %s cannot be run, %d left',
                            task, n_tasks)
            elif deps_finished:
                LOGGER.debug('master: task %s can run', task)
                self.queue.put(task)
                n_tasks -= 1
                LOGGER.debug('master: task %s scheduled, %d left',
                             task, n_tasks)
            else:
                LOGGER.debug('master: task %s blocked by dependencies', task)
                tasks_left.append(task)

        return tasks_left

    def execute_tasks(self, *, full_graph, hard_graph, env, config):
        '''Execute the tasks.

        :param DepGraph full_graph: Full dependency graph for the tasks, i.e.
                                    including both hard and soft dependencies.
        :param DepGraph hard_graph: Hard-dependency graph for the tasks.
        :param env: An initial environment for the scheduled tasks.
        :type env: Env
        :param env: The configuration object (for things like paths, etc.).
        :type env: Config
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
            thread = QueueScheduling.WorkerThread(self.queue, env, config,
                                                  cond_var)
            thread.start()
            threads.append(thread)

        # process tasks; sort them in topological order
        tasks_left = full_graph.topological_sort()
        while tasks_left:
            n_tasks_left = len(tasks_left)
            with cond_var:
                tasks_left = self._enqueue(tasks_left, full_graph, hard_graph,
                                           env)

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

        def __init__(self, queue, env, config, cond_var):
            '''Initialize the thread.

            :param queue: The producer-consumer task queue.
            :param env: The execution environment for the tasks.
            :param config: The configuration for the tasks.
            :param cond_var: A condition variable to notify when we are
                             finished running a task
            '''
            super().__init__()
            self.queue = queue
            self.config = config
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
                LOGGER.info('task %s starts', task)

                # we start to work on the task
                self.env.set_pending(task)

                start = time.time()
                try:
                    env_update, status = task.do(self.env, self.config)
                except Exception as ex:  # pylint: disable=broad-except
                    LOGGER.exception('task %s on worker %s failed: %s',
                                     task, self.name, ex)
                    LOGGER.debug('worker %s: setting FAILED status in the '
                                 'environment...', self.name)
                    self.env.set_failed(task)
                else:
                    LOGGER.debug('worker %s: task %s completed '
                                 'with status %s', self.name, task, status)
                    LOGGER.info('task %s completed with status %s',
                                task, status)
                    LOGGER.debug('worker %s: proposed environment update: %s',
                                 self.name, env_update)
                    self.env.set_status(task, status)
                    self.env.apply(env_update)
                end = time.time()
                self.env.set_start_end_clock(task, start=start, end=end)

                LOGGER.debug('worker %s: wants more!', self.name)
                self.queue.task_done()

                # notify the master that a new task has completed
                with self.cond_var:
                    LOGGER.debug('worker %s: notifies master', self.name)
                    self.cond_var.notify_all()
