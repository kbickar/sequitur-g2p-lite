from __future__ import division
from __future__ import print_function

__author__    = 'Maximilian Bisani'
__version__   = '$LastChangedRevision: 1691 $'
__date__      = '$LastChangedDate: 2011-08-03 15:38:08 +0200 (Wed, 03 Aug 2011) $'
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

import itertools, math, sys
import sequitur_, SequenceModel, misc
from symbols import SymbolInventory
from misc import reversed, sorted, set

class MultigramInventory(sequitur_.MultigramInventory):
    def __getstate__(self):
        return [ self.symbol(i) for i in range(1, self.size() + 1) ]

    def __setstate__(self, data):
        super(MultigramInventory, self).__init__()
        for i, lr in enumerate(data):
            j = self.index(lr)
            assert j == i+1

    def sizeTemplates(self):
        result = set()
        for i in range(1, self.size() + 1):
            left, right = self.symbol(i)
            result.add((len(left), len(right)))
        return sorted(result)

class Sequitur:
    pass

class Model(object):
    discount = None
    sequenceModel = None        

# ===========================================================================
class Translator:
    def __init__(self, model):
        self.setModel(model)

    def setModel(self, model):
        self.model = model
        self.sequitur = self.model.sequitur
        self.translator = sequitur_.Translator()
        self.translator.setMultigramInventory(self.sequitur.inventory)
        self.translator.setSequenceModel(self.model.sequenceModel)

    def setStackLimit(self, n):
        self.translator.setStackLimit(n)

    class TranslationFailure(RuntimeError):
        pass

    def unpackJoint(self, joint):
        assert joint[0] == self.sequitur.term
        assert joint[-1] == self.sequitur.term
        return [ self.sequitur.inventory.symbol(q) for q in joint[1:-1] ]

    def translateFirstBest(self, left):
        left = self.sequitur.leftInventory.parse(left)
        try:
            logLik, joint = self.translator(left)
        except RuntimeError:
            exc = sys.exc_info()[1]
            raise self.TranslationFailure(*exc.args)
        return logLik, self.unpackJoint(joint)

    def firstBestJoint(self, left):
        logLik, joint = self.translateFirstBest(left)
        joint = [ (self.sequitur.leftInventory.format(left),
                   self.sequitur.rightInventory.format(right))
                  for left, right in joint ]
        return logLik, joint

    def jointToLeftRight(self, joint):
        left  = [ l for ll, rr in joint for l in ll ]
        left = self.sequitur.leftInventory.format(left)
        right = [ r for ll, rr in joint for r in rr ]
        right = self.sequitur.rightInventory.format(right)
        return left, right

    def firstBest(self, left):
        logLik, joint = self.translateFirstBest(left)
        left2, right = self.jointToLeftRight(joint)
        assert tuple(left) == left2
        return logLik, right

    def __call__(self, left):
        logLik, right = self.firstBest(left)
        return right

    def nBestInit(self, left):
        left = self.sequitur.leftInventory.parse(left)
        try:
            result = self.translator.nBestInit(left)
        except RuntimeError:
            exc = sys.exc_info()[1]
            raise self.TranslationFailure(*exc.args)
        result.thisown = True
        result.logLikBest = self.translator.nBestBestLogLik(result)
        result.logLikTotal = self.translator.nBestTotalLogLik(result)
        return result

    def nBestNext(self, nBestContext):
        try:
            logLik, joint = self.translator.nBestNext(nBestContext)
        except RuntimeError:
            exc = sys.exc_info()[1]
            if exc.args[0] == 'no further translations':
                raise StopIteration
            else:
                raise self.TranslationFailure(*exc.args)
        joint = self.unpackJoint(joint)
        left, right = self.jointToLeftRight(joint)
        return logLik, right

    def reportStats(self, f):
        print('stack usage: ', self.translator.stackUsage(), file=f)

