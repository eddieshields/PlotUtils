import inspect
from ROOT import (TObject, TH1, TGraph, TGraphErrors,
                  TF1, TVirtualFitter, RooRealVar)
import numpy as np

from plotutils._roofit_utils import _convert_roofit_object


def root_plotable(func):
    """
    Wrapper around a matplotlib function to
    plot ROOT object directly.
    """
    def _root_converter(*args, **kwargs):
        if _check_for_root_object(*args, **kwargs):
            plotable = _convert_object(*args, **kwargs)
            # Check if function accepts x and y key arguments.
            if 'x' not in inspect.signature(func).parameters.keys():
                func(plotable['x'], plotable['y'], **kwargs)
            else:
                # Remove keys that are not accepted by function.
                remove = []
                for k in plotable.keys():
                    if k not in inspect.signature(func).parameters.keys():
                        remove.append(k)
                for r in remove:
                    plotable.pop(r)
                func(**plotable, **kwargs)
        else:
            func(*args, **kwargs)

    return _root_converter


def _check_for_root_object(*args, **kwargs):
    """
    Check if any of the parameters passed
    to the function are derived from the
    ROOT base class TObject.
    """
    for obj in args:
        if isinstance(obj, TObject):
            return True
    for obj in kwargs.values():
        if isinstance(obj, TObject):
            return True

    return False


def _convert_object(root_obj: TObject, *args, **kwargs):
    if isinstance(root_obj, RooRealVar):
        return _convert_root_object(_convert_roofit_object(root_obj,
                                    *args, **kwargs))
    else:
        return _convert_root_object(root_obj)


def _convert_root_object(root_obj: TObject) -> tuple:
    """
    Convert a root object to a series of objects that can be plotted.
    The return type must be a tuple.

    Parameters
    ----------
    root_obj : TObject
        ROOT object

    Returns
    -------
    plotable : dict
        Dictionary of plotable arrays
    """
    if isinstance(root_obj, TH1):
        plotable = _convert_th1(root_obj)
    elif isinstance(root_obj, TGraph):
        plotable = _convert_tgraph(root_obj)
    elif isinstance(root_obj, TGraphErrors):
        plotable = _convert_tgrapherrors(root_obj)
    elif isinstance(root_obj, TF1):
        plotable = _convert_tf1(root_obj)

    return plotable


def _convert_th1(root_obj: TH1) -> dict:
    """
    Take the values from the histogram and add them to a series
    of arrays.

    Parameters
    ----------
    root_obj : TH1
        ROOT histogram

    Returns
    -------
    dict
        Dictionary with x, y, xerr, yerr points
    """
    assert(isinstance(root_obj, TH1))
    x, y, x_err, y_err = [], [], [], []
    for n in range(1, root_obj.GetNbinsX() + 1):
        x.append(root_obj.GetXaxis().GetBinCenter(n))
        y.append(root_obj.GetBinContent(n))
        x_err.append(root_obj.GetXaxis().GetBinWidth(n) * 0.5)
        y_err.append(root_obj.GetBinError(n))

    return {'x': np.array(x), 'y': np.array(y),
            'xerr': np.array(x_err), 'yerr': np.array(y_err)}


def _convert_tgraph(root_obj: TGraph) -> dict:
    """
    Take the values from a TGraph and add them to a series
    of arrays

    Parameters
    ----------
    root_obj : TGraph
        ROOT TGraph

    Returns
    -------
    dict
        Dictionary with x, y points
    """
    assert(isinstance(root_obj, TGraph))
    xm, ym = root_obj.GetX(), root_obj.GetY()
    x, y = [], []
    for n in range(0, root_obj.GetN()):
        x.append(xm[n])
        y.append(ym[n])

    return {'x': np.array(x), 'y': np.array(y)}


def _convert_tgrapherrors(root_obj: TGraphErrors) -> dict:
    """
    Take the values from a TGraphErrors and add them to a series
    of arrays

    Parameters
    ----------
    root_obj : TGraphError
        ROOT TGraphError

    Returns
    -------
    dict
        Dictionary with x, y, xerr, yerr points
    """
    xm, ym, x_errm, y_errm = (root_obj.GetX(),
                              root_obj.GetY(),
                              root_obj.GetEX(),
                              root_obj.GetEY())
    x, y, x_err, y_err = [], [], [], []
    for n in range(0, root_obj.GetN()):
        x.append(xm[n])
        y.append(ym[n])
        x_err.append(x_errm[n])
        y_err.append(y_errm[n])

    return {'x': np.array(x), 'y': np.array(y),
            'xerr': np.array(x_err), 'yerr': np.array(y_err)}


def _convert_tf1(root_obj: TF1) -> dict:
    """
    Takes values from a fit function and puts them into an array
    to be plotted.

    Parameters
    ----------
    root_obj : TF1
        ROOT TF1

    Returns
    -------
    dict
        Dictionary with x, y points
    """
    assert(isinstance(root_obj, TF1))
    x = np.linspace(root_obj.GetXaxis().GetXmin(),
                    root_obj.GetXaxis().GetXmax(),
                    1000)
    y = []
    for p in x:
        y.append(root_obj.Eval(p))

    return {'x': x, 'y': np.array(y)}


def _calculate_confidence_band(root_obj: TF1,
                               ci: float,
                               steps: int = 1000) -> dict:
    """
    Calculate confidence bands from a fit of a
    TF1 to a histogram.

    Parameters
    ----------
    root_obj : TH1
        ROOT TF1 pdf used for the fit
    ci : float
        Confidence interval
    steps : int
        Number of points in band

    Returns
    -------
    dict
        Dictionary with x, y, xerr, yerr points
    """
    assert(isinstance(root_obj, TF1))
    band = TGraphErrors(steps)
    lowb, highb = root_obj.GetXaxis().GetXmin(), root_obj.GetXaxis().GetXmax()
    for i in range(steps):
        x = (lowb + (
             (highb - lowb) / steps) * i)
        y = 0
        band.SetPoint(i, x, y)
        (TVirtualFitter.GetFitter()).GetConfidenceIntervals(band, ci)

    return _convert_tgrapherrors(band)


def confidence_band(ff: TF1, ci: float, steps: int = 1000) -> dict:
    """
    Calculate the confidence bands from a fit of a
    TF1 to a histogram and return the points ready to
    be directly plotted.

    Parameters
    ----------
    root_obj : TH1
        ROOT TF1 pdf used for the fit
    ci : float
        Confidence interval
    steps : int
        Number of points in band

    Returns
    -------
    dict
        Dictionary with x, y1, y2 points
    """
    points = _calculate_confidence_band(ff, ci, steps)
    return {'x': points['x'], 'y1': points['y'] - points['yerr'],
            'y2': points['y'] + points['yerr']}


def calculate_pull(hist: TH1, ff: TF1) -> tuple:
    """
    Calculate a pull plot between a histogram and a fitted function.

    Parameters
    ----------
    hist : TH1
        ROOT TH1 histogram
    ff : TF1
        ROOT TF1 function used to fit.

    Returns
    -------
    x, y : np.array, np.array
        points for pull plot
    """
    x, y = [], []
    for n in range(1, hist.GetNbinsX() + 1):
        x.append(hist.GetBinCenter(n))
        if not hist.GetBinError(n):
            y.append(0)
            continue
        y.append((hist.GetBinContent(n) - ff.Eval(hist.GetBinCenter(n))) / (
                 hist.GetBinError(n)))

    return x, y
