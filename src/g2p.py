#!/usr/bin/env python
from __future__ import print_function
"""
Grapheme-to-Phoneme Conversion

Samples can be either in plain format (one word per line followed by
phonetic transcription) or Bliss XML Lexicon format.
"""

__author__    = 'Maximilian Bisani'
__version__   = '$LastChangedRevision: 1667 $'
__date__      = '$LastChangedDate: 2007-06-02 16:32:35 +0200 (Sat, 02 Jun 2007) $'
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

The full source is available at: https://github.com/kbickar/sequitur-g2p-lite
"""

import math, sys
import SequiturTool
from sequitur import Translator
from misc import gOpenIn, gOpenOut, set

# ===========================================================================
def loadPlainSample(fname, encoding = None):
    sample = []
    for line in gOpenIn(fname, encoding or defaultEncoding):
        fields = line.split()
        if not fields: continue
        left  = tuple(fields[0])
        right = tuple(fields[1:])
        sample.append((left, right))
    return sample

def loadG2PSample(fname):
    if fname == '-':
        sample = loadPlainSample(fname)
    else:
        firstLine = gOpenIn(fname, defaultEncoding).readline()
        if firstLine.startswith('<?xml'):
            sample = [ (tuple(orth), tuple(phon))
                       for orth, phon in loadBlissLexicon(fname) ]
        else:
            sample = loadPlainSample(fname)
    return sample
# ===========================================================================
def readApply(fname, encoding = None):
    for line in gOpenIn(fname, encoding):
        word = line.strip()
        left = tuple(word)
        yield word, left 
        
# ===========================================================================
class MemoryTranslator:
    def __init__(self, sample):
        self.memory = dict(sample)

    TranslationFailure = Translator.TranslationFailure

    def __call__(self, left):
        if left in self.memory:
            return self.memory[left]
        else:
            raise self.TranslationFailure()

    def reportStats(self, f):
        pass

# ===========================================================================
def mainTest(translator, testSample, options):
    if options.testResult:
        resultFile = gOpenOut(options.testResult, defaultEncoding)
    else:
        resultFile = None
    from Evaluation import Evaluator
    evaluator = Evaluator()
    evaluator.setSample(testSample)
    evaluator.resultFile = resultFile
    evaluator.verboseLog = stdout
    if options.test_segmental:
        supraSegmental = set(['.', "'", '"'])
        def removeSupraSegmental(phon):
            return filter(lambda p: p not in supraSegmental, phon)
        evaluator.compareFilter = removeSupraSegmental
    result = evaluator.evaluate(translator)
    print(result)

def mainApply(translator, options):
    if options.phoneme_to_phoneme:
        words = readApplyP2P(options.applySample, options.encoding)
    else:
        words = readApply(options.applySample, options.encoding)

    if options.variants_mass or options.variants_number:
        wantVariants = True
        threshold = options.variants_mass or 1.0
        nVariantsLimit = options.variants_number or 1e9
    else:
        wantVariants = False

    for word, left in words:
        try:
            if wantVariants:
                totalPosterior = 0.0
                nVariants = 0
                nBest = translator.nBestInit(left)
                while totalPosterior < threshold and nVariants < nVariantsLimit:
                    try:
                        logLik, result = translator.nBestNext(nBest)
                    except StopIteration:
                        break
                    posterior = math.exp(logLik - nBest.logLikTotal)
                    print(('%s\t%d\t%f\t%s' % \
                          (word, nVariants, posterior, ' '.join(result))))
                    totalPosterior += posterior
                    nVariants += 1
            else:
                result = translator(left)
                print(('%s\t%s' % (word, ' '.join(result))))
        except translator.TranslationFailure:
            exc = sys.exc_info()[1]
            try:
                print('failed to convert "%s": %s' % (word, exc), file=stderr)
            except:
                pass

def mainApplyWord(translator, options):
    if options.variants_mass or options.variants_number:
        wantVariants = True
        threshold = options.variants_mass or 1.0
        nVariantsLimit = options.variants_number or 1e9
    else:
        wantVariants = False
        
    word = options.applyWord
    left = tuple(word)
    try:
        if wantVariants:
            totalPosterior = 0.0
            nVariants = 0
            nBest = translator.nBestInit(left)
            while totalPosterior < threshold and nVariants < nVariantsLimit:
                try:
                    logLik, result = translator.nBestNext(nBest)
                except StopIteration:
                    break
                posterior = math.exp(logLik - nBest.logLikTotal)
                defn = ' '.join(result)
                print(f"{word}\t{posterior:.3f}\t{defn}")
                totalPosterior += posterior
                nVariants += 1
        else:
            result = translator(left)
            print(('%s\t%s' % (word, ' '.join(result))))
    except translator.TranslationFailure:
        exc = sys.exc_info()[1]
        try:
            print('failed to convert "%s": %s' % (word, exc), file=stderr)
        except:
            pass


def main(options, args):
    if options.phoneme_to_phoneme:
        loadSample = loadP2PSample
    else:
        loadSample = loadG2PSample

    if options.fakeTranslator:
        translator = MemoryTranslator(loadSample(options.fakeTranslator))
    else:
        model = SequiturTool.procureModel(options, loadSample, log=stdout)
        if not model:
            return 1
        if options.testSample or options.applySample or options.applyWord:
            translator = Translator(model)
            if options.stack_limit:
                translator.setStackLimit(options.stack_limit)
        del model

    if options.testSample:
        mainTest(translator, loadSample(options.testSample), options)
        translator.reportStats(sys.stdout)

    if options.applySample:
        mainApply(translator, options)
        translator.reportStats(sys.stderr)

    if options.applyWord:
        mainApplyWord(translator, options)

# ===========================================================================
if __name__ == '__main__':
    import optparse, tool
    optparser = optparse.OptionParser(
        usage   = '%prog [OPTION]... FILE...\n' + str(__doc__),
        version = '%prog ' + __version__)
    tool.addOptions(optparser)
    optparser.add_option(
        '-m', '--model', dest='modelFile',
        help='read model from FILE', metavar='FILE')
    optparser.add_option(
        '-x', '--test', dest='testSample',
        help='read test sample from FILE', metavar='FILE')
    optparser.add_option(
        '-e', '--encoding', default='ISO-8859-15',
        help='use character set encoding ENC', metavar='ENC')
    optparser.add_option(
        '-P', '--phoneme-to-phoneme', action='store_true',
        help='train/apply a phoneme-to-phoneme converter')
    optparser.add_option(
        '--test-segmental', action='store_true',
        help='evaluate only at segmental level, i.e. do not count syllable boundaries and stress marks')
    optparser.add_option(
        '-B', '--result', dest='testResult',
        help='store test result in table FILE (for use with bootlog or R)', metavar='FILE')
    optparser.add_option(
        '-a', '--apply', dest='applySample',
        help='apply grapheme-to-phoneme conversion to words read from FILE', metavar='FILE')
    optparser.add_option(
        '-w', '--word', dest='applyWord',
        help='apply grapheme-to-phoneme conversion to word', metavar='string')
    optparser.add_option(
        '-V', '--variants-mass', type='float',
        help='generate pronunciation variants until \sum_i p(var_i) >= Q (only effective with --apply)', metavar='Q')
    optparser.add_option(
        '--variants-number', type='int',
        help='generate up to N pronunciation variants (only effective with --apply)', metavar='N')
    optparser.add_option(
        '-f', '--fake', dest='fakeTranslator',
        help='use a translation memory (read from sample FILE) instead of a genuine model (use in combination with -x to evaluate two files against each other)', metavar='FILE')
    optparser.add_option(
        '--stack-limit', type='int',
        help='limit size of search stack to N elements', metavar='N')

    options, args = optparser.parse_args()

    global stdout, stderr, defaultEncoding
    if sys.version_info[:2] <= (2, 5):
        import codecs
        global defaultEncoding
        defaultEncoding = options.encoding
        encoder, decoder, streamReader, streamWriter = codecs.lookup(options.encoding)
        stdout = streamWriter(sys.stdout)
        stderr = streamWriter(sys.stderr)
    else:
        defaultEncoding = options.encoding
        stdout = sys.stdout
        stderr = sys.stderr

    tool.run(main, options, args)
