'''Module for the ``report`` subcommand.'''


from ..common import Command
from ...javert.test_report import TestReportTask


class ReportCommand(Command):
    '''Command class for the ``report`` subcommand.'''

    NAME = 'report'

    PRIORITY = TestReportTask.PRIORITY

    HELP = 'build reports'
