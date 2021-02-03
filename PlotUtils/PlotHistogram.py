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
    def __init__(self,hist,func=False,pull=False,simulation=False,preliminary=True,legend=True,log_scale=False,**kwargs):
        # Initiate base class.
        super(PlotHistogram, self).__init__(pull=pull,log_scale=log_scale)

        self.hist = hist
        self.ff = func
        self.xmin = hist.GetXaxis().GetXmin()
        self.xmax = hist.GetXaxis().GetXmax()
        self.ymin = 0.1
        self.ymax = 1.1 * hist.GetMaximum()
        self.bin_width = hist.GetBinWidth(1)

        # Set axis.
        self.xtitle = kwargs['xtitle'] if ( kwargs.__contains__('xtitle') ) else hist.GetXaxis().GetTitle()
        self.ytitle = kwargs['ytitle'] if ( kwargs.__contains__('ytitle') ) else hist.GetYaxis().GetTitle()
        self.units  = kwargs['units']  if ( kwargs.__contains__('units')  ) else ''

        self.components = kwargs['components'] if ( kwargs.__contains__('components') ) else {}

        # Miscellanious.
        self.legend = legend
        self.simulation = simulation
        self.preliminary = preliminary

    def plot(self,output=0):
        # Plot components.
        if ( self.components ): self.addcomponents( self.components )

        # Plot function.
        if ( self.ff ):
            x_vals, pdf_vals = listfromtf1( self.ff )
            self.add_plot(x_vals,pdf_vals,color='blue',linewidth=2.5,label='Fit')

        # Plot points.
        x, y, x_err, yerr = listfromhist( self.hist )
        self.add_errorbar(x,y,x_err,yerr,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8,label='Data')

        # Add legend.
        if ( self.legend ): self.add_legend(loc='upper left',fontsize=20,ncol=1,frameon=False)

        # Add label.
        self.add_LHCbLabel(simulation=self.simulation,preliminary=self.preliminary)

        # Add pull.
        if ( self.pull ):
            x, pull_vals = listforpull( self.hist, self.ff )
            self.add_pull(x,pull_vals)

        return self.set_plot(output)

        
    def addcomponents(self,components):
        '''
        Plots components
        '''
        for comp, settings in components.items():
            x, y = listfromtf1( comp )
            if ( settings.__contains__('fill') ):
                fill = settings.pop('fill')
                if ( fill == True ):
                    self.add_fill(x,y,**settings)
            else:
                self.add_plot(x,y,**settings)

        return