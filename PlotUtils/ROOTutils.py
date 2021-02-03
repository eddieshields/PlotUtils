import ROOT as r
from ROOT import TH1, TH2, RooDataHist, TGraph, TGraphErrors
import numpy as np
import matplotlib.pyplot as plt


def listfromhist(hist):
    '''
    Take the values from the histogram and add them to a series 
    of arrays.
    '''
    x, y, x_err, y_err = [ ], [ ], [ ], [ ]
    for n in range(1,hist.GetNbinsX()+1):
        x.append(hist.GetXaxis().GetBinCenter(n))
        y.append(hist.GetBinContent(n))
        x_err.append(hist.GetXaxis().GetBinWidth(n)*0.5)
        y_err.append(hist.GetBinError(n))

    return np.array(x), np.array(y), np.array( x_err ), np.array( y_err )

def listfrom2dhist(hist):
    x = np.zeros(hist.GetNbinsX())
    y = np.zeros(hist.GetNbinsY())
    vals = np.zeros(hist.GetNbinsX()*hist.GetNbinsY(),dtype='float64')
    errs = np.zeros(hist.GetNbinsX()*hist.GetNbinsY(),dtype='float64')
    vals = vals.reshape(hist.GetNbinsY(),hist.GetNbinsX())
    errs = errs.reshape(hist.GetNbinsY(),hist.GetNbinsX())
    for i in range(1,hist.GetNbinsX()+1):
        x[i-1] = hist.GetXaxis().GetBinCenter(i)
        for j in range(1,hist.GetNbinsY()+1):
            y[j-1] = eff.GetYaxis().GetBinCenter(j)
            vals[i-1][j-1] = hist.GetBinContent(i,j)
            errs[i-1][j-1] = hist.GetBinError(i,j)

    return x, y, vals, errs

def listfromgraph(gr):
    '''
    Take the values from a TGraph and add them to a series 
    of arrays
    '''
    xm, ym = gr.GetX(), gr.GetY()
    x, y = [ ], [ ]
    for n in range(0,gr.GetN()):
        x.append( xm[n] )
        y.append( ym[n] )
    
    return np.array(x), np.array(y)

def listfromgrapherrors(gr):
    '''
    Take the values from a TGraph and add them to a series 
    of arrays
    '''
    xm, ym, x_errm, y_errm = gr.GetX(), gr.GetY(), gr.GetEX(), gr.GetEY()
    x, y, x_err, y_err = [ ], [ ], [ ], [ ]
    for n in range(0,gr.GetN()):
        x.append( xm[n] )
        y.append( ym[n] )
        x_err.append( x_errm[n] )
        y_err.append( y_errm[n] ) 

    return np.array(x), np.array(y), np.array( x_err ), np.array( y_err )

def listfromtf1(ff):
    '''
    Takes values from a fit function and puts them into an array
    to be plotted.
    '''
    x_vals = np.linspace(ff.GetXaxis().GetXmin(),ff.GetXaxis().GetXmax(),1000)
    pdf_vals = [ ]
    for v in x_vals:
        pdf_vals.append( ff.Eval( v ) )

    return x_vals, np.array( pdf_vals )

def listforpull(hist,ff):
    x, pull_vals = [ ], [ ]
    for n in range(1,hist.GetNbinsX()+1):
        x.append( hist.GetBinCenter( n ) )
        if not ( hist.GetBinError( n ) ):
            pull_vals.append( 0. )
            continue
        pull_vals.append( ( hist.GetBinContent( n ) - ff.Eval( hist.GetBinCenter( n ) ) ) / hist.GetBinError( n ) )

    return x, pull_vals


