#!/usr/bin/env python
# Written by Eric Crosson
# 2015-09-19

"""Simulate an EDF scheduler.

An Earliest Deadline First (EDF) scheduler selects which task from the queue of
work to do by choosing the task with the nearest deadline.

Tasks are considered to be periodic (except for one-shot tasks, see below).

"""

from time import time
from collections import MutableMapping


class TaskPool(MutableMapping):

    """Behave like a dict, but return an empty list on undefined key access."""

    def __init__(self, *args, **kwargs):
        # TODO: make a static class var, not an object var
        self.default_value = []
        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        """Return a default value if key has no value yet."""
        try:
            self.store[key]
        except KeyError:
            self.store[key] = self.default_value
        finally:
            return key


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
        self.last_ran = last_ran
        self.deadline = time() + interval


class EDF():

    def __init__(self):
        """Initialize the EDF internals."""
        self.pool = TaskPool()


    def add_job(self, function, interval, one_shot = False):
        """Add task to EDF scheduler, with period interval."""
        task = Task(function, interval, one_shot)
        task_pool = self.pool[interval]
        # TODO: resume sorting
        task_pool.insert(task)
        self.pool[interval] += task


    def remove_task(self, task, interval = None):
        """Remove a task from the EDF queue. Optionally supply the interval for faster
        removal time.

        :param:  task            the task to remove from the EDF task pool
        :param:  interval        optionally specify the interval for reduced
                                 searching time

        """
        pass


    def execute():
        """Begin execution of scheduled tasks."""
        # TODO: spawn thread to execute tasks
        pass


    def stop():
        """Stop execution of scheduled tasks."""
        # TODO: stop thread executing tasks
        pass


    def pop_task():
        """Select the next EDF task."""
        # TODO: make this a real task with dummy defaults
        edf_task = None
        for interval, task_queue in self.pool.items():
            task = task_queue[0]
            if task.deadline < edf_task.deadline:
                edf_task = task
        return edf_task



def print_time():
    print('Current time: %s' % time())


def print_troll():
    print("\t\tI'm a grumpy old troll, heh")



if __name__ == "__main__":
    scheduler = EDF()
    print('Scheduling jobs')
    scheduler.add_job(print_time, 1)
    scheduler.add_job(print_troll, 5)
    print('Beginning scheduler')
    scheduler.execute()
