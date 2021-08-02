from ROOT import TH1D, TF1

import sys
import os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import plotutils


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4


def test_histogram():
    ff = TF1('fit', 'gaus', -3, 3)
    h = TH1D("h", "h", 100, -3, 3)
    h.FillRandom("gaus", 5000)

    h.Fit(ff)

    #plotutils.Plot()

    assert 1 == 1
