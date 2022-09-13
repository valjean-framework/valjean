# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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
        try:
            meth = getattr(self, meth_name)
        except AttributeError:
            return ''
        return meth(item)
