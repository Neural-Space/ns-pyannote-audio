#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2016 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


from __future__ import division

import h5py
import numpy as np
import pysndfile.sndio
from pyannote.core import SlidingWindow, SlidingWindowFeature


class PyannoteFeatureExtractionError(Exception):
    pass


def get_wav_duration(wav):
    y, sample_rate, _ = pysndfile.sndio.read(wav)
    n_samples = y.shape[0]
    return n_samples / sample_rate


class Precomputed(object):
    """Load precomputed features from HDF5 file

    Parameters
    ----------
    features_h5 : str
        Path to HDF5 file generated by script 'feature_extraction.py'.
    """

    def __init__(self, features_h5=None):
        super(Precomputed, self).__init__()
        self.features_h5 = features_h5

        self.f_ = h5py.File(self.features_h5, 'r')

        start = self.f_.attrs['start']
        duration = self.f_.attrs['duration']
        step = self.f_.attrs['step']
        self.sliding_window_ = SlidingWindow(
            start=start, duration=duration, step=step)

        self.dimension_ = self.f_.attrs['dimension']

    def __call__(self, wav):

        if wav not in self.f_:
            msg = 'Cannot extract features from "{wav}".'
            raise PyannoteFeatureExtractionError(msg.format(wav=wav))

        data = np.array(self.f_['wav'])
        return SlidingWindowFeature(data, self.sliding_window_)

    def sliding_window(self):
        return self.sliding_window_

    def dimension(self):
        return self.dimension_
