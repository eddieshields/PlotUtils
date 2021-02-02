import ROOT as r
from ROOT import TGraph, TGraphErrors

import matplotlib.pyplot as plt

from PlotUtils.PlotAbs import PlotAbs
from PlotUtils.ROOTutils import *

class PlotGraph(PlotAbs):
    def __init__(self):
        '''
        Initiate class
        '''
        super(PlotHistogram, self).__init__()

        self.gr = gr
        self.ff = func
        self.xmin = gr.GetXaxis().GetXmin()
        self.xmax = gr.GetXaxis().GetXmax()
        self.ymin = gr.GetYaxis().GetXmin()
        self.ymax = gr.GetYaxis().GetXmax()
        # Set axis.
        self.xtitle = kwargs['xtitle'] if ( 'xtitle' in kwargs) else gr.GetXaxis().GetTitle()
        self.ytitle = kwargs['ytitle'] if ( 'ytitle' in kwargs) else gr.GetYaxis().GetTitle()
        self.units  = kwargs['units']  if ( 'units' in kwargs ) else ''
        # Blind.
        self.blind = blind
        # Miscellanious.
        self.simulation = simulation
        self.preliminary = preliminary
        self.confidencebands = confidenceband

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
                self.add_confidenceband(two_x,two_y,two_yerr,color='green')
            
            # Plot fit shape.
            x_vals, pdf_vals = listfromtf1( self.ff )
            if ( self.blind ):
                for i in range(len(x_vals)):
                    pdf_vals[i] = pdf_vals[i] + self.blind*x_vals[i]
            self.add_plot(x_vals,pdf_vals,color='blue',linewidth=2.5)

        # Plot graph.
        if ( self.errors ): x, y, x_err, y_err = listfromgrapherrors( self.gr )
        else: x, y, x_err, y_err = listfromgraph( self.gr )
        if ( self.blind ):
            for i in range(len(x)):
                y[i] = y[i] + self.blind*x[i]
        self.add_errorbar(x,y,x_err,y_err,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8)

        # Add legend.
        if ( self.legend ): self.add_legend(loc='upper right',fontsize=20,ncol=1,frameon=False)

        # Add label.
        self.add_LHCbLabel(simulation=self.simulation,preliminary=self.preliminary)

        return self.set_plot(output)

    def calculateconfidencebands(self):
        onesigma_band = r.TGraphErrors(1000)
        twosigma_band = r.TGraphErrors(1000)
        for i in range(1000):
            x = (self.ymax/1000.)*i
            y = 0
            onesigma_band.SetPoint(i,x,y)
            twosigma_band.SetPoint(i,x,y)

        (r.TVirtualFitter.GetFitter()).GetConfidenceIntervals(onesigma_band,0.68)
        (r.TVirtualFitter.GetFitter()).GetConfidenceIntervals(twosigma_band,0.95)

        return onesigma_band, twosigma_band


    def add_confidenceband(self,x,y,y_err,**kwargs):
        self.ax.fill_between(x, y-y_err,y+yerr,**kwargs)

        return
   



#'''
#Class that takes in a ROOT histogram and plots it nicely using matplotlib
#'''
#class PlotGraph:
#    def __init__(self,gr,func=False,errors=True,simulation=False,preliminary=True,confidencebands=False,blind=False,**kwargs):
#        '''
#        Initiate class
#        '''
#        # Set font.
#        rc('font',**{'family':'serif','serif':['Roman']}) 
#        rc('text', usetex=True)
#
#        self.gr = gr
#        self.ff = func
#        self.errors = errors
#        self.xmin = gr.GetXaxis().GetXmin()
#        self.xmax = gr.GetXaxis().GetXmax()
#        self.ymin = gr.GetYaxis().GetXmin()
#        self.ymax = gr.GetYaxis().GetXmax()
#
#        # Set axis.
#        self.xtitle = kwargs['xtitle'] if ( 'xtitle' in kwargs) else gr.GetXaxis().GetTitle()
#        self.ytitle = kwargs['ytitle'] if ( 'ytitle' in kwargs) else gr.GetYaxis().GetTitle()
#        self.units  = kwargs['units']  if ( 'units' in kwargs ) else ''
#
#        # Blind.
#        self.blind = blind
#
#        # Miscellanious.
#        self.simulation = simulation
#        self.preliminary = preliminary
#        self.confidencebands = confidencebands
#
#    def plot(self,output=0):
#        '''
#        Plot everything.
#        '''
#        fig, ax = plt.subplots(figsize=(12,8))
#
#        if ( self.ff ):
#            # Plot confidence bands.
#            if ( self.confidencebands ):
#                onesigma_band, twosigma_band = self.calculateconfidencebands()
#                two_x, two_y, two_xerr, two_yerr = listfromgrapherrors( twosigma_band )
#                if ( self.blind ):
#                    for i in range(len(two_x)):
#                        two_y[i] = two_y[i] + self.blind*two_x[i]
#                plt.fill_between(two_x, two_y-two_yerr, two_y+two_yerr,color='yellow')
#                one_x, one_y, one_xerr, one_yerr = listfromgrapherrors( onesigma_band )
#                if ( self.blind ):
#                    for i in range(len(one_x)):
#                        one_y[i] = one_y[i] + self.blind*one_x[i]
#                plt.fill_between(one_x, one_y-one_yerr, one_y+one_yerr,color='green')
#            # Plot fit shape.
#            x_vals, pdf_vals = listfromtf1( self.ff )
#            if ( self.blind ):
#                for i in range(len(x_vals)):
#                    pdf_vals[i] = pdf_vals[i] + self.blind*x_vals[i]
#            plt.plot(x_vals,pdf_vals,color='blue',linewidth=2.5)
#
#        # Plot graph.
#        if ( self.errors ): x, y, x_err, y_err = listfromgrapherrors( self.gr )
#        else: x, y, x_err, y_err = listfromgraph( self.gr )
#        if ( self.blind ):
#            for i in range(len(x)):
#                y[i] = y[i] + self.blind*x[i]
#        plt.errorbar(x,y,xerr=x_err,yerr=y_err,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8)
#            
#        # Axis.
#        plt.ylabel("$%s$" % self.ytitle,fontsize=35,horizontalalignment='right', y=1.0)
#        plt.xlabel("$%s$" % (self.xtitle),fontsize=35,horizontalalignment='right', x=1.0)
#        ax.tick_params(axis='both', which='major', labelsize=30)
#        plt.xlim(self.xmin,self.xmax)
#        #plt.ylim(0.1,self.ymax*1.05)
#        
#        #Add LHCb logo
#        plt.text(0.1*self.xmax,0.9*self.ymax,"\\textbf{LHCb}",fontsize=35)
#        if ( self.simulation ): plt.text(0.1*self.xmax,0.85*self.ymax,"\\textit{simulation}",fontsize=25)
#        else:
#            if ( self.preliminary ): plt.text(0.1*self.xmax,0.85*self.ymax,"\\textit{preliminary}",fontsize=25)
#        
#        margins = {  #     vvv margin in inches
#        		"left"   : 0.17,
#        		"bottom" : 0.15,
#        		"right"  : 0.99,
#        		"top"    : 0.98
#        		}
#
#        fig.subplots_adjust(**margins)
#
#        if ( output ):
#            fig.savefig( output )
#            print('Saved figure to '+output)
#        return fig
#
#    def calculateconfidencebands(self):
#        onesigma_band = r.TGraphErrors(1000)
#        twosigma_band = r.TGraphErrors(1000)
#        for i in range(1000):
#            x = (self.ymax/1000.)*i
#            y = 0
#            onesigma_band.SetPoint(i,x,y)
#            twosigma_band.SetPoint(i,x,y)
#
#        (r.TVirtualFitter.GetFitter()).GetConfidenceIntervals(onesigma_band,0.68)
#        (r.TVirtualFitter.GetFitter()).GetConfidenceIntervals(twosigma_band,0.95)
#
#        return onesigma_band, twosigma_band
#