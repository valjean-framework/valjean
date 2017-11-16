import enum


TaskStatus = enum.Enum('TaskStatus',
                       'SCHEDULED PENDING SUCCESS FAILURE NOTRUN')
