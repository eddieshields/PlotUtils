import ROOT as r
from ROOT import TGraph, TGraphErrors

import matplotlib.pyplot as plt
from matplotlib import gridspec

from PlotUtils.PlotAbs import PlotAbs
from PlotUtils.ROOTutils import *

class PlotGraph(PlotAbs):
    def __init__(self,gr,func=False,errors=True,
                 confidencebands=False,blind=False,legend=True,**kwargs):
        '''
        Initiate class
        '''
        super(PlotGraph, self).__init__(**kwargs)

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
        self.confidencebands = confidencebands


    def plot(self,output=0):
        '''
        Plot everything.
        '''

        if ( self.ff ):
            # Plot confidence bands.
            if ( self.confidencebands ):
                onesigma_band, twosigma_band = self.calculateconfidencebands()
                two_x, two_y, two_xerr, two_yerr = listfromgrapherrors( twosigma_band )
                if ( self.blind ): two_y = self.blindlist( two_y )
                self.add_confidenceband(two_x,two_y,two_yerr,color='yellow')
                one_x, one_y, one_xerr, one_yerr = listfromgrapherrors( onesigma_band )
                if ( self.blind ): one_y = self.blindlist( one_y )
                self.add_confidenceband(one_x,one_y,one_yerr,color='lime')

            # Plot fit shape.
            x_vals, pdf_vals = listfromtf1( self.ff )
            if ( self.blind ): pdf_vals = self.blindlist( pdf_vals )
            self.add_plot(x_vals,pdf_vals,color='blue',linewidth=2.5,label='Fit')

        # Plot graph.
        x, y, x_err, y_err = listfromgrapherrors( self.gr )
        if ( self.blind ):
            print('\033[0;31m BLINDING RESULT \033[0m')
            y = self.blindlist(y)
        self.add_errorbar(x,y,x_err,y_err,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8,label='Data')

        # Add legend.
        if ( self.legend ): self.add_legend(loc='upper left',fontsize=20,ncol=1,frameon=False)

        return self.set_plot(output)

    def blindlist(self,list):
        for i in range(len(list)):
            list[i] = list[i] + self.blind*list[i]
        return list

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

    def add_graph(self,gr,**kwargs):
        '''
        Add an additional TGraph.
        '''
        if ( isinstance(gr,r.TGraphErrors) ):
            x, y, x_err, y_err = listfromgrapherrors( gr )
            self.add_errorbar(x,y,x_err,y_err,**kwargs)
        else:
            x, y = listfromgraph( gr )
            self.add_scatter(x,y,**kwargs)

        return

    def plot_break(self,break1,break2,output=0):
        '''
        Plot graph that is broken in the x-axis.
        Code adapted from https://stackoverflow.com/questions/32185411/break-in-x-axis-of-matplotlib
        '''
        self.fig = plt.figure(figsize=(12,8))
        self.spec = gridspec.GridSpec(ncols=2, nrows=3, width_ratios=[break1-self.xmin, self.xmax-break2], hspace=None)
        self.ax = self.fig.add_subplot(self.spec[0])
        self.ax2 = self.fig.add_subplot(self.spec[1],sharey=self.ax)

        if ( self.ff ):
            # Plot confidence bands.
            if ( self.confidencebands ):
                onesigma_band, twosigma_band = self.calculateconfidencebands()
                two_x, two_y, two_xerr, two_yerr = listfromgrapherrors( twosigma_band )
                if ( self.blind ): two_y = self.blindlist( two_y )
                self.add_confidenceband(two_x,two_y,two_yerr,color='yellow')
                self.ax2.fill_between(two_x,two_y-two_yerr,two_y+two_yerr,color='yellow')
                one_x, one_y, one_xerr, one_yerr = listfromgrapherrors( onesigma_band )
                if ( self.blind ): one_y = self.blindlist( one_y )
                self.add_confidenceband(one_x,one_y,one_yerr,color='lime')
                self.ax2.fill_between(one_x,one_y-one_yerr,one_y+one_yerr,color='lime')

            # Plot fit shape.
            x_vals, pdf_vals = listfromtf1( self.ff )
            if ( self.blind ): pdf_vals = self.blindlist( pdf_vals )
            self.add_plot(x_vals,pdf_vals,color='blue',linewidth=2.5,label='Fit')
            self.ax2.plot(x_vals,pdf_vals,color='blue',linewidth=2.5)

        # Plot graph.
        x, y, x_err, y_err = listfromgrapherrors( self.gr )
        if ( self.blind ):
            print('\033[0;31m BLINDING RESULT \033[0m')
            y = self.blindlist(y)
        self.add_errorbar(x,y,x_err,y_err,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8,label='Data')
        self.ax2.errorbar(x,y,x_err,y_err,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8)

        self.ax.set_xlim(self.xmin,break1)
        self.ax2.set_xlim(break2,self.xmax)

        # hide the spines between ax and ax2
        self.ax.spines['right'].set_visible(False)
        self.ax2.spines['left'].set_visible(False)
        self.ax.yaxis.tick_left()
        self.ax2.tick_params(labelright='off')
        self.ax2.axes.yaxis.set_visible(False)
        #self.ax2.yaxis.tick_right()
        #self.ax2.yaxis.set_yticks([])

        d = .015 # how big to make the diagonal lines in axes coordinates
        # arguments to pass plot, just so we don't keep repeating them
        kwargs2 = dict(transform=self.ax.transAxes, color='k', clip_on=False)
        self.ax.plot((1-d,1+d), (-d,+d), **kwargs2)
        self.ax.plot((1-d,1+d),(1-d,1+d), **kwargs2)

        kwargs2.update(transform=self.ax2.transAxes)  # switch to the bottom axes
        self.ax2.plot((-d,+d), (1-d,1+d), (-d,+d), **kwargs2)
        self.ax2.plot((-d,+d), (-d,+d), **kwargs2)

        # This code come from set_plot.
        # Axis.
        self.ax2.set_xlabel('$%s$'%self.xtitle,fontsize=35,horizontalalignment='right', x=1.0)
        self.ax.set_ylabel('$%s$'%self.ytitle,fontsize=35,horizontalalignment='right', y=1.0)
        self.ax.tick_params(axis='both', which='major', labelsize=30)

        if ( self.ymax ): 
            self.ax.set_ylim(self.ymin,self.ymax)
        
        margins = {  #     vvv margin in inches
        		"left"   : 0.17,
        		"bottom" : 0.15,
        		"right"  : 0.99,
        		"top"    : 0.98
        		}

        if ( self.logy ): self.ax.set_yscale('log')
        self.fig.subplots_adjust(wspace=0.1)
        self.fig.subplots_adjust(**margins)

        if ( output ):
            self.fig.savefig( output )
            print('Saved figure to '+output)
        return self.ax, self.fig
