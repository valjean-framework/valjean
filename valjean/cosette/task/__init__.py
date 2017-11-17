import enum

#: Enumeration for the task status
TaskStatus = enum.Enum('TaskStatus',
                       'SCHEDULED PENDING SUCCESS FAILURE NOTRUN')
