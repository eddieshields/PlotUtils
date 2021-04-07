import ROOT as r
from ROOT import RooRealVar, RooDataHist, RooDataSet, RooGaussian, RooAddPdf, RooArgSet

import sys, os
sys.path.append( os.getcwd() )
from PlotUtils.PlotRooHistogram import PlotRooHistogram

def main():
    x = RooRealVar("x","x",-10,10)

    m = RooRealVar("m","mean",-3,-10,10)
    s = RooRealVar("s","sigma",3,0.1,10)
    g1 = RooGaussian("g1","Gaussian1",x,m,s)

    m2 = RooRealVar("m1","mean2",3,-10,10)
    s2 = RooRealVar("s2","sigma2",3,0.1,10)
    g2 = RooGaussian("g2","Gaussian2",x,m2,s2)

    f = RooRealVar("f","fraction",0.5,0,1)

    model = RooAddPdf("model","model",g1,g2,f)

    # Generate data.
    data = model.generate(RooArgSet(x),1000)

    # Fit.
    model.fitTo(data)

    mp = PlotRooHistogram(x,data.binnedClone(),model,pull=True)
    mp.add_component('g1','Gaussian 1',style='l',linestyle='--',color='pink')
    mp.add_component('g2','Gaussian 2',style='f',color='cyan')
    mp.add_LHCbLabel(0.01,0.9,'Preliminary')
    mp.add_legend()
    mp.plot('figs/rooplot.pdf')


#-------------------------
if __name__ == '__main__':
    main()
