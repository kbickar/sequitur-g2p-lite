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

from math import *

gold  = (1 + sqrt(5)) / 2
cGold = (3 - sqrt(5)) / 2


def bracketMinimum(f, xa, xb):
    pass


maxIterations = 100
zEpsilon = 1.0e-18


def linearMinimization(f, x=None, lower=None, upper=None, tolerance = 1.0e-10, maxIterations = maxIterations):
    pass

def hasConverged(fCurrent, fOld, tolerance):
    pass


def directionSetMinimization(f, initialPoint, directions = None, tolerance = 1.0e-10, maxIterations = maxIterations):
    pass

def hasSignificantDecrease(series):
    pass
