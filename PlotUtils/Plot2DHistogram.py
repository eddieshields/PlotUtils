import ROOT as r
from ROOT import TH1, TH2, TH3

import matplotlib.pyplot as plt
import seaborn as sns
from PlotUtils.ROOTutils import *
from PlotUtils.PlotAbs import PlotAbs


class Plot2DHistogram(PlotAbs):
    def __init__(self,hist,simulation=False,preliminary=True,legend=True,**kwargs):
        # Initiate base class.
        super(Plot2DHistogram, self).__init__()

        self.hist = hist
        #self.xmin = hist.GetXaxis().GetXmin()
        #self.xmax = hist.GetXaxis().GetXmax()
        #self.ymin = hist.GetYaxis().GetXmin()
        #self.ymax = hist.GetXaxis().GetXmax()
        #self.bin_width = hist.GetBinWidth(1,1)

        # Set axis.
        #self.xtitle = kwargs['xtitle'] if ( kwargs.__contains__('xtitle') ) else hist.GetXaxis().GetTitle()
        #self.ytitle = kwargs['ytitle'] if ( kwargs.__contains__('ytitle') ) else hist.GetYaxis().GetTitle()
        #self.units  = kwargs['units']  if ( kwargs.__contains__('units')  ) else ''

        # Miscellanious.
        self.legend = legend
        self.simulation = simulation
        self.preliminary = preliminary

    def plot(self,output=0):
        #if ( isinstance(self.hist,r.TH2D) ): x, y, vals, errs = listfrom2dhist( self.hist )
        #else: vals = hist
        vals = self.hist

        self.ax = sns.heatmap(vals,square=True, cmap="YlGnBu")

        if ( output ):
            self.fig.savefig( output )
            print('Saved figure to '+output)
        return self.fig