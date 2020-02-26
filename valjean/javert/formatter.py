'''This module contains the :class:`Formatter` abstract base class. All other
formatters must derive from it.
'''

from abc import ABC, abstractmethod


class Formatter(ABC):
    '''Abstract base class for any formatter.'''

    @abstractmethod
    def header(self, name, depth):
        '''Format a section header.'''
        raise NotImplementedError('header() method is not implemented')

    def text(self, text):
        '''Format some text.'''
        raise NotImplementedError('text() method is not implemented')

    def template(self, item):
        '''Convert an item to the relevant format.'''
        class_name = item.__class__.__name__
        meth_name = 'format_' + class_name.lower()
        print('LOOKing for', meth_name)
        try:
            meth = getattr(self, meth_name)
        except AttributeError:
            return ''
        return meth(item)
