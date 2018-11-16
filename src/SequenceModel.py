from __future__ import division
from __future__ import print_function

__author__    = 'Maximilian Bisani'
__version__   = '$LastChangedRevision: 1668 $'
__date__      = '$LastChangedDate: 2007-06-02 18:14:47 +0200 (Sat, 02 Jun 2007) $'
__copyright__ = 'Copyright (c) 2004-2005  RWTH Aachen University'
__license__   = """
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License Version 2 (June
1991) as published by the Free Software Foundation.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, you will find it at
http://www.gnu.org/licenses/gpl.html, or write to the Free Software
Foundation, Inc., 51 Franlin Street, Fifth Floor, Boston, MA 02110,
USA.
 
Should a provision of no. 9 and 10 of the GNU General Public License
be invalid or become invalid, a valid provision is deemed to have been
agreed upon which comes closest to what the parties intended
commercially. In any case guarantee/warranty shall be limited to gross
negligent actions or intended actions or fraudulent concealment.
"""

import copy, math
from misc import set
import sequitur_


class AccuDict(dict):
    pass

class EvidenceList:
    pass

class BackOffModel:
    pass

class SequenceModelEstimator:
    pass

class SequenceModel(sequitur_.SequenceModel):
    def __getstate__(self):
        dct = copy.copy(self.__dict__)
        del dct['this']
        return (self.init(), self.term(), self.get(), dct)

    def __setstate__(self, data):
        super(SequenceModel, self).__init__()
        init, term, data, dct = data
        self.setInitAndTerm(init, term)
        self.set(data)
        self.__dict__.update(dct)

    def size(self):
        return len(self.get())
