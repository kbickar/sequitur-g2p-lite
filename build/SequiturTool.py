from __future__ import division, print_function

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
try:
    import cPickle as pickle
except:
    import pickle
from tool import UsageError
import sys

class Tool:
    def __init__(self, options, loadSample, log=sys.stdout):
        self.options = options
        self.loadSample = loadSample
        self.log = log

    def procureModel(self):
        if self.options.modelFile:
            if sys.version_info[:2] >= (3, 0):
                model = pickle.load(open(self.options.modelFile, 'rb'), encoding='latin1')
            else:
                try:
                    f = open(self.options.modelFile, 'rb')
                    model = pickle.load(f)
                except ValueError:
                    print('This error most likely occured because the loaded model was created in python3.\n', file=sys.stderr)
                    raise
                
            self.sequitur = model.sequitur
        else:
            self.sequitur = Sequitur()
            model = None

        if not model:
            raise UsageError
        return model

def procureModel(options, loadSample, log=sys.stdout):
    tool = Tool(options, loadSample, log)
    return tool.procureModel()

