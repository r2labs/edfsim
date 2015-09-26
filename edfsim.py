#!/usr/bin/env python
# Written by Eric Crosson
# 2015-09-19

"""Simulate an EDF scheduler.

An Earliest Deadline First (EDF) scheduler selects which task from the queue of
work to do by choosing the task with the nearest deadline.

Tasks are considered to be periodic (except for one-shot tasks, see below).

"""

from sys import exit
from time import time


class NoScheduledTaskException(Exception):
    pass


class Task():

    """A task to be executed by the EDF scheduler."""

    def __init__(self, task, interval, one_shot, last_ran = None):
        """Initialize a task with metadata.

        :param:  task            the function to execute
        :param:  interval        the interval on which to execute task
        :param:  one_shot        flag indicating task runs only once
        :param:  last_ran        timestamp indicating last execution of task

        """
        self.task = task
        self.interval = interval
        self.one_shot = one_shot
        self.last_ran = last_ran
        self.deadline = time() + interval
        self.execution_times = []


    def __str__(self):
        return self.task.__name__


class EDF():

    def __init__(self):
        """Initialize the EDF internals."""
        self.pool = {}


    def add_job(self, function, interval, one_shot = False):
        """Add task to EDF scheduler, with period interval."""
        task = Task(function, interval, one_shot)
        task_pool = []
        try:
            task_pool = self.pool[interval]
        except:
            pass
        task_pool.append(task)
        task_pool.sort(key=lambda x: x.deadline)
        self.pool[interval] = task_pool


    def remove_job(self, function, interval = None):
        # TODO : call remove_task
        if interval is None:
            for intvl, task_pool in self.pool.items():
                if interval is not None:
                    break
                for task in task_pool:
                    if task.task == function:
                        interval = intvl
                        break

        remove_task(task, interval)


    def remove_task(self, task, interval = None):
        """Remove a task from the EDF queue. Optionally supply the interval for faster
        removal time.

        :param:  task            the task to remove from the EDF task pool
        :param:  interval        optionally specify the interval for reduced
                                 searching time

        """
        if interval is None:
            for intvl, task_pool in self.pool.items():
                if interval is not None:
                    break
                for task in task_pool:
                    if task == task:
                        interval = intvl
                        break

        task_pool = self.pool[interval]
        task_pool.remove(task)
        self.pool[interval] = task_pool


    def start(self):
        """Begin execution of scheduled tasks."""
        # TODO: spawn thread to execute tasks
        count = time() + 4
        while True:
            task = self.pop_task()
            ret = self.execute(task)
            print('ret: %s' % ret)

            if time() > count:
                exit()


    def stop(self):
        """Stop execution of scheduled tasks."""
        # TODO: stop thread executing tasks
        pass


    def execute(self, task):
        """Execute task."""
        execution_start = time()
        ret = task.task()
        execution_end = time()
        execution_time = execution_end - execution_start
        task.execution_times.append(execution_time)
        task.last_ran = time()
        task.deadline = time() + task.interval
        return ret


    def pop_task(self):
        """Select the next EDF task.

        One-shot tasks are not re-scheduled.

        """
        try:
            tasks = [q[0] for interval, q in self.pool.items()]
            tasks.sort(key=lambda x: x.deadline)
            edf = tasks[0]
            if edf.one_shot:
                self.remote_task(edf)
            return edf
        except:
            raise NoScheduledTaskException()



def print_time():
    print('Current time: %s' % time())
    return 1


def print_troll():
    print("\t\tI'm a grumpy old troll, heh")
    return 2



if __name__ == '__main__':
    scheduler = EDF()
    print('Scheduling jobs')
    scheduler.add_job(print_time, 1)
    scheduler.add_job(print_troll, 2)
    print('Beginning scheduler')
    scheduler.start()
