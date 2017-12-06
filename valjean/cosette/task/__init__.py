'''Top module for :mod:`~valjean.cosette.task`.'''

import enum

#: Enumeration for the task status
TaskStatus = enum.Enum('TaskStatus',  # pylint: disable=invalid-name
                       'WAITING PENDING DONE FAILED SKIPPED')
