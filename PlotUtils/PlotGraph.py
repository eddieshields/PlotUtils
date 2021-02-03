import ROOT as r
from ROOT import TGraph, TGraphErrors

import matplotlib.pyplot as plt

from PlotUtils.PlotAbs import PlotAbs
from PlotUtils.ROOTutils import *

class PlotGraph(PlotAbs):
    def __init__(self,gr,func=False,errors=True,simulation=False,preliminary=True,confidencebands=False,blind=False,legend=True,**kwargs):
        '''
        Initiate class
        '''
        super(PlotGraph, self).__init__()

        self.gr = gr
        self.ff = func
        self.xmin = kwargs['xmin'] if ( kwargs.__contains__('xmin') ) else gr.GetXaxis().GetXmin()
        self.xmax = kwargs['xmax'] if ( kwargs.__contains__('xmax') ) else gr.GetXaxis().GetXmax()
        self.ymin = kwargs['ymin'] if ( kwargs.__contains__('ymin') ) else gr.GetYaxis().GetXmin()
        self.ymax = kwargs['ymax'] if ( kwargs.__contains__('ymax') ) else gr.GetYaxis().GetXmax()
        # Set axis.
        self.xtitle = kwargs['xtitle'] if ( kwargs.__contains__('xtitle') ) else gr.GetXaxis().GetTitle()
        self.ytitle = kwargs['ytitle'] if ( kwargs.__contains__('ytitle') ) else gr.GetYaxis().GetTitle()
        self.units  = kwargs['units']  if ( kwargs.__contains__('units')  ) else ''
        # Blind.
        self.blind = blind
        # Miscellanious.
        self.legend = legend
        self.errors = errors
        self.simulation = simulation
        self.preliminary = preliminary
        self.confidencebands = confidencebands

        self.components = kwargs['components'] if ( kwargs.__contains__('components') ) else {}

    def plot(self,output=0):
        '''
        Plot everything.
        '''

        if ( self.ff ):
            # Plot confidence bands.
            if ( self.confidencebands ):
                onesigma_band, twosigma_band = self.calculateconfidencebands()
                two_x, two_y, two_xerr, two_yerr = listfromgrapherrors( twosigma_band )
                if ( self.blind ):
                    for i in range(len(two_x)):
                        two_y[i] = two_y[i] + self.blind*two_x[i]
                self.add_confidenceband(two_x,two_y,two_yerr,color='yellow')
                one_x, one_y, one_xerr, one_yerr = listfromgrapherrors( onesigma_band )
                if ( self.blind ):
                    for i in range(len(one_x)):
                        one_y[i] = one_y[i] + self.blind*one_x[i]
                self.add_confidenceband(one_x,one_y,one_yerr,color='lime')

            if ( self.components ):
                self.addcomponents( self.components )
            
            # Plot fit shape.
            x_vals, pdf_vals = listfromtf1( self.ff )
            if ( self.blind ):
                for i in range(len(x_vals)):
                    pdf_vals[i] = pdf_vals[i] + self.blind*x_vals[i]
            self.add_plot(x_vals,pdf_vals,color='blue',linewidth=2.5,label='Fit')

        # Plot graph.
        x, y, x_err, y_err = listfromgrapherrors( self.gr )
        if ( self.blind ):
            print('\033[0;31m BLINDING RESULT \033[0m')
            for i in range(len(x)):
                y[i] = y[i] + self.blind*x[i]
        self.add_errorbar(x,y,x_err,y_err,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8)

        # Add legend.
        if ( self.legend ): self.add_legend(loc='upper left',fontsize=20,ncol=1,frameon=False)

        # Add label.
        self.add_LHCbLabel(simulation=self.simulation,preliminary=self.preliminary)

        return self.set_plot(output)

    def calculateconfidencebands(self):
        onesigma_band = r.TGraphErrors(1000)
        twosigma_band = r.TGraphErrors(1000)
        for i in range(1000):
            x = (self.xmax/1000.)*i
            y = 0
            onesigma_band.SetPoint(i,x,y)
            twosigma_band.SetPoint(i,x,y)

        (r.TVirtualFitter.GetFitter()).GetConfidenceIntervals(onesigma_band,0.68)
        (r.TVirtualFitter.GetFitter()).GetConfidenceIntervals(twosigma_band,0.95)

        return onesigma_band, twosigma_band


    def add_confidenceband(self,x,y,y_err,**kwargs):
        self.ax.fill_between(x, y-y_err,y+y_err,**kwargs)

        return

    def addcomponents(self,components):
        '''
        Plots components
        '''
        for comp, settings in components.items():
            x, y, x_err, y_err = listfromgrapherrors( comp )
            self.add_errorbar(x,y,x_err,y_err,**settings)

        return