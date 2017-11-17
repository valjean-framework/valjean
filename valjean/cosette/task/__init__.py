import enum

#: Enumeration for the task status
TaskStatus = enum.Enum('TaskStatus',
                       'WAITING PENDING DONE FAILED SKIPPED')
