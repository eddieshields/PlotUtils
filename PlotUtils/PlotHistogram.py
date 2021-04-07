import ROOT as r
from ROOT import TH1, TH2, TH3

import matplotlib.pyplot as plt

from PlotUtils.ROOTutils import *
from PlotUtils.PlotAbs import PlotAbs

'''
Class for plotting ROOT TH1 objects.

Generally MatPlotLib produces nicer plots than root so this class
converts ROOT objects like TH1 and TF1 and plots them in MatPlotLib.
'''
class PlotHistogram(PlotAbs):
    def __init__(self,hist,func=False,pull=True,legend=False,label='Preliminary',log_scale=False,name='canv',xname='',yname=''):
        # Initiate base class.
        super(PlotHistogram, self).__init__(pull=pull,log_scale=log_scale)

        self.hist = hist
        self.ff = func

        self.label = label 
        self.xmin = hist.GetXaxis().GetXmin()
        self.xmax = hist.GetXaxis().GetXmax()
        self.ymin = 0.1
        self.ymax = 1.1 * hist.GetMaximum()
        self.bin_width = hist.GetBinWidth(1)

        # Set axis.
        self.xtitle = hist.GetXaxis().GetTitle()
        self.ytitle = hist.GetYaxis().GetTitle()
        self.units  = ''

        # Miscellanious.
        self.legend = legend

        # Plot function.
        if ( self.ff ):
            x_vals, pdf_vals = listfromtf1( self.ff )
            self.add_plot(x_vals,pdf_vals,color='blue',linewidth=2.5,label='Fit')

        # Plot points.
        x, y, x_err, yerr = listfromhist( self.hist )
        self.add_errorbar(x,y,x_err,yerr,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8,label='Data')

    def plot(self,output=0):

        # Plot function.
        if ( self.ff ):
            x_vals, pdf_vals = listfromtf1( self.ff )
            self.add_plot(x_vals,pdf_vals,color='blue',linewidth=2.5,label='Fit')

        # Plot points.
        x, y, x_err, yerr = listfromhist( self.hist )
        self.add_errorbar(x,y,x_err,yerr,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8,label='Data')

        # Add legend.
        if ( self.legend ): self.add_legend(loc='upper left',fontsize=20,ncol=1,frameon=False)

        # Add pull.
        if ( self.pull ):
            x, pull_vals = listforpull( self.hist, self.ff )
            self.add_pull(x,pull_vals)

        return self.set_plot(output)