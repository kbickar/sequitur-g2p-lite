Sequitur G2P Lite
============

A Grapheme-to-Phoneme converter that uses a trained model.

Introduction
------------

Sequitur G2P is a data-driven grapheme-to-phoneme converter written at
RWTH Aachen University by Maximilian Bisani.

The method used in this software is described in

```
   M. Bisani and H. Ney: "Joint-Sequence Models for Grapheme-to-Phoneme
   Conversion". Speech Communication, Volume 50, Issue 5, May 2008,
   Pages 434-451

   (avaliable online at http://dx.doi.org/10.1016/j.specom.2008.01.002)
```

This software is made available to you under terms of the GNU Public
License. It can be used for experimentation and as part of other free
software projects. For details see the licensing terms below.

If you publish about work that involves the use of this software,
please cite the above paper. (You should feel obliged to do so by
rules of good scientific conduct.)

You may contact the author with any questions or comments via e-mail:
maximilian.bisani@rwth-aachen.de

Installing
----------

To build and use this software you need to have the following part installed:
- Python (http://www.python.org)
  tested with 2.5, 2.7 and 3.6
- SWIG (http://www.swig.org)
  tested with 1.3.31
- a C++ compiler that's recognized by Python's distutils.
  tested with GCC 4.1, 4.2 and 4.3

To install change to the source directory and type:
    ```python setup.py install --prefix /usr/local```
You may substitue /usr/local with some other directory.  If you do so
make sure that `some-other-directory/lib/python2.5/site-packages/` is in
your PYTHONPATH, e.g. by typing
    ```export PYTHONPATH=some-other-directory/lib/python2.7/site-packages```

You can also install via `pip` by pointing it at this repository. You still
need SWIG and a C++ compiler.
```
pip install git+https://github.com/kbickar/sequitur-g2p0lite@master
```


Using
-----

This is a trimmed down version of https://github.com/sequitur-g2p/sequitur-g2p.  
Once built, it doesn't require any library out of the standard Python 2.7.

The model used needs to have been saved with a slight modification to output a pickle
file without a numpy array for the model discount

This can be done by adding the line:
```model.discount = model.discount.tolist()```
just before the call to `pickle.dump`

