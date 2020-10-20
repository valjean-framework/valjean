'''Verbosity module.

4 levels of verbosity exist to build tables and plots: SILENT, SUMMARY,
INTERMEDIATE and FULL_DETAILS.
'''
from enum import Enum


class Verbosity(Enum):
    '''Verbosity enum.

    Six levels are currently available: SILENT, SUMMARY, DEFAULT,
    INTERMEDIATE, FULL_DETAILS, DEVELOPMENT.
    '''
    SILENT = 0
    SUMMARY = 1
    DEFAULT = 2
    INTERMEDIATE = 3
    FULL_DETAILS = 4
    DEVELOPMENT = 5
