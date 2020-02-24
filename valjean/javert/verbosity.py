'''Verbosity module.

4 levels of verbosity exist to build tables and plots: SILENT, SUMMARY,
INTERMEDIATE and FULL_DETAILS.
'''
from enum import Enum


class Verbosity(Enum):
    '''Verbosity enum.

    Four levels are currently available: SILENT, SUMMARY, INTERMEDIATE,
    FULL_DETAILS.
    '''
    SILENT = 0
    SUMMARY = 1
    INTERMEDIATE = 2
    FULL_DETAILS = 3
    DEVELOPMENT = 4
